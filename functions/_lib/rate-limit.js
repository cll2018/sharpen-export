// Shared limiters for the Cloudflare Pages Functions, backed by D1.
//
// Two separate problems, deliberately solved in one place:
//
//   1. The upstream LLM (agnes-3.0-flash) allows 20 requests per minute per key
//      and answers 429 beyond that. /ai-chat and /translate use the same key, so
//      they must draw from one shared budget rather than each having their own.
//   2. /rfq is a public form anyone can post to, so it needs a per-IP cap.
//
// This lives in D1 (binding RATE_LIMIT_DB) because Pages Functions are
// stateless: an in-process counter is per-isolate and cannot enforce a global
// cap, which is exactly the cap that matters against a per-key limit.
//
// Every function here FAILS OPEN. If D1 is missing or unhappy the site keeps
// working — a limiter outage must never become a site outage, and for /rfq it
// must never swallow a real customer inquiry.

/** Upstream allows 20 requests/minute for this key; stop short of the ceiling. */
const LLM_MAX_PER_MINUTE = 20;

/** /rfq: at most 5 submissions per IP inside a 5-minute window... */
const RFQ_MAX_PER_WINDOW = 5;
const RFQ_WINDOW_MINUTES = 5;

/** ...and at most 10 submissions per IP in total. */
const RFQ_MAX_TOTAL_PER_IP = 10;

const MINUTE_MS = 60_000;

/** Read a positive number from the environment, falling back to the default. */
function configured(env, name, fallback) {
  const raw = env && env[name];
  const value = Number(raw);
  return Number.isFinite(value) && value > 0 ? value : fallback;
}

/** The limits actually in force, so the docs and the tests agree with runtime. */
export function rateLimits(env) {
  return {
    llmPerMinute: configured(env, "LLM_MAX_PER_MINUTE", LLM_MAX_PER_MINUTE),
    rfqPerWindow: configured(env, "RFQ_MAX_PER_WINDOW", RFQ_MAX_PER_WINDOW),
    rfqWindowMinutes: configured(env, "RFQ_WINDOW_MINUTES", RFQ_WINDOW_MINUTES),
    rfqTotalPerIp: configured(env, "RFQ_MAX_TOTAL_PER_IP", RFQ_MAX_TOTAL_PER_IP),
  };
}

/**
 * Take one slot from the shared LLM budget.
 *
 * Fixed-window counter: one row per minute, incremented with a single atomic
 * `INSERT ... ON CONFLICT DO UPDATE ... RETURNING`, so concurrent requests in
 * different isolates cannot both read a stale count and both proceed.
 *
 * Returns `{ allowed, limit, used, retryAfterSeconds }`. `used === null` means
 * the limiter was unavailable and the call was let through.
 */
export async function takeLlmSlot(env) {
  const limit = rateLimits(env).llmPerMinute;
  const db = env && env.RATE_LIMIT_DB;
  if (!db) return { allowed: true, limit, used: null, degraded: "no-binding" };

  const now = Date.now();
  const windowStart = Math.floor(now / MINUTE_MS) * MINUTE_MS;
  const windowEndsIn = Math.max(1, Math.ceil((windowStart + MINUTE_MS - now) / 1000));

  try {
    const results = await db.batch([
      db
        .prepare(
          "INSERT INTO llm_window (window_start, used) VALUES (?1, 1) " +
            "ON CONFLICT(window_start) DO UPDATE SET used = used + 1 RETURNING used"
        )
        .bind(windowStart),
      // Only the current minute matters, so old buckets are dropped as we go.
      // Keeps the table at ~1 row/minute instead of growing without bound.
      db
        .prepare("DELETE FROM llm_window WHERE window_start < ?1")
        .bind(windowStart - 10 * MINUTE_MS),
    ]);

    const row = results && results[0] && results[0].results && results[0].results[0];
    const used = row && typeof row.used === "number" ? row.used : null;
    if (used === null) {
      console.warn("[rate-limit] llm window returned an unexpected shape");
      return { allowed: true, limit, used: null, degraded: "unexpected-result" };
    }
    if (used > limit) {
      return { allowed: false, limit, used, retryAfterSeconds: windowEndsIn };
    }
    return { allowed: true, limit, used };
  } catch (e) {
    console.warn("[rate-limit] llm limiter failed open: " + (e && e.message));
    return { allowed: true, limit, used: null, degraded: "error" };
  }
}

/**
 * Decide whether this IP may submit an RFQ.
 *
 * Two independent rules, both per IP hash:
 *   - more than `rfqPerWindow` submissions inside the rolling window, or
 *   - more than `rfqTotalPerIp` submissions ever.
 *
 * Pure read — the caller records the submission only after it actually goes
 * through, so a typo'd form does not eat into the sender's allowance.
 */
export async function checkRfqLimit(env, ipHash) {
  const cfg = rateLimits(env);
  const windowMs = cfg.rfqWindowMinutes * MINUTE_MS;
  const db = env && env.RATE_LIMIT_DB;
  if (!db) return { allowed: true, degraded: "no-binding" };

  const now = Date.now();
  try {
    const windowRow = await db
      .prepare(
        "SELECT COUNT(*) AS n, MIN(ts) AS oldest FROM rfq_events WHERE ip_hash = ?1 AND ts > ?2"
      )
      .bind(ipHash, now - windowMs)
      .first();
    const inWindow = (windowRow && windowRow.n) || 0;

    if (inWindow >= cfg.rfqPerWindow) {
      const oldest = (windowRow && windowRow.oldest) || now;
      const freesIn = Math.max(1, Math.ceil((oldest + windowMs - now) / 1000));
      return {
        allowed: false,
        reason: "window",
        inWindow,
        perWindow: cfg.rfqPerWindow,
        windowMinutes: cfg.rfqWindowMinutes,
        retryAfterSeconds: freesIn,
      };
    }

    const totalRow = await db
      .prepare("SELECT COUNT(*) AS n FROM rfq_events WHERE ip_hash = ?1")
      .bind(ipHash)
      .first();
    const total = (totalRow && totalRow.n) || 0;

    if (total >= cfg.rfqTotalPerIp) {
      return { allowed: false, reason: "total", total, totalPerIp: cfg.rfqTotalPerIp };
    }

    return { allowed: true, inWindow, total };
  } catch (e) {
    console.warn("[rate-limit] rfq limiter failed open: " + (e && e.message));
    return { allowed: true, degraded: "error" };
  }
}

/** Record an accepted RFQ against the sender's IP hash. */
export async function recordRfq(env, ipHash) {
  const db = env && env.RATE_LIMIT_DB;
  if (!db) return;
  try {
    await db
      .prepare("INSERT INTO rfq_events (ip_hash, ts) VALUES (?1, ?2)")
      .bind(ipHash, Date.now())
      .run();
  } catch (e) {
    // The inquiry is already on its way; a bookkeeping failure is not worth
    // failing the request over.
    console.warn("[rate-limit] could not record rfq: " + (e && e.message));
  }
}

/**
 * Stable pseudonym for the caller's IP.
 *
 * The raw address is never stored — only a salted SHA-256 digest, which is all
 * the counting logic needs. The salt keeps the digests from being reversible
 * back to an address by brute force (IPv4 has far too few values to resist an
 * unsalted hash).
 */
export async function clientIpHash(env, request) {
  const header =
    request.headers.get("CF-Connecting-IP") ||
    request.headers.get("X-Forwarded-For") ||
    "";
  const ip = header.split(",")[0].trim();
  if (!ip) return "unknown";

  const salt =
    (env && (env.RATE_LIMIT_SALT || env.GITHUB_OAUTH_SECRET)) || "sapu-rate-limit";
  const bytes = new TextEncoder().encode(salt + "|" + ip);
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return [...new Uint8Array(digest)]
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("")
    .slice(0, 32);
}

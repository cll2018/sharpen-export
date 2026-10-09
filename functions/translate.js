// Cloudflare Pages Function: POST /translate
// Translates one content item (news article or product) for the "publish in all
// languages" page at /admin/publish.html.
//
// Design notes:
//  - Security mirrors functions/ai-chat.js: non-secret config (apiBaseUrl / model)
//    lives in data/settings.json, the secret key is read from the Pages env var
//    AI_LLM_API_KEY and never leaves the server. Same-origin POSTs only, with a
//    payload cap, so it cannot be abused as an open translation proxy.
//  - MODE "all" (preferred): translates into every target language in ONE upstream
//    request. The configured provider rate-limits by request count, so 13
//    separate calls frequently fail with 502; a single call avoids that entirely.
//  - MODE "single": one language per request, used as a fallback to fill in any
//    language the combined response missed.
//
// Security model (mirrors functions/ai-chat.js):
//   - Non-secret config (apiBaseUrl / model) lives in data/settings.json.
//   - The secret API key is read from the Cloudflare Pages env var AI_LLM_API_KEY.
//   - Only same-origin POSTs with a bounded payload are accepted.
//   - Upstream calls draw on the shared per-minute budget in ./_lib/rate-limit.js.

import { takeLlmSlot } from "./_lib/rate-limit.js";

const MAX_BODY = 24_000; // chars of source text accepted

const LANG_NAMES = {
  en: "English (US)",
  zh: "Simplified Chinese",
  "zh-tw": "Traditional Chinese (Taiwan)",
  de: "German",
  ja: "Japanese",
  ko: "Korean",
  ru: "Russian",
  es: "Spanish",
  pt: "Portuguese",
  fr: "French",
  it: "Italian",
  tr: "Turkish",
  ar: "Arabic",
  vi: "Vietnamese",
};

// Established product terminology for this site. Translating these words with a
// generic dictionary produces bad results (e.g. 金刚石砂轮 -> "diamond paste"),
// so the required renderings are pinned here and echoed back in the prompt.
//
// The canonical copy now lives in data/translation-glossary.json so that this
// Function and scripts/i18n-sync.mjs (the GitHub Action that syncs zh -> the
// other 13 languages) always use identical wording. What follows is the
// built-in fallback, used if that file cannot be fetched at runtime.
const GLOSSARY_FALLBACK = [
  ["萨普新材", "Sharpen New Materials", "Sharpen New Materials", "サプ新材", "사프신재", "SAP New Materials", "Sharpen New Materials", "Sharpen New Materials", "Sharpen New Materials", "Sharpen New Materials", "Sharpen New Materials", "سابو للمواد الجديدة", "Sharpen New Materials"],
  ["长沙市萨普新材料有限公司", "Changsha Sharpen New Materials Co., Ltd.", "Changsha Sharpen New Materials Co., Ltd.", "長沙サプ新材料有限公司", "창사 사프 신소재 유한회사", "ООО «Чанша Сап Новые Материалы»", "Changsha Sharpen New Materials Co., Ltd.", "Changsha Sharpen New Materials Co., Ltd.", "Changsha Sharpen New Materials Co., Ltd.", "Changsha Sharpen New Materials Co., Ltd.", "Changsha Sharpen New Materials Co., Ltd.", "تشانغشا سابو للمواد الجديدة المحدودة", "Changsha Sharpen New Materials Co., Ltd."],
  ["金刚石砂轮", "diamond grinding wheel", "Diamantscheibe", "ダイヤモンド砥石", "다이아몬드 휠", "алмазный круг", "rueda de diamante", "roda de diamante", "meule diamant", "mole per diamante", "elmas taş", "قرص الماس", "đĩa mài kim cương"],
  ["CBN砂轮", "CBN grinding wheel", "CBN-Schleifscheibe", "CBN砥石", "CBN 휠", "CBN круг", "rueda CBN", "roda CBN", "meule CBN", "mole CBN", "CBN taş", "قرص CBN", "đĩa mài CBN"],
  ["硬质合金", "cemented carbide", "Hartmetall", "超硬合金", "탄화강", "твердосплав", "carburo", "carboneto", "carbure", "carburo", "sert metal", "كربيد", "carbide cứng"],
  ["金属陶瓷结合剂", "cermet bond", "Keramikmetallbindung", "セラミックメタルバインド", "서멧 결합제", "керамико-металлическая связка", "aglutinante cermet", "aglutinante cermet", "liant cermet", "legante cermet", "seramik metal bağlayıcı", "رابطة سيرميت", "chất kết dính cermet"],
  ["树脂结合剂", "resin bond", "Kunstharzbindung", "樹脂バインド", "수지 결합제", "смоляная связка", "aglutinante de resina", "aglutinante de resina", "liant résine", "legante resinosa", "reçine bağlayıcı", "رابط راتنجي", "chất kết dính nhựa"],
  ["碳化硅晶圆减薄砂轮", "SiC wafer thinning wheel", "SiC-Wafer-Dünnschliff", "SiCウェーハ研削", "SiC 웨이퍼 씬닝", "SiC пластины", "rueda de adelgazado de obleas SiC", "roda de desbaste de wafer SiC", "meule d'amincissement de wafer SiC", "mola di assottigliamento wafer SiC", "SiC wafer inceltme", "عجلة ترقيم رقائق SiC", "đĩa mài mỏng wafer SiC"],
  ["粉末冶金高速钢", "powder metallurgy high-speed steel", "Pulvermetallurgie-Schnellstahl", "粉末冶金高速度鋼", "분말야금 고속강", "порошковая быстрорежущая сталь", "acero rápido de metalurgia de polvos", "aço rápido de metalurgia de pó", "acier rapide à métallurgie des poudres", "acciaio rapido da metallurgia delle polveri", "toz metalurjisi yüksek hızlı çelik", "فولاذ عالي السرKata من المساحيق", "thép tốc độ cao luyện bột"],
  ["均热板", "heat spreader", "Wärmeleiter", "放熱板", "히트 스프리더", "радиатор", "disipador de calor", "dissipador de calor", "conducteur thermique", "dispersione di calore", "ısı yayıcı", "موصل حراري", "tản nhiệt"],
  ["五轴数控磨削", "five-axis CNC grinding", "5-Achs-CNC-Schliff", "5軸NC研削", "5축 CNC 연삭", "5-осевое фрезерование", "rectificado CNC de 5 ejes", "retificação CNC de 5 eixos", "rectification CNC 5 axes", "rettifica CNC a 5 assi", "5 eksenli CNC taşlama", "الطحن CNC بخمسة محاور", "mài CNC 5 trục"],
];

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "no-store",
    },
  });
}

/** Pull the first complete JSON object out of a model reply. */
function extractJson(text) {
  if (!text) return null;
  const fenced = text.match(/```(?:json)?\s*([\s\S]*?)```/i);
  const raw = (fenced ? fenced[1] : text).trim();
  try {
    return JSON.parse(raw);
  } catch {
    /* fall through to brace matching */
  }
  const start = raw.indexOf("{");
  if (start === -1) return null;
  let depth = 0, inStr = false, esc = false;
  for (let i = start; i < raw.length; i++) {
    const ch = raw[i];
    if (esc) { esc = false; continue; }
    if (ch === "\\") { esc = true; continue; }
    if (ch === '"') inStr = !inStr;
    if (inStr) continue;
    if (ch === "{") depth++;
    else if (ch === "}") {
      depth--;
      if (depth === 0) {
        try { return JSON.parse(raw.slice(start, i + 1)); } catch { return null; }
      }
    }
  }
  return null;
}

// Column order inside each glossary row: index 0 is the Chinese term, then
// en, de, ja, ko, ru, es, pt, fr, it, tr, ar, vi.
const GLOSSARY_LANGS = ["en", "de", "ja", "ko", "ru", "es", "pt", "fr", "it", "tr", "ar", "vi"];

/** Load the shared glossary; fall back to the table above if it is unavailable. */
async function loadGlossary(origin) {
  try {
    const res = await fetch(new URL(origin + "/data/translation-glossary.json"));
    if (!res.ok) return null;
    const data = await res.json();
    if (data && Array.isArray(data.glossary) && data.glossary.length) return data;
  } catch {
    /* keep the built-in fallback */
  }
  return null;
}

function glossaryBlock(sourceLang, data) {
  const rows = (data && data.glossary) || GLOSSARY_FALLBACK;
  const langs = (data && data.glossaryLangs) || GLOSSARY_LANGS;
  const extra = (data && data.glossaryExtra) || {};
  const lines = [];
  for (const row of rows) {
    const zh = row[0];
    const targets = [];
    for (let i = 0; i < langs.length; i++) {
      const code = langs[i];
      if (code === sourceLang) continue;
      targets.push(LANG_NAMES[code] + " = " + row[i + 1]);
    }
    for (const code of Object.keys(extra[zh] || {})) {
      if (code === sourceLang) continue;
      targets.push(LANG_NAMES[code] + " = " + extra[zh][code]);
    }
    lines.push("- " + zh + " → " + targets.join("; "));
  }
  return lines.join("\n");
}

function fidelityRules(sourceLang, glossary) {
  return [
    "- TRANSLATE FAITHFULLY AND LITERALLY. Do not add, remove, summarize, explain, embellish or comment. Do not invent facts, dates, numbers, adjectives or product claims.",
    "- Do NOT add adjectives, qualifiers or details that are not present in the source (e.g. if the source says \"new grinding wheel\", do not write \"new ultra-thin large-sized wheel\").",
    "- Translate every word, but add no words. If a technical term has a pinned rendering below, use exactly that rendering.",
    "- Keep every number, date, unit, model name and proper noun exactly as written in the source.",
    "- Keep all HTML tags, markdown syntax and entities exactly as they are; translate only the human-readable text between them.",
    "- Keep template expressions such as {{ site.email }} exactly as written; never translate, rename or drop them.",
    "- Keep the tone of a professional industrial-manufacturing B2B website.",
    "- Use the pinned terminology below for these industry terms, so that the wording matches the rest of the website:",
    glossaryBlock(sourceLang, glossary),
  ].join("\n");
}

function sourcePayload(kind, item) {
  const p = { title: item.title || "", description: item.description || "" };
  if (kind === "product") p.features = Array.isArray(item.features) ? item.features : [];
  else p.body = item.body || "";
  if (kind === "news" && item.section) p.section_label_to_translate = item.section;
  return p;
}

function buildAllPrompt(kind, sourceLang, item, targets, glossary) {
  const perLang = kind === "product"
    ? '"title": "...", "description": "...", "features": ["...", "..."]'
    : '"title": "...", "description": "...", "body": "..."' + (item.section ? ', "section": "..."' : "");
  return [
    `Translate this ${kind === "product" ? "product entry" : "news article"} from ${LANG_NAMES[sourceLang] || sourceLang} into these ${targets.length} languages: ` +
      targets.map((c) => `${c} (${LANG_NAMES[c]})`).join(", ") + ".",
    "",
    fidelityRules(sourceLang, glossary),
    kind === "product"
      ? '- "features" is a list of short bullets: translate each bullet separately and return exactly the same number of bullets.'
      : '- "body" may contain HTML (<p>, <ul>, <li>, <strong>): keep the tags, translate only the text.' +
        (item.section ? ' Also translate the news section label and return it as "section".' : ""),
    "",
    "Reply with ONLY a JSON object mapping each language code to its translation, no prose and no code fence:",
    '{ "' + targets[0] + '": { ' + perLang + ' }, "' + targets[targets.length - 1] + '": { ' + perLang + ' }, ... }',
    "",
    "SOURCE JSON:",
    JSON.stringify(sourcePayload(kind, item), null, 1),
  ].join("\n");
}

function buildOnePrompt(kind, sourceLang, item, target, glossary) {
  const perLang = kind === "product"
    ? '"title": "...", "description": "...", "features": ["...", "..."]'
    : '"title": "...", "description": "...", "body": "..."' + (item.section ? ', "section": "..."' : "");
  return [
    `Translate this ${kind === "product" ? "product entry" : "news article"} from ${LANG_NAMES[sourceLang] || sourceLang} into ${LANG_NAMES[target] || target}.`,
    "",
    fidelityRules(sourceLang, glossary),
    kind === "product"
      ? '- "features" is a list of short bullets: translate each bullet separately and return exactly the same number of bullets.'
      : '- "body" may contain HTML (<p>, <ul>, <li>, <strong>): keep the tags, translate only the text.' +
        (item.section ? ' Also translate the news section label and return it as "section".' : ""),
    "",
    "Reply with ONLY a JSON object, no prose and no code fence: { " + perLang + " }",
    "",
    "SOURCE JSON:",
    JSON.stringify(sourcePayload(kind, item), null, 1),
  ].join("\n");
}

async function callModel(settings, apiKey, prompt, maxTokens, env) {
  // Every upstream request draws on the shared 20-per-minute budget, INCLUDING
  // the retries below. That is the point: the provider's limit is per API key,
  // not per user request, so a retry storm is exactly what trips the 429.
  const slot = await takeLlmSlot(env);
  if (!slot.allowed) {
    const err = new Error(
      "上游接口本分钟调用额度已用完（上限 " +
        slot.limit +
        " 次/分钟），约 " +
        slot.retryAfterSeconds +
        " 秒后自动恢复，请稍后再试。"
    );
    // Retrying immediately cannot help; the window has to roll over first.
    err.retryable = false;
    err.budgetExhausted = true;
    throw err;
  }

  const upstream = await fetch((settings.apiBaseUrl || "").replace(/\/$/, "") + "/chat/completions", {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: "Bearer " + apiKey },
    body: JSON.stringify({
      model: settings.model || "gpt-4o-mini",
      temperature: 0.1,
      max_tokens: maxTokens || 4000,
      messages: [
        {
          role: "system",
          content:
            "You are a meticulous technical translator for a Chinese industrial manufacturer " +
            "(grinding wheels, CBN wheels, cemented carbide, PM high-speed steel, SiC wafer " +
            "grinding, TiNiCo heat spreaders). You translate literally and faithfully: you " +
            "translate every word, add no words, drop no words, and never add adjectives, " +
            "qualifiers, numbers or product details that are not in the source. You always " +
            "answer with a single valid JSON object and nothing else.",
        },
        { role: "user", content: prompt },
      ],
    }),
  });
  if (!upstream.ok) {
    // Surface WHY. The provider explains a rate limit in the response body, and
    // without it every failure reaches the operator as an identical opaque error.
    let detail = "";
    try {
      detail = (await upstream.text()).replace(/\s+/g, " ").trim().slice(0, 240);
    } catch {
      /* an unreadable body still leaves us the status code */
    }
    const err = new Error(
      "LLM HTTP " + upstream.status + (detail ? " — " + detail : "")
    );
    err.retryable = true;
    err.status = upstream.status;
    const retryAfter = Number(upstream.headers.get("retry-after"));
    if (Number.isFinite(retryAfter) && retryAfter > 0) {
      err.retryAfterMs = Math.min(retryAfter * 1000, 8000);
    } else if (upstream.status === 429) {
      // No hint from the provider: back off hard instead of hammering a quota
      // that is already exhausted — retrying fast is what turns one 429 into a
      // storm of them, which is exactly how this endpoint used to fail.
      err.retryAfterMs = 6000;
    }
    throw err;
  }
  const data = await upstream.json();
  const content = data.choices && data.choices[0] && data.choices[0].message
    ? data.choices[0].message.content
    : "";
  const parsed = extractJson(content);
  if (!parsed) {
    const err = new Error("model reply was not valid JSON");
    err.retryable = true;
    throw err;
  }
  return parsed;
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/**
 * How long to wait before the next attempt. The provider rate-limits by request
 * count and may state a Retry-After; when it does, waiting that long is the only
 * thing that actually helps. Otherwise fall back to a plain backoff.
 */
function retryDelay(err, fallbackMs) {
  const hinted = err && err.retryAfterMs;
  return hinted > 0 ? hinted : fallbackMs;
}

/**
 * Application failures are reported as HTTP 200 with `ok:false` on purpose.
 * This zone has origin_error_page_pass_thru=off, so Cloudflare swaps any 5xx
 * body coming back from Pages for its own "502 Bad gateway" page — the operator
 * then only ever sees "HTTP 502" instead of the real reason. A 200 that carries
 * ok:false is the only shape that survives all the way to the admin screen.
 * The admin page already treats `!res.ok || !data.ok` as a failure.
 */
function fail(error, extra) {
  return json(Object.assign({ ok: false, error }, extra || {}), 200);
}

function pickLang(raw, kind, item, fallbackSection) {
  const out = {
    title: String((raw && raw.title) || ""),
    description: String((raw && raw.description) || ""),
  };
  if (!out.title) return null;
  if (kind === "product") {
    out.features = Array.isArray(raw.features) ? raw.features.map(String) : [];
  } else {
    out.body = String((raw && raw.body) || "");
    if (fallbackSection) out.section = String(raw.section || fallbackSection);
  }
  return out;
}

export async function onRequestPost({ request, env }) {
  // Same-origin (first-party) only: this Function translates content for our own
  // admin page. A MISSING Origin used to be waved through, which left this
  // endpoint as an open translation proxy for anyone with an HTTP client — and
  // the LLM key behind it has a tight request quota, so abuse surfaces as
  // site-wide 429s.
  //
  // The check still blocks genuinely cross-origin callers, but it now accepts
  // every first-party host instead of requiring an exact substring match:
  //   - the request host itself (www.sapu-cn.online),
  //   - the apex domain (sapu-cn.online) and any of its subdomains,
  //   - *.pages.dev preview deployments.
  // The previous `origin.includes(host)` 403'd the admin whenever it was opened
  // from the apex domain or a preview build, which made "一键发布" fail with a
  // opaque cross-origin error even though the call was first-party.
  const origin = request.headers.get("Origin");
  const host = new URL(request.url).host;
  let originHost = "";
  try { originHost = origin ? new URL(origin).host : ""; } catch { originHost = ""; }
  const firstParty =
    originHost === host ||
    originHost === "sapu-cn.online" ||
    originHost.endsWith(".sapu-cn.online") ||
    originHost.endsWith(".pages.dev");
  if (!origin || !firstParty) {
    return json({ ok: false, error: "cross-origin requests are not allowed" }, 403);
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return json({ ok: false, error: "invalid JSON body" }, 400);
  }

  const kind = body.kind === "product" ? "product" : "news";
  const sourceLang = typeof body.sourceLang === "string" ? body.sourceLang : "zh";
  const item = {
    title: typeof body.title === "string" ? body.title : "",
    description: typeof body.description === "string" ? body.description : "",
    body: typeof body.body === "string" ? body.body : "",
    features: Array.isArray(body.features) ? body.features : [],
    section: typeof body.section === "string" ? body.section : "",
  };
  if (!item.title) return json({ ok: false, error: "title is required" }, 400);

  const sourceSize = item.title.length + item.description.length + item.body.length +
    item.features.join("").length;
  if (sourceSize > MAX_BODY) {
    return json(
      { ok: false, error: `source content is too long (${sourceSize} chars, limit ${MAX_BODY}). Shorten it or translate that language in the CMS.` },
      413
    );
  }

  const mode = body.mode === "single" ? "single" : "all";
  const requested = Array.isArray(body.langs) ? body.langs : (body.lang ? [body.lang] : []);
  const targets = [...new Set(requested)]
    .filter((c) => LANG_NAMES[c] && c !== sourceLang);
  if (!targets.length) return json({ ok: true, results: {} });

  let settings;
  try {
    settings = await fetch(new URL(request.url).origin + "/data/settings.json").then((r) => r.json());
  } catch {
    return fail("could not load data/settings.json");
  }
  // Shared terminology with scripts/i18n-sync.mjs; falls back to the inline
  // table inside this file when the JSON cannot be read.
  const glossary = await loadGlossary(new URL(request.url).origin);
  const apiKey = env.AI_LLM_API_KEY;
  if (!apiKey) {
    return fail("AI_LLM_API_KEY is not set on this Cloudflare Pages project");
  }

  const results = {};
  const errors = {};

  if (mode === "all") {
    const prompt = buildAllPrompt(kind, sourceLang, item, targets, glossary);
    const maxTokens = Math.min(16000, 1200 + Math.ceil(sourceSize * 0.9 * targets.length / 2.2));
    let lastErr = "unknown error";
    let rateLimited = false;
    for (let attempt = 1; attempt <= 2; attempt++) {
      try {
        const parsed = await callModel(settings, apiKey, prompt, maxTokens, env);
        for (const lang of targets) {
          const picked = pickLang(parsed[lang], kind, item, item.section);
          if (picked) results[lang] = picked;
          else errors[lang] = "missing in combined response";
        }
        if (Object.keys(results).length) break;
        lastErr = "combined response had no usable entries";
      } catch (e) {
        lastErr = String(e && e.message ? e.message : e).slice(0, 240);
        console.warn("[translate] mode=all attempt " + attempt + " failed: " + lastErr);
        if (e && (e.budgetExhausted || e.status === 429)) rateLimited = true;
        if (e && e.retryable === false) break;
        if (attempt < 2) await sleep(retryDelay(e, 1500));
      }
    }
    if (!Object.keys(results).length) {
      return fail(lastErr, { mode, languages: targets.length, rateLimited });
    }
  } else {
    const lang = targets[0];
    let lastErr = "unknown error";
    let rateLimited = false;
    for (let attempt = 1; attempt <= 3; attempt++) {
      try {
        const parsed = await callModel(settings, apiKey, buildOnePrompt(kind, sourceLang, item, lang, glossary), 4000, env);
        const picked = pickLang(parsed, kind, item, item.section);
        if (picked) {
          results[lang] = picked;
          lastErr = "";
          break;
        }
        lastErr = "reply had no title";
      } catch (e) {
        lastErr = String(e && e.message ? e.message : e).slice(0, 240);
        console.warn("[translate] mode=single lang=" + lang + " attempt " + attempt + " failed: " + lastErr);
        if (e && (e.budgetExhausted || e.status === 429)) rateLimited = true;
        if (e && e.retryable === false) break;
        // back off: the provider rate-limits by request count
        if (attempt < 3) await sleep(retryDelay(e, 2000 * attempt));
      }
    }
    if (!results[lang]) return fail(lastErr, { mode, lang, rateLimited });
  }

  return json({ ok: true, mode, results, errors });
}

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: { Allow: "POST, OPTIONS" } });
}

// Compute sitemap URL list + robots.txt content as build-time data so the
// Eleventy templates render them verbatim without hand-maintained dates.
const site = require("../_data/site.js");
const { execSync } = require("child_process");

// ISO build timestamp (diagnostics only — NOT a blanket sitemap lastmod).
const BUILD_TIME = new Date().toISOString().slice(0, 10);

// Per-page lastmod = date of the last git commit touching the page source
// file. A blanket build-date lastmod on every URL is ignored by Google,
// so report real dates and omit lastmod when it cannot be determined.
// Dates are collected with ONE git log pass (newest-first) and mapped to
// source files — 490 individual git calls would be far too slow.
function gitLastmods(relPaths) {
  const map = {};
  try {
    // No path filter: 490 quoted paths exceed the Windows command-line
    // length limit. The whole-repo log is small enough to parse fully;
    // unrelated files are simply never looked up in the map.
    const out = execSync(
      'git log --format="COMMIT%x09%cs" --name-only',
      { cwd: __dirname + "/..", stdio: ["ignore", "pipe", "ignore"], timeout: 120000, maxBuffer: 64 * 1024 * 1024 }
    ).toString();
    let cur = null;
    for (const line of out.split(/\r?\n/)) {
      const PREFIX = "COMMIT\t"; // C O M M I T \t == 7 chars
      if (line.indexOf(PREFIX) === 0) { cur = line.slice(PREFIX.length); continue; }
      const f = line.trim();
      if (f && !(f in map)) map[f] = cur; // first hit = newest commit
    }
  } catch (e) {
    /* no git available: every lastmod stays undefined and is omitted */
  }
  return map;
}

const DOMAIN = "https://" + site.domain;

// All 8 product images (same paths across every language) so the products
// page URL carries the full product image index for Google Images.
const PRODUCT_IMAGES = ((require("./products").en) || []).map((p) => p.image);

// Per-product detail-page slugs (single source of truth) + full product data
// so the sitemap can emit one URL per product per language.
const PRODUCT_SLUGS = require("./productSlugs.json");
const PRODUCTS_ALL = require("./products");

// All pages per language: home, products, about, news, contact.
// `images` is an array of image paths; the products page lists every product.
const PAGES = [
  { seg: "", priority: "1.0", changefreq: "weekly", images: ["/assets/img/logo.png"] },
  { seg: "products", priority: "0.9", changefreq: "weekly", images: PRODUCT_IMAGES },
  { seg: "about", priority: "0.7", changefreq: "monthly", images: ["/assets/img/pm-steel.webp"] },
  { seg: "news", priority: "0.7", changefreq: "daily", images: ["/assets/img/news-company.png"] },
  { seg: "contact", priority: "0.7", changefreq: "monthly", images: ["/assets/img/news-industry.png"] },
  { seg: "search", priority: "0.3", changefreq: "monthly", images: ["/assets/img/logo.png"] },
  { seg: "privacy", priority: "0.4", changefreq: "yearly", images: ["/assets/img/logo.png"] },
];

function pageUrl(lang, seg) {
  if (!seg) return "/" + lang + "/";
  return "/" + lang + "/" + seg + "/";
}

const urls = [];
for (const l of site.langs) {
  for (const p of PAGES) {
    const path = pageUrl(l.code, p.seg);
    urls.push({
      loc: DOMAIN + path,
      src: l.code + "/" + (p.seg ? p.seg : "index") + ".md",
      changefreq: p.changefreq,
      priority: p.priority,
      images: p.images.map((i) => DOMAIN + i),
      title: (l.native ? l.native + " " : "") + site.shortName + (p.seg ? " – " + p.seg : ""),
    });
  }
}

// Per-product detail pages: one URL per product per language, each carrying
// its own product photo for Google Images + the localized product name.
for (const l of site.langs) {
  const plist = PRODUCTS_ALL[l.code] || [];
  for (const p of plist) {
    const slug = PRODUCT_SLUGS[p.id];
    if (!slug) continue;
    urls.push({
      loc: DOMAIN + "/" + l.code + "/products/" + slug + "/",
      src: l.code + "/products/" + slug + ".md",
      changefreq: "weekly",
      priority: "0.8",
      images: [DOMAIN + p.image],
      title: (l.native ? l.native + " " : "") + p.name + " – " + site.shortName,
    });
  }
}

// Per-article news detail pages — every language now carries a hand-written
// body (21 articles each), and newsSlugs.json holds the localized title for
// all 14 languages, so we emit one URL per article per language.
const NEWS_SLUGS = require("./newsSlugs.json");
const NEWS_LANGS = site.langs.map((l) => l.code);
for (const l of NEWS_LANGS) {
  for (const slug of Object.keys(NEWS_SLUGS)) {
    const title = NEWS_SLUGS[slug][l] || NEWS_SLUGS[slug].en;
    urls.push({
      loc: DOMAIN + "/" + l + "/news/" + slug + "/",
      src: l + "/news/" + slug + ".md",
      changefreq: "monthly",
      priority: "0.6",
      images: [DOMAIN + "/assets/img/logo.png"],
      title: (NEWS_SLUGS[slug] && NEWS_SLUGS[slug][l] ? NEWS_SLUGS[slug][l] : NEWS_SLUGS[slug].en) + " – " + site.shortName,
    });
  }
}

// Resolve lastmod dates with ONE batched git log pass now that every URL
// has been collected; pages without a resolvable date get no lastmod at
// all (honest) rather than a fake build-date.
const LASTMODS = gitLastmods(urls.map((u) => u.src));
for (const u of urls) {
  u.lastmod = LASTMODS[u.src] || null;
  delete u.src;
}
// robots.txt body (served at /robots.txt).
//
// Owner policy: allow EVERY crawler (search engines and AI/LLM agents) to read
// the public site. Only the Decap CMS admin UI is excluded from indexing.
//
// Why the previous "re-allow every agent" list did not fully work:
// robots.txt has no "last matching group wins" rule (RFC 9309 §2.2.1). When the
// same user-agent appears in more than one group, the groups are MERGED. So a
// Cloudflare-managed block that PREPENDS `User-agent: Baiduspider / Disallow: /`
// is not removed by a later `User-agent: Baiduspider / Allow: /`; the records
// are combined, and crawlers using first-match semantics (e.g. Baiduspider)
// stay blocked. The reliable fix is to turn OFF Cloudflare's managed robots.txt
// (Security Settings > Bot traffic > "Set your preference to block training in
// robots.txt"); this file is then served verbatim. The explicit allow group
// below is kept as a defensive override for spec-compliant crawlers meanwhile.
const CRAWLERS = [
  // Chinese-market search engines (owner wants Baidu/360/Sogou indexation)
  "Baiduspider", "360bot", "Sogou", "PetalBot",
  // Major search / social crawlers
  "Googlebot", "Bingbot", "YandexBot", "Applebot", "DuckDuckBot", "BraveBot",
  "SemrushBot", "AhrefsBot", "MojeekBot", "Qwant", "Naver",
  // AI training / agent crawlers that Cloudflare blocks by default — we allow
  "Amazonbot", "Applebot-Extended", "Bytespider", "CCBot", "ClaudeBot",
  "Diffbot", "Google-Extended", "GPTBot", "omgili", "anthropic-ai",
  "Claude-Web", "cohere-ai", "MistralAI-Training", "meta-externalagent",
  "GoogleOther", "Google-Agent", "meta-externalfetcher",
  "Perplexity-User", "FireCrawl", "FirecrawlAgent", "KimiBot", "Kimi-User",
  "Amazon-User", "Amzn-User", "Retool", "Instapaper", "ChathiveCrawler",
  "HuggingCrawler", "Cotoyogi", "ICC-Crawler", "atlassian-bot",
  "FishBot", "BorderxBot", "NavuBot", "SemrushBot-SWA", "WARDBot",
  "magpie-crawler", "CitibotSiteCrawler", "AwarioSmartBot",
  "AwarioRssBot", "Google-CloudVertexBot", "QualifiedBot",
];

const robots = [
  "User-agent: *",
  "Allow: /",
  "Disallow: /admin/",
  "Content-Signal: search=yes,ai-train=yes,use=reference",
  "",
  "# Explicit allow for crawlers Cloudflare's managed robots.txt may disallow.",
  "# One group with many User-agent lines (valid per RFC 9309) replaces the",
  "# previous one-group-per-agent form, which duplicated several agent names.",
]
  .concat(CRAWLERS.map((ua) => "User-agent: " + ua))
  .concat([
    "Allow: /",
    "Disallow: /admin/",
    "",
    "Sitemap: " + DOMAIN + "/sitemap.xml",
  ])
  .join("\n");

module.exports = { sitemap: urls, robots, buildTime: BUILD_TIME, domain: DOMAIN };

// Compute sitemap URL list + robots.txt content as build-time data so the
// Eleventy templates render them verbatim without hand-maintained dates.
const site = require("../_data/site.js");

// ISO build timestamp (used for sitemap lastmod).
const BUILD_TIME = new Date().toISOString().slice(0, 10);

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
  { seg: "about", priority: "0.7", changefreq: "monthly", images: ["/assets/img/pm-steel.jpg"] },
  { seg: "news", priority: "0.7", changefreq: "daily", images: ["/assets/img/news-company.png"] },
  { seg: "contact", priority: "0.7", changefreq: "monthly", images: ["/assets/img/news-industry.png"] },
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
      lastmod: BUILD_TIME,
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
      lastmod: BUILD_TIME,
      changefreq: "weekly",
      priority: "0.8",
      images: [DOMAIN + p.image],
      title: (l.native ? l.native + " " : "") + p.name + " – " + site.shortName,
    });
  }
}

// robots.txt body (served at /robots.txt).
// NOTE: Cloudflare's managed robots appends a block that Disallow `/` for many
// AI crawlers (GPTBot, ClaudeBot, Bytespider, PetalBot, KimiBot, CCBot,
// Amazonbot, Applebot-Extended, Diffbot, Google-Extended, GoogleOther,
// ommgili, anthropic-ai, cohere-ai, MistralAI-*, meta-external*, qualified-bot,
// semrush, firecrawl, perplexity, hugging, cohere, etc.) AND for Baiduspider.
//
// The owner wants ALL of these to freely crawl the public site, so after the
// Cloudflare block we re-allow every one of them explicitly. robots.txt rule:
// an agent's own User-agent block wins over the wildcard `*`, and the LAST
// block for a given agent wins, so these override Cloudflare's Disallow.
// Only /admin/ stays blocked (the Decap CMS login UI is not public).
//
// The Cloudflare robots section lists these exact agent strings; we mirror it.
const CRAWLERS = [
  // Chinese-market search engines (owner wants Baidu/360/Sogou indexation)
  "Baiduspider", "360bot", "Sogou",
  // Major search / social crawlers
  "Googlebot", "Bingbot", "YandexBot", "Applebot", "DuckDuckBot", "BraveBot",
  "SemrushBot", "AhrefsBot", "DuckDuckBot", "MojeekBot",
  // AI training / agent crawlers that Cloudflare blocks by default — we allow
  "Amazonbot", "Applebot-Extended", "Bytespider", "CCBot", "ClaudeBot",
  "Diffbot", "Google-Extended", "GPTBot", "omgili", "anthropic-ai",
  "Claude-Web", "cohere-ai", "MistralAI-Training", "meta-externalagent",
  "GoogleOther", "Google-Agent", "meta-externalfetcher",
  "Perplexity-User", "FireCrawl", "FirecrawlAgent", "KimiBot", "Kimi-User",
  "Amazon-User", "Amzn-User", "Retool", "Instapaper", "ChathiveCrawler",
  "HuggingCrawler", "cohere-ai", "Cotoyogi", "ICC-Crawler", "atlassian-bot",
  "FishBot", "BorderxBot", "NavuBot", "SemrushBot-SWA", "WARDBot",
  "magpie-crawler", "CitibotSiteCrawler", "PetallBot", "AwarioSmartBot",
  "AwarioRssBot", "Google-CloudVertexBot", "QualifiedBot", "Qwant", "Naver",
];

const robots = [
  "User-agent: *",
  "Allow: /",
  "# Block only the Decap CMS admin from being indexed",
  "Disallow: /admin/",
  "",
  "# --- AI / LLM content signals (owner wants AI to freely read & use the site) ---",
  "# Cloudflare's managed robots defaults these to no; we override to yes so",
  "# search AI (Perplexity/ChatGPT) and training crawlers can all use the content.",
  "Content-Signal: search=yes,ai-train=yes,use=reference",
  "# llms.txt is served at /llms.txt — plain-language AI-readable index",
  "Sitemap: " + DOMAIN + "/llms.txt",
  "Sitemap: " + DOMAIN + "/sitemap.xml",
  "",
  "# Owner policy: explicitly ALLOW every public crawler (incl. AI agents)",
  "# so nothing is blocked by Cloudflare's managed-robots. Per-agent blocks",
  "# below win over Cloudflare's Disallow for the same agent.",
].concat(
  CRAWLERS.flatMap((ua) => [
    "User-agent: " + ua,
    "Allow: /",
    "Disallow: /admin/",
    "",
  ])
).concat([
  "# Catch-all for any crawler not explicitly listed above:",
  "# allow it but keep the Decap CMS admin out of the index.",
  "User-agent: *",
  "Allow: /",
  "Disallow: /admin/",
  "Content-Signal: search=yes,ai-train=yes,use=reference",
  "",
  "Sitemap: " + DOMAIN + "/sitemap.xml",
  "Sitemap: " + DOMAIN + "/llms.txt",
]).join("\n");

module.exports = { sitemap: urls, robots, buildTime: BUILD_TIME, domain: DOMAIN };

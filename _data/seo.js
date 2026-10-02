// Compute sitemap URL list + robots.txt content as build-time data so the
// Eleventy templates render them verbatim without hand-maintained dates.
const site = require("../_data/site.js");

// ISO build timestamp (used for sitemap lastmod).
const BUILD_TIME = new Date().toISOString().slice(0, 10);

// All pages per language: home, products, about, news, contact.
const PAGES = [
  { seg: "", priority: "1.0", changefreq: "weekly", image: "/assets/img/logo.png" },
  { seg: "products", priority: "0.9", changefreq: "weekly", image: "/assets/img/diamond-wheels.jpg" },
  { seg: "about", priority: "0.7", changefreq: "monthly", image: "/assets/img/pm-steel.jpg" },
  { seg: "news", priority: "0.7", changefreq: "daily", image: "/assets/img/news-company.png" },
  { seg: "contact", priority: "0.7", changefreq: "monthly", image: "/assets/img/news-industry.png" },
];

const DOMAIN = "https://" + site.domain;

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
      image: DOMAIN + p.image,
      title: (l.native ? l.native + " " : "") + site.shortName + (p.seg ? " – " + p.seg : ""),
    });
  }
}

// robots.txt body (served at /robots.txt).
// NOTE: Cloudflare's managed robots appends a block that Disallow `/` for many
// AI crawlers AND for Baiduspider. Our site explicitly wants Baidu / 360 /
// Sogou to index (Chinese-market SEO), so we add per-agent Allow rules after
// the cloudflare block. robots.txt is order-insensitive per agent block, and
// an agent's own rules override the wildcard, so these win for those agents.
const robots = [
  "User-agent: *",
  "Allow: /",
  "# Block the Decap CMS admin from being indexed",
  "Disallow: /admin/",
  "",
  "# Explicitly allow Chinese-market search crawlers (overrides any Cloudflare",
  "# managed-robots Disallow for these agents).",
  "User-agent: Baiduspider",
  "Allow: /",
  "User-agent: 360bot",
  "Allow: /",
  "User-agent: Sogou",
  "Allow: /",
  "",
  "Sitemap: " + DOMAIN + "/sitemap.xml",
].join("\n");

module.exports = { sitemap: urls, robots, buildTime: BUILD_TIME, domain: DOMAIN };

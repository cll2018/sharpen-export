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
const robots = [
  "User-agent: *",
  "Allow: /",
  "# Block the Decap CMS admin from being indexed",
  "Disallow: /admin/",
  "",
  "Sitemap: " + DOMAIN + "/sitemap.xml",
].join("\n");

module.exports = { sitemap: urls, robots, buildTime: BUILD_TIME, domain: DOMAIN };

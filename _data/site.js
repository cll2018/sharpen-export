// Site-wide configuration now lives in data/site.json so the CMS collections
// "站点信息 / Site Info" can edit brand, contact details, navigation, footer
// and per-language brand strings. This file stays as a thin loader so
// .eleventy.js filters, seo.js and the templates keep importing the same shape.
module.exports = require("../data/site.json");

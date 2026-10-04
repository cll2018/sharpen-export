// UI strings (home sections, buttons, search page labels) now live in
// data/i18n.json so the CMS collection "界面文案 / UI Strings" can edit them.
// This file stays as a thin loader so templates keep doing `i18n[lang]`.
module.exports = require("../data/i18n.json");

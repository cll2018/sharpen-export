// ---------------------------------------------------------------------------
// Site-wide configuration. Fill in the placeholders before going live.
// These values drive the header, footer, language switcher, WhatsApp button,
// Tawk.to script, AI chat widget and the RFQ form.
// ---------------------------------------------------------------------------

// Language set, derived from the product -> market fit (see README).
// `dir` is "rtl" for Arabic. Add/remove a row to change the site languages.
// zh-tw (Traditional Chinese) was added on request; geo auto-adaptation lives in
// root.njk (reads /cdn-cgi/trace -> country -> language).
const langs = [
  { code: "en", native: "English",        dir: "ltr", market: "Global B2B lingua franca" },
  { code: "zh", native: "简体中文",       dir: "ltr", market: "Domestic + Greater China" },
  { code: "zh-tw", native: "繁體中文",    dir: "ltr", market: "Taiwan, Hong Kong, Macau, overseas Chinese" },
  { code: "de", native: "Deutsch",        dir: "ltr", market: "Precision tooling / semiconductors (DE, AT, CH)" },
  { code: "ja", native: "日本語",         dir: "ltr", market: "Advanced ceramics / sapphire / semiconductors" },
  { code: "ko", native: "한국어",         dir: "ltr", market: "Semiconductors / LEDs / displays" },
  { code: "ru", native: "Русский",        dir: "ltr", market: "Machinery / metallurgy / tooling" },
  { code: "es", native: "Español",        dir: "ltr", market: "Spain + Latin America manufacturing" },
  { code: "pt", native: "Português",      dir: "ltr", market: "Brazil manufacturing / mining / automotive" },
  { code: "fr", native: "Français",        dir: "ltr", market: "France aerospace / precision mechanics" },
  { code: "it", native: "Italiano",        dir: "ltr", market: "Machine tools / ceramics / automotive" },
  { code: "tr", native: "Türkçe",          dir: "ltr", market: "Growing industrial hub (EU<->Asia bridge)" },
  { code: "ar", native: "العربية",         dir: "rtl", market: "Middle East manufacturing / oil & gas tooling" },
  { code: "vi", native: "Tiếng Việt",      dir: "ltr", market: "Electronics assembly / semiconductor emerging" },
];

module.exports = {
  // --- Brand -------------------------------------------------------------
  name: "Changsha Sharpen New Materials Co., Ltd.",
  nameZh: "长沙市萨普新材料有限公司",
  shortName: "Sharpen",
  domain: "sapu-cn.online", // used for canonical / hreflang absolute URLs
  logo: "/assets/img/logo.png",
  defaultLang: "en",
  fallbackLang: "en",

  // --- Languages (see table above) --------------------------------------
  langs,

  // --- Contact (shown in footer + RFQ form defaults) ---------------------
  email: "changliangliang@sapu-cn.online",
  phone: "+86-731-82225958",
  wechat: "sapu2023", // WeChat ID
  whatsapp: "8618656871390", // digits only, e.g. 8613800000000 (no +)
  address: "No. 68, Zhuyun Road, Yuelu District, Changsha, Hunan, China",
  addressZh: "中国湖南省长沙市岳麓区竹韵路68号",

  // --- Real-time inquiry -------------------------------------------------
  // 1) Tawk.to live chat — RECEIVE visitor messages in the Tawk dashboard /
  //    mobile app. Free. Get the Property ID from https://tawk.to and put it
  //    below (or edit it in the Decap CMS backend). When set, base.njk loads it.
  // Tawk.to live chat — RECEIVE visitor messages in the Tawk dashboard / mobile app.
  // Value is the full embed path "propertyId/widgetId" from your Tawk install snippet.
  tawkPropertyId: "6abf1e38b91309344d32ec0e/1k3t8s3es",
  // 2) Web3Forms: free, no-backend form-to-email. Get a key at
  //    https://web3forms.com and put it below; the RFQ form emails you.
  web3formsKey: "YOUR_WEB3FORMS_KEY",
  // 3) Built-in AI chat (primary auto-reply channel). Configuration lives in
  //    data/settings.json (editable in the Decap CMS backend); the secret API
  //    key lives in a Cloudflare Pages env var AI_LLM_API_KEY.
  aiChatPath: "/ai-chat",

  // --- Resources --------------------------------------------------------
  brochure: "/assets/img/brochure.pdf", // company brochure (migrated from old site)

  // --- Social / extras (optional) ---------------------------------------
  linkedin: "", // TODO: optional
  youtube: "",

  // --- Navigation (URLs per language; labels fall back to English) -------
  nav: [
    { key: "home",     en: "/en/",           zh: "/zh/",           "zh-tw": "/zh-tw/",           label: "Home",     zhLabel: "首页" },
    { key: "products", en: "/en/products/",  zh: "/zh/products/",  "zh-tw": "/zh-tw/products/",  label: "Products", zhLabel: "产品" },
    { key: "about",    en: "/en/about/",     zh: "/zh/about/",     "zh-tw": "/zh-tw/about/",     label: "About",    zhLabel: "关于我们" },
    { key: "news",     en: "/en/news/",      zh: "/zh/news/",      "zh-tw": "/zh-tw/news/",      label: "News",     zhLabel: "新闻" },
    { key: "contact",  en: "/en/contact/",   zh: "/zh/contact/",   "zh-tw": "/zh-tw/contact/",   label: "Contact",  zhLabel: "联系我们" },
  ],
};

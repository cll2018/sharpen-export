// ---------------------------------------------------------------------------
// Site-wide configuration. Fill in the placeholders before going live.
// These values drive the header, footer, language switcher, WhatsApp button,
// Tawk.to script, AI chat widget and the RFQ form.
// ---------------------------------------------------------------------------

// Language set, derived from the product -> market fit (see README).
// `dir` is "rtl" for Arabic. Add/remove a row to change the site languages.
const langs = [
  { code: "en", native: "English",    dir: "ltr", market: "Global B2B lingua franca" },
  { code: "zh", native: "中文",        dir: "ltr", market: "Domestic + Greater China" },
  { code: "de", native: "Deutsch",    dir: "ltr", market: "Precision tooling / semiconductors (DE, AT, CH)" },
  { code: "ja", native: "日本語",      dir: "ltr", market: "Advanced ceramics / sapphire / semiconductors" },
  { code: "ko", native: "한국어",      dir: "ltr", market: "Semiconductors / LEDs / displays" },
  { code: "ru", native: "Русский",    dir: "ltr", market: "Machinery / metallurgy / tooling" },
  { code: "es", native: "Español",    dir: "ltr", market: "Spain + Latin America manufacturing" },
  { code: "pt", native: "Português",  dir: "ltr", market: "Brazil manufacturing / mining / automotive" },
  { code: "fr", native: "Français",   dir: "ltr", market: "France aerospace / precision mechanics" },
  { code: "it", native: "Italiano",   dir: "ltr", market: "Machine tools / ceramics / automotive" },
  { code: "tr", native: "Türkçe",     dir: "ltr", market: "Growing industrial hub (EU<->Asia bridge)" },
  { code: "ar", native: "العربية",    dir: "rtl", market: "Middle East manufacturing / oil & gas tooling" },
  { code: "vi", native: "Tiếng Việt", dir: "ltr", market: "Electronics assembly / semiconductor emerging" },
];

module.exports = {
  // --- Brand -------------------------------------------------------------
  name: "Changsha Sharpen New Materials Co., Ltd.",
  nameZh: "长沙市萨普新材料有限公司",
  shortName: "Sharpen",
  domain: "sharpen-cn.com", // used for canonical / hreflang absolute URLs
  logo: "/assets/img/logo.png",
  defaultLang: "en",
  fallbackLang: "en",

  // --- Languages (see table above) --------------------------------------
  langs,

  // --- Contact (shown in footer + RFQ form defaults) ---------------------
  email: "changliangliang@sapu-cn.online",
  phone: "+86-731-82225958",
  wechat: "sapu2023", // WeChat ID
  whatsapp: "8613800000000", // TODO: digits only, e.g. 8613800000000 (no +)
  address:
    "No. xx, xx Road, Changsha High-Tech Zone, Hunan, China", // TODO: confirm
  addressZh: "中国湖南省长沙市高新区xx路xx号", // TODO: 确认

  // --- Real-time inquiry -------------------------------------------------
  // 1) Tawk.to live chat (optional secondary channel). Free. Get the Property
  //    ID from the embed snippet at https://tawk.to (looks like 64a1b2c3...).
  tawkPropertyId: "YOUR_TAWK_PROPERTY_ID",
  // 2) Web3Forms: free, no-backend form-to-email. Get a key at
  //    https://web3forms.com and put it below; the RFQ form emails you.
  web3formsKey: "YOUR_WEB3FORMS_KEY",
  // 3) Built-in AI chat (primary real-time channel). Configuration lives in
  //    data/settings.json (editable in the Decap CMS backend); the secret API
  //    key lives in a Cloudflare Pages env var AI_LLM_API_KEY.
  aiChatPath: "/ai-chat",

  // --- Social / extras (optional) ---------------------------------------
  linkedin: "", // TODO: optional
  youtube: "",

  // --- Navigation (URLs per language; labels fall back to English) -------
  nav: [
    { key: "home",     en: "/en/",           zh: "/zh/",           label: "Home",     zhLabel: "首页" },
    { key: "products", en: "/en/products/",  zh: "/zh/products/",  label: "Products", zhLabel: "产品" },
    { key: "about",    en: "/en/about/",     zh: "/zh/about/",     label: "About",    zhLabel: "关于我们" },
    { key: "contact",  en: "/en/contact/",   zh: "/zh/contact/",   label: "Contact",  zhLabel: "联系我们" },
  ],
};

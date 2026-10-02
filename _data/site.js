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
  nameZhTw: "長沙市薩普新材料有限公司",
  shortName: "Sharpen",
  domain: "www.sapu-cn.online", // used for canonical / hreflang absolute URLs (www is the served/301 target)
  logo: "/assets/img/logo.png",
  defaultLang: "en",
  fallbackLang: "en",

  // --- Localized brand / title (used for <title> suffix + per-page) -----
  // Each language gets its OWN company name so the title is not diluted by
  // the English "Changsha Sharpen New Materials Co., Ltd." (SEO issue).
  // `titleSuffix` is appended to the page title; `localDesc` is the
  // localized meta description fallback (used when a page has none).
  brandPerLang: {
    en:    { suffix: "Changsha Sharpen New Materials",      desc: "Diamond & CBN grinding wheels, PM high-speed steel, TiNiCo heat spreaders and SiC wafer thinning wheels — a global B2B manufacturer based in Changsha, China.", title: "Home" },
    zh:    { suffix: "长沙市萨普新材料",                      desc: "金刚石/CBN砂轮、粉末冶金高速钢、TiNiCo超合金均热板与碳化硅晶圆减薄砂轮，总部位于中国长沙的国家高新技术企业。", title: "首页" },
    "zh-tw":{ suffix: "長沙市薩普新材料",                     desc: "鑽石/CBN砂輪、粉末冶金高速鋼、TiNiCo超合金均熱板與碳化矽晶圓減薄砂輪，總部位於中國長沙。", title: "首頁" },
    de:    { suffix: "Changsha Sharpen Neue Werkstoffe",      desc: "Diamant- & CBN-Schleifscheiben, PM-HSS, TiNiCo-Wärmeleiter und SiC-Wafer-Dünnschliff — globaler B2B-Hersteller aus Changsha.", title: "Startseite" },
    ja:    { suffix: "長沙 Sharpen 新素材",                    desc: "ダイヤモンド/CBN砥石、粉末冶金高速度鋼、TiNiCo放熱板、SiCウェーハ研削。中国長沙のグローバルB2Bメーカー。", title: "ホーム" },
    ko:    { suffix: "장사 샤펜 신소재",                       desc: "다이아몬드·CBN 연마 휠, PM 고속강, TiNiCo 히트 스프리더, SiC 웨이퍼 씬닝 — 중국 장사의 글로벌 B2B 제조업체.", title: "홈" },
    ru:    { suffix: "Чанша Sharpen новые материалы",         desc: "Алмазные и CBN круги, ПМ БРС, TiNiCo радиаторы, круги для тонирования SiC-пластин — глобальный B2B-производитель из Чанша, Китай.", title: "Главная" },
    es:    { suffix: "Changsha Sharpen Nuevos Materiales",    desc: "Ruedas de diamante y CBN, acero rápido PM, disipadores TiNiCo y ruedas de delgado de obleas SiC — fabricante B2B global en Changsha, China.", title: "Inicio" },
    pt:    { suffix: "Changsha Sharpen Novos Materiais",      desc: "Roda de diamante e CBN, aço rápido PM, dissipador TiNiCo e roda de delgado de wafer SiC — fabricante B2B global de Changsha, China.", title: "Início" },
    fr:    { suffix: "Changsha Sharpen Nouveaux Matériaux",   desc: "Meules diamant et CBN, acier rapide PM, dissipateur TiNiCo, meules d'amincissement de wafer SiC — fabricant B2B mondial de Changsha, Chine.", title: "Accueil" },
    it:    { suffix: "Changsha Sharpen Nuovi Materiali",      desc: "Mole diamantate e CBN, acciaio rapido PM, dissipatore TiNiCo, mole di decapaggio wafer SiC — produttore B2B globale di Changsha, Cina.", title: "Home" },
    tr:    { suffix: "Changsha Sharpen Yeni Malzemeler",      desc: "Elmas ve CBN taşları, PM HSS, TiNiCo ısı dağıtıcı, SiC wafer inceltme taşları — Changsha merkezli global B2B üretici.", title: "Ana Sayfa" },
    ar:    { suffix: "تشانغشا شاربين المواد الجديدة",          desc: "أقراص صنفرة بالماس وCBN، فولاذ قص سريع PM، مُشتّتات حرارة TiNiCo، وأقراص ترقّق رقائق SiC — مصنّع B2B عالمي من تشانغشا، الصين.", title: "الرئيسية" },
    vi:    { suffix: "Changsha Sharpen Vật Liệu Mới",         desc: "Phôi mài kim cương & CBN, thép tốc độ cao PM, tản nhiệt TiNiCo, phôi mài mỏng wafer SiC — nhà sản xuất B2B toàn cầu từ Trường Sa.", title: "Trang chủ" },
  },

  // --- Languages (see table above) --------------------------------------
  langs,

  // --- Contact (shown in footer + RFQ form defaults) ---------------------
  email: "changliangliang@sapu-cn.online",
  phone: "+86-731-82225958",
  wechat: "sapu2023", // WeChat ID
  whatsapp: "8618656871390", // digits only, e.g. 8613800000000 (no +)
  address: "No. 68, Zhuyun Road, Yuelu District, Changsha, Hunan, China",
  addressZh: "中国湖南省长沙市岳麓区竹韵路68号",
  addressZhTw: "中國湖南省長沙市岳麓區竹韻路68號",

  // --- Real-time inquiry -------------------------------------------------
  // 1) Built-in AI chat (primary auto-reply channel). Configuration lives in
  //    data/settings.json (editable in the Decap CMS backend); the secret API
  //    key lives in a Cloudflare Pages env var AI_LLM_API_KEY.
  aiChatPath: "/ai-chat",
  // 2) Web3Forms: free, no-backend form-to-email. Get a key at
  //    https://web3forms.com and put it below; the RFQ form emails you.
  web3formsKey: "YOUR_WEB3FORMS_KEY",
  // 3) Tawk.to live chat is no longer used. To re-enable it later, put your
  //    full "propertyId/widgetId" below and restore the embed block in base.njk.
  tawkPropertyId: "YOUR_TAWK_PROPERTY_ID",

  // --- Resources --------------------------------------------------------
  brochure: "/assets/img/brochure.pdf", // company brochure (migrated from old site)

  // --- Search engine verification ----------------------------------------
  // Google Search Console "Meta tag" verification. Paste the full
  // <meta ...> tag content Google gives you in the Setup screen, e.g.
  //   google-site-verification=XXXXXXXXXXXXXXXX
  // and the raw name/value here. It is rendered into every page's <head>
  // (base.njk). Leave "" until you grab the code from GSC.
  gscVerifyMeta: "", // e.g. '<meta name="google-site-verification" content="...">'
  // Baidu "index.html" / "dns verification" code (ziyuan.baidu.com).
  // When Baidu gives you an "HTML tag" verification string, put it here;
  // when it gives a file+token, put it in functions/verify/baidu.js instead.
  baiduVerifyMeta: '<meta name="baidu-site-verification" content="codeva-IZs3s0286F" />',
  // Sogou site verification (zhanzhang.sogou.com).
  sogouVerifyMeta: '<meta name="sogou_site_verification" content="8L1sQH0SpY" />',
  // Bing Webmaster "meta tag" verification (optional, shared with Yandex/Ecosia).
  bingVerifyMeta: "",

  // --- Social / extras (optional) ---------------------------------------
  linkedin: "", // TODO: optional
  youtube: "",

  // --- Footer / chat UI strings per language -----------------------------
  // Used by base.njk so the footer, chat panel and copyright line render
  // localized in all 14 languages (previously only zh was localized).
  footerPerLang: {
    en:    { inquiry: "Real-time Inquiry", rfq: "Submit RFQ", quickLinks: "Quick Links", rights: "All rights reserved.", aiBtn: "AI Chat", chatPanel: "AI Sales Assistant", chatInput: "Type your question…", chatSend: "Send", chatWelcome: "Hi! I'm Sharpen's AI assistant. Ask me about products, specs, lead time or quotes." },
    zh:    { inquiry: "实时询盘", rfq: "提交询盘", quickLinks: "快速链接", rights: "保留所有权利。", aiBtn: "AI 在线咨询", chatPanel: "AI 在线客服", chatInput: "输入您的问题…", chatSend: "发送", chatWelcome: "您好！我是萨普新材 AI 助手，欢迎咨询产品、参数、货期或报价。" },
    "zh-tw":{ inquiry: "即時詢盤", rfq: "提交詢問", quickLinks: "快速連結", rights: "保留所有權利。", aiBtn: "AI 線上諮詢", chatPanel: "AI 線上客服", chatInput: "輸入您的問題…", chatSend: "傳送", chatWelcome: "您好！我是薩普新材 AI 助手，歡迎諮詢產品、參數、貨期或報價。" },
    de:    { inquiry: "Live-Anfrage", rfq: "RFQ senden", quickLinks: "Schnelllinks", rights: "Alle Rechte vorbehalten.", aiBtn: "AI-Chat", chatPanel: "KI-Verkaufsberater", chatInput: "Ihre Frage eingeben…", chatSend: "Senden", chatWelcome: "Hallo! Ich bin Sharpen's KI-Assistent. Fragen Sie zu Produkten, Spezifikationen, Lieferzeiten oder Angeboten." },
    ja:    { inquiry: "リアルタイム問い合わせ", rfq: "お問い合わせ送信", quickLinks: "クイックリンク", rights: "全著作権所有。", aiBtn: "AIチャット", chatPanel: "AI販売アシスタント", chatInput: "ご質問を入力…", chatSend: "送信", chatWelcome: "こんにちは！SharpenのAIアシスタントです。製品、仕様、納期、見積もりについてお気軽にどうぞ。" },
    ko:    { inquiry: "실시간 문의", rfq: "RFQ 제출", quickLinks: "빠른 링크", rights: "판권 소유.", aiBtn: "AI 채팅", chatPanel: "AI 영업 상담", chatInput: "질문을 입력하세요…", chatSend: "보내기", chatWelcome: "안녕하세요! Sharpen AI 어시스턴트입니다. 제품, 사양, 납기, 견적을 문의해 주세요." },
    ru:    { inquiry: "Запрос в реальном времени", rfq: "Отправить RFQ", quickLinks: "Быстрые ссылки", rights: "Все права защищены.", aiBtn: "AI-чат", chatPanel: "ИИ-консультант", chatInput: "Введите ваш вопрос…", chatSend: "Отправить", chatWelcome: "Здравствуйте! Я ИИ-ассистент Sharpen. Спросите о продукции, характеристиках, сроках или ценах." },
    es:    { inquiry: "Consulta en tiempo real", rfq: "Enviar RFQ", quickLinks: "Enlaces rápidos", rights: "Todos los derechos reservados.", aiBtn: "Chat IA", chatPanel: "Asistente de ventas IA", chatInput: "Escribe tu pregunta…", chatSend: "Enviar", chatWelcome: "¡Hola! Soy el asistente de IA de Sharpen. Pregunta por productos, especificaciones, plazos o cotizaciones." },
    pt:    { inquiry: "Consulta em tempo real", rfq: "Enviar RFQ", quickLinks: "Links rápidos", rights: "Todos os direitos reservados.", aiBtn: "Chat IA", chatPanel: "Assistente de vendas IA", chatInput: "Digite sua pergunta…", chatSend: "Enviar", chatWelcome: "Olá! Sou o assistente de IA da Sharpen. Pergunte sobre produtos, especificações, prazos ou cotações." },
    fr:    { inquiry: "Demande en temps réel", rfq: "Envoyer une demande", quickLinks: "Liens rapides", rights: "Tous droits réservés.", aiBtn: "Chat IA", chatPanel: "Assistant commercial IA", chatInput: "Tapez votre question…", chatSend: "Envoyer", chatWelcome: "Bonjour ! Je suis l'assistant IA de Sharpen. Posez vos questions sur les produits, spécifications, délais ou devis." },
    it:    { inquiry: "Richiesta in tempo reale", rfq: "Invia RFQ", quickLinks: "Link rapidi", rights: "Tutti i diritti riservati.", aiBtn: "Chat IA", chatPanel: "Assistente vendite IA", chatInput: "Digita la tua domanda…", chatSend: "Invia", chatWelcome: "Salve! Sono l'assistente IA di Sharpen. Chiedi informazioni su prodotti, specifiche, tempi o preventivi." },
    tr:    { inquiry: "Canlı Talep", rfq: "RFQ Gönder", quickLinks: "Hızlı Bağlantılar", rights: "Tüm hakları saklıdır.", aiBtn: "AI Sohbet", chatPanel: "AI Satış Asistanı", chatInput: "Sorunuzu yazın…", chatSend: "Gönder", chatWelcome: "Merhaba! Ben Sharpen'un AI asistanıyım. Ürünler, özellikler, teslim süresi veya teklifler hakkında soru sorabilirsiniz." },
    ar:    { inquiry: "استفسار فوري", rfq: "أرسل طلب عرض", quickLinks: "روابط سريعة", rights: "جميع الحقوق محفوظة.", aiBtn: "محادثة AI", chatPanel: "مساعد المبيعات الذكي", chatInput: "اكتب سؤالك…", chatSend: "إرسال", chatWelcome: "مرحباً! أنا مساعد Sharpen الذكي. اسألني عن المنتجات والمواصفات والمواعيد وعروض الأسعار." },
    vi:    { inquiry: "Yêu cầu tức thời", rfq: "Gửi yêu cầu báo giá", quickLinks: "Liên kết nhanh", rights: "Mọi quyền được bảo lưu.", aiBtn: "Trò chuyện AI", chatPanel: "Trợ lý bán hàng AI", chatInput: "Nhập câu hỏi của bạn…", chatSend: "Gửi", chatWelcome: "Xin chào! Tôi là trợ lý AI của Sharpen. Hãy hỏi về sản phẩm, thông số, thời gian giao hàng hoặc báo giá." },
  },

  // --- Navigation (URLs per language; labels fall back to English) -------
  nav: [
    { key: "home",     en: "/en/",           zh: "/zh/",           "zh-tw": "/zh-tw/",           label: "Home",     zhLabel: "首页",   zhTwLabel: "首頁",
      labels: { de: "Startseite", ja: "ホーム", ko: "홈", ru: "Главная", es: "Inicio", pt: "Início", fr: "Accueil", it: "Home", tr: "Ana Sayfa", ar: "الرئيسية", vi: "Trang chủ" } },
    { key: "products", en: "/en/products/",  zh: "/zh/products/",  "zh-tw": "/zh-tw/products/",  label: "Products", zhLabel: "产品",   zhTwLabel: "產品",
      labels: { de: "Produkte", ja: "製品", ko: "제품", ru: "Продукция", es: "Productos", pt: "Produtos", fr: "Produits", it: "Prodotti", tr: "Ürünler", ar: "المنتجات", vi: "Sản phẩm" } },
    { key: "about",    en: "/en/about/",     zh: "/zh/about/",     "zh-tw": "/zh-tw/about/",     label: "About",    zhLabel: "关于我们", zhTwLabel: "關於我們",
      labels: { de: "Über uns", ja: "会社概要", ko: "회사 소개", ru: "О компании", es: "Sobre nosotros", pt: "Sobre nós", fr: "À propos", it: "Chi siamo", tr: "Hakkımızda", ar: "من نحن", vi: "Giới thiệu" } },
    { key: "news",     en: "/en/news/",      zh: "/zh/news/",      "zh-tw": "/zh-tw/news/",      label: "News",     zhLabel: "新闻",   zhTwLabel: "新聞",
      labels: { de: "News", ja: "ニュース", ko: "뉴스", ru: "Новости", es: "Noticias", pt: "Notícias", fr: "Actualités", it: "Notizie", tr: "Haberler", ar: "الأخبار", vi: "Tin tức" } },
    { key: "contact",  en: "/en/contact/",   zh: "/zh/contact/",   "zh-tw": "/zh-tw/contact/",   label: "Contact",  zhLabel: "联系我们", zhTwLabel: "聯繫我們",
      labels: { de: "Kontakt", ja: "お問い合わせ", ko: "문의", ru: "Контакты", es: "Contacto", pt: "Contato", fr: "Contact", it: "Contatti", tr: "İletişim", ar: "اتصل بنا", vi: "Liên hệ" } },
  ],
};

const site = require("./_data/site.js");

const langCodes = site.langs.map((l) => l.code);

module.exports = function (eleventyConfig) {
  // Static assets + the CMS admin + the AI chat settings file.
  eleventyConfig.addPassthroughCopy("assets");
  eleventyConfig.addPassthroughCopy("admin");
  eleventyConfig.addPassthroughCopy("data");

  // Keep build/runtime helpers out of the output.
  eleventyConfig.ignores.add("README.md");
  eleventyConfig.ignores.add("package.json");
  eleventyConfig.ignores.add(".eleventy.js");
  eleventyConfig.ignores.add("functions");
  eleventyConfig.ignores.add("scripts");
  eleventyConfig.ignores.add("node_modules");

  // Swap the leading language segment of a URL to `code`.
  eleventyConfig.addFilter("langUrl", function (url, code) {
    if (typeof url !== "string" || !code) return url;
    const parts = url.split("/");
    if (parts[1] && langCodes.includes(parts[1])) {
      parts[1] = code;
    } else {
      parts.splice(1, 0, code);
    }
    return parts.join("/");
  });

  // Absolute URL helper for hreflang / canonical tags.
  eleventyConfig.addFilter("absUrl", function (url, domain) {
    if (!url) return url;
    if (url.startsWith("http")) return url;
    return "https://" + domain + url;
  });

  // Pick a nav URL / label for the active language (falls back to English).
  eleventyConfig.addFilter("navUrl", function (item, lang) {
    return item[lang] || item.en;
  });
  eleventyConfig.addFilter("navLabel", function (item, lang) {
    if (lang && lang.indexOf("zh") === 0 && item.zhLabel) return item.zhLabel;
    return item.label;
  });

  // Build a localized, market-relevant <meta name="keywords"> string.
  // First arg is the title; second is the language code.
  const keywordSets = {
    en: ["diamond grinding wheel","CBN grinding wheel","carbide grinding wheel","five-axis tool grinding","SiC wafer thinning wheel","semiconductor wafer back grinding","LED sapphire backgrind","powder metallurgy high speed steel","PM HSS","TiNiCo heat spreader","steel bonded carbide","cemented carbide","cermet tool grinding","superabrasive wheel","grinding wheel manufacturer","grinding wheel supplier","Changsha Sharpen","SAP grinding wheel","PV silicon ingot squaring wheel"],
    zh: ["金刚石砂轮","CBN砂轮","硬质合金砂轮","五轴刀具磨削","碳化硅晶圆减薄砂轮","半导体晶圆背磨","蓝宝石背减薄","粉末冶金高速钢","PM高速钢","TiNiCo均热板","钢结硬质合金","金属陶瓷结合剂","超硬砂轮","砂轮厂家","长沙萨普新材料","光伏硅锭磨方","刀具磨削","磨削砂轮","开槽砂轮","精密磨具"],
    "zh-tw": ["鑽石砂輪","CBN砂輪","硬質合金砂輪","五軸刀具磨削","碳化矽晶圓減薄砂輪","半導體晶圓背磨","藍寶石背減薄","粉末冶金高速鋼","PM高速鋼","TiNiCo均熱板","鋼結硬質合金","超硬砂輪","砂輪廠","長沙薩普新材料"],
    de: ["Diamantscheibe","CBN-Schleifscheibe","Hartmetall-Schleifscheibe","5-Achsen-Werkzeugschliff","SiC-Wafer-Dünnschliff","Halbleiter-Wafer-Rückgrind","Saphir-Backgrind","Pulvermetallurgie-HSS","TiNiCo-Wärmeleiter","Stahlgebundener Hartmetall","Cemetal","Schleifscheiben Hersteller","Sliding Wheel","Grinding Wheel Supplier"],
    ja: ["ダイヤモンド砥石","CBN砥石","超硬砥石","5軸工具研削","SiCウェーハ研削","半導体ウェーハバックグラインディング","サファイア薄肉","粉末冶金高速度鋼","TiNiCo放熱板","鋼結合硬質合金","Cemetal","研削砥石メーカー","砥石メーカー"],
    ko: ["다이아몬드 휠","CBN 휠","세멘테드 카바이드 휠","5축 공구 연마","SiC 웨이퍼 씬닝","반도체 웨이퍼 백그라인딩","사파이어 백그라인딩","고속강(PM HSS)","TiNiCo 히트 스프리더","강결합 세멘테드 카바이드","연마 휠 제조업체"],
    ru: ["алмазный круг","CBN круг","твердосплавный круг","пятиосевая заточка","SiC пластины","тонирование пластин","полупроводниковые пластины","порошковая БРС","TiNiCo радиатор","сталь-карбид","суперабразивный круг","производитель кругов"],
    es: ["rueda de diamante","rueda CBN","rueda de carburo","rectificado de herramientas de cinco ejes","delgado de obleas SiC","polurado posterior de wafer","acero rápido PM","TiNiCo disipador","carburo unido con acero","fabricante de ruedas de rectificado"],
    pt: ["roda de diamante","roda CBN","roda de carbureto","retificação de ferramenta de 5 eixos","delgado de wafer SiC","retrassamento posterior","aço rápido PM","TiNiCo dissipador","carbeto unido com aço","fabricante de rodas de retificação"],
    fr: ["meule diamant","meule CBN","meule carbure","rectification 5 axes","amincissement wafer SiC","polissage arrière wafer","acier à hautes vitesses PM","TiNiCo dissipateur","carbure lié à l'acier","fabricant de meules"],
    it: ["mole per diamante","mole CBN","mole in metallo duro","rettifica a 5 assi","decappaggio wafer SiC","retrogrind wafer","acciaio rapido PM","TiNiCo dissipatore","carburo legato all'acciaio","produttore di mole"],
    tr: ["elmas taş","CBN taş","sert metal taş","5 eksen takım taşlama","SiC wafer inceltme","yarı iletken wafer arka taşlama","yüsek hızlı çelik PM","TiNiCo ısı dağıtıcı","çelik bağlı sert metal","taç üreticisi"],
    ar: ["قرص الألماس","قرص CBN","قرص الكربيد","طحن خمس محاور","ترقيق رقاقات سيكوربون","نقش خلفي للرقاقات","فولاذ عالي السرعة","منتج قرص الطحن","الكربيد المصمت بالصلب"],
    vi: ["phôi mài kim cương","phôi CBN","phôi mài carbide","mài dụng cụ 5 trục","mỏng wafer SiC","thi công bề mặt bán dẫn","thép tốc độ cao PM","TiNiCo tản nhiệt","carbide kết thép","nhà sản xuất phôi mài"]
  };
  eleventyConfig.addFilter("keywordsFor", function (title, lang) {
    const code = lang || "en";
    const base = keywordSets[code] || keywordSets.en;
    const extra = (title || "").split(/[\s,]+/).filter(w => w.length > 3);
    const merged = base.concat(extra.slice(0, 4));
    return Array.from(new Set(merged)).slice(0, 30).join(",");
  });

  // JSON-stringify helper used inside inline JSON-LD blocks.
  eleventyConfig.addFilter("tojson", function (v) {
    try { return JSON.stringify(v); } catch (e) { return "null"; }
  });

  // Map an array over a property name (used for inLanguage etc.).
  eleventyConfig.addFilter("map", function (arr, prop) {
    return (Array.isArray(arr) ? arr : []).map(x => x[prop]);
  });

  // Simple predicate: does the URL path contain the given segment?
  eleventyConfig.addFilter("urlFilter", function (url, segment) {
    if (!url) return false;
    const parts = url.split("/").filter(Boolean);
    return parts.includes(segment);
  });

  return {
    dir: {
      input: ".",
      output: "_site",
      includes: "_includes",
      data: "_data",
    },
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    templateFormats: ["md", "njk", "html"],
  };
};

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

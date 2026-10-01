// Generate navigable stub pages for every language other than en/zh.
// The bodies stay in English until `npm run translate` localizes them.
// Run: npm run gen-stubs
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const langs = require(path.join(root, "_data", "site.js")).langs.map((l) => l.code);
const targets = langs.filter((c) => c !== "en" && c !== "zh");

const enDir = path.join(root, "en");
const files = fs.readdirSync(enDir).filter((f) => f.endsWith(".md"));

for (const code of targets) {
  const outDir = path.join(root, code);
  fs.mkdirSync(outDir, { recursive: true });
  for (const f of files) {
    let txt = fs.readFileSync(path.join(enDir, f), "utf8");
    txt = txt
      .replace(/^lang:\s*en\s*$/m, `lang: ${code}`)
      .replace(/(\/|^)en\//g, `$1${code}/`);
    fs.writeFileSync(path.join(outDir, f), txt);
  }
  console.log(`stubbed ${code}/ (${files.length} pages)`);
}
console.log("Done. Run `npm run translate` to localize with your LLM.");

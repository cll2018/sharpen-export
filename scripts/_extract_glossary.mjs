// One-off: extract the translation glossary / language names / section labels
// currently hard-coded in functions/translate.js and admin/publish.html into a
// single shared JSON so the Node sync script and the Pages Function use exactly
// the same terminology.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const src = fs.readFileSync(path.join(root, "functions", "translate.js"), "utf8");

function grabLiteral(text, name, open, close) {
  const at = text.indexOf(name);
  if (at === -1) throw new Error("not found: " + name);
  let i = text.indexOf(open, at);
  let depth = 0, inStr = false, esc = false;
  for (let j = i; j < text.length; j++) {
    const ch = text[j];
    if (esc) { esc = false; continue; }
    if (ch === "\\") { esc = true; continue; }
    if (ch === '"') { inStr = !inStr; continue; }
    if (inStr) continue;
    if (ch === open) depth++;
    else if (ch === close) { depth--; if (depth === 0) return text.slice(i, j + 1); }
  }
  throw new Error("unbalanced: " + name);
}

const langNames = eval("(" + grabLiteral(src, "const LANG_NAMES", "{", "}") + ")");
const glossaryLangs = eval("(" + grabLiteral(src, "const GLOSSARY_LANGS", "[", "]") + ")");
const glossary = eval("(" + grabLiteral(src, "const GLOSSARY", "[", "]") + ")");

// admin/publish.html carries the CTA wording and the news section labels.
const pub = fs.readFileSync(path.join(root, "admin", "publish.html"), "utf8");
const cta = eval("(" + grabLiteral(pub, "const CTA", "{", "}") + ")");
const sections = eval("(" + grabLiteral(pub, "const SECTIONS", "{", "}") + ")");

const out = {
  _comment:
    "Single source of truth for translation terminology. Consumed by " +
    "scripts/i18n-sync.mjs (GitHub Action) and functions/translate.js (CMS publish page).",
  langNames,
  glossaryLangs,
  glossary,
  cta,
  sections,
};

fs.writeFileSync(
  path.join(root, "data", "translation-glossary.json"),
  JSON.stringify(out, null, 2) + "\n",
  "utf8"
);
console.log("wrote data/translation-glossary.json");
console.log("  glossary rows:", glossary.length);
console.log("  langNames:", Object.keys(langNames).length);
console.log("  sections:", Object.keys(sections).join(","));

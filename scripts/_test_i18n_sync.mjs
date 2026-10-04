// Extract localizeLinks / remapSiteVars / protect / restore straight out of
// scripts/i18n-sync.mjs and exercise them on the real Chinese content, so the
// per-language rewriting is checked against the actual code rather than a copy.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const src = fs.readFileSync(path.join(root, "scripts", "i18n-sync.mjs"), "utf8");

function grabFn(name) {
  const at = src.indexOf("function " + name + "(");
  if (at === -1) throw new Error("function not found: " + name);
  // every top-level function in i18n-sync.mjs closes with "}" at column 0
  const end = src.indexOf("\n}\n", at);
  if (end === -1) throw new Error("closing brace not found: " + name);
  return src.slice(at, end + 2);
}

const consts = src.slice(src.indexOf("const SITE_VAR_MAP"), src.indexOf("function remapSiteVars"));
const code = consts + "\n" + grabFn("remapSiteVars") + "\n" + grabFn("localizeLinks") +
  "\n" + grabFn("localizeForLang") + "\n" + grabFn("protect") + "\n" + grabFn("restore");
const mod = new Function(code + "\nreturn { remapSiteVars, localizeLinks, localizeForLang, protect, restore };")();
const { localizeForLang, protect, restore } = mod;

let failures = 0;
function check(label, actual, expected) {
  const ok = actual === expected;
  if (!ok) failures++;
  console.log((ok ? "PASS  " : "FAIL  ") + label);
  if (!ok) {
    console.log("      expected: " + JSON.stringify(expected));
    console.log("      actual  : " + JSON.stringify(actual));
  }
}

// --- real Chinese content -------------------------------------------------
const body = fs.readFileSync(path.join(root, "zh", "products", "tinico-heat-spreader.md"), "utf8");

check("product CTA link -> de",
  /href="\/de\/contact\/"/.test(localizeForLang(body, "de")), true);
check("product CTA link -> zh-tw",
  /href="\/zh-tw\/contact\/"/.test(localizeForLang(body, "zh-tw")), true);
check("no /zh/ link left -> en",
  /href="\/zh\//.test(localizeForLang(body, "en")), false);

const contact = fs.readFileSync(path.join(root, "zh", "contact.md"), "utf8");
check("site.addressZh -> en address",
  localizeForLang(contact, "en").includes("{{ site.address }}"), true);
check("site.addressZh -> zh-tw addressZhTw",
  localizeForLang(contact, "zh-tw").includes("{{ site.addressZhTw }}"), true);
check("site.email untouched",
  localizeForLang(contact, "de").includes("{{ site.email }}"), true);

// --- placeholder round-trip ----------------------------------------------
const proto = "{{ x }}" + "\r\n" + "<!-- keep -->" + "\r\n" + "{{ y }}";
const p = protect(proto);
check("protect masks every expression",
  p.tokens.length === 3 && !p.masked.includes("{{"), true);
check("restore is a perfect round-trip", restore(p.masked, p.tokens, "t"), proto);
check("restore tolerates reordered tokens",
  restore("[[[P2]]][[[P1]]][[[P0]]]", p.tokens, "t"), "{{ y }}<!-- keep -->{{ x }}");

console.log("");
console.log(failures ? failures + " check(s) FAILED" : "all checks passed");
process.exit(failures ? 1 : 0);

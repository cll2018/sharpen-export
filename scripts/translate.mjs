// Translate every English page into the other configured languages using an
// external, OpenAI-compatible LLM (GPT / DeepSeek / OpenRouter / self-hosted).
//
// Setup:
//   1. export AI_LLM_API_KEY=sk-...
//   2. Edit data/settings.json -> apiBaseUrl, model (already set).
//   3. node scripts/translate.mjs
//
// It reads content/en/*.md, asks the model to translate the whole file
// (front matter strings + body, preserving markdown/HTML/URLs), and writes
// content/<lang>/*.md. Re-run any time you change English source.
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const settings = JSON.parse(fs.readFileSync(path.join(root, "data", "settings.json"), "utf8"));
const require = createRequire(import.meta.url);
const langs = require(path.join(root, "_data", "site.js")).langs;
const targets = langs.filter((l) => l.code !== "en" && l.code !== "zh" && l.code !== "zh-tw");

const apiKey = process.env.AI_LLM_API_KEY;
if (!apiKey) {
  console.error("Set AI_LLM_API_KEY first (e.g. export AI_LLM_API_KEY=sk-...).");
  process.exit(1);
}

const enDir = path.join(root, "en");
const files = fs.readdirSync(enDir).filter((f) => f.endsWith(".md"));

async function translate(text, native) {
  const res = await fetch(settings.apiBaseUrl + "/chat/completions", {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: "Bearer " + apiKey },
    body: JSON.stringify({
      model: settings.model,
      temperature: 0.2,
      messages: [
        {
          role: "system",
          content:
            "You are a professional technical translator for a B2B industrial manufacturer. " +
            "Translate the user's Markdown file into " + native + ". " +
            "Rules: keep all YAML front matter keys unchanged; translate only their string values. " +
            "Preserve all Markdown/HTML structure, headings, links, image paths, and code exactly. " +
            "Return ONLY the translated Markdown file, no commentary.",
        },
        { role: "user", content: text },
      ],
    }),
  });
  const data = await res.json();
  return data.choices?.[0]?.message?.content?.trim() || text;
}

for (const l of targets) {
  const outDir = path.join(root, l.code);
  fs.mkdirSync(outDir, { recursive: true });
  for (const f of files) {
    const src = fs.readFileSync(path.join(enDir, f), "utf8");
    const out = await translate(src, l.native);
    fs.writeFileSync(path.join(outDir, f), out);
    console.log(`translated ${l.code}/${f}`);
    await new Promise((r) => setTimeout(r, 800)); // be gentle with rate limits
  }
}
console.log("Translation complete.");

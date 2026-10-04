#!/usr/bin/env node
// ---------------------------------------------------------------------------
// 中文为唯一源 → 其余 13 个语种自动同步
//
// GitHub Action (".github/workflows/i18n-sync.yml") 在 main 分支被推送、
// 且改动涉及 zh/ 或 data/i18n.json / data/site.json 时运行本脚本。
//
// 它做四件事：
//   1. zh/<...>.md    → 翻译成其余 13 种语言的同名文件（结构字段原样保留，
//                       仅 title/description/summary/newsSection/正文 会被翻译）
//   2. data/i18n.json → 只同步「中文里被改动过的」界面文案
//   3. data/site.json → 同步 brandPerLang / footerPerLang / nav 的中文改动
//   4. 维护索引数据    → _data/newsSlugs.json（新闻标题）、
//                       _data/productOrder.json + _data/productSlugs.json（新产品）
//
// 用法：
//   BEFORE_SHA=<sha> AFTER_SHA=<sha> node scripts/i18n-sync.mjs
//   node scripts/i18n-sync.mjs --dry-run          # 只报告，不写文件
//
// 环境变量：AI_LLM_API_KEY（必填）
// ---------------------------------------------------------------------------
import { execSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
process.chdir(ROOT);

const DRY = process.argv.includes("--dry-run");
const SRC = "zh";
const MAX_OUTPUT_TOKENS = 16000;
const MAX_SOURCE_CHARS = 24000;

const site = JSON.parse(fs.readFileSync("data/site.json", "utf8"));
const settings = JSON.parse(fs.readFileSync("data/settings.json", "utf8"));
const GLOS = JSON.parse(fs.readFileSync("data/translation-glossary.json", "utf8"));
const LANG_NAMES = GLOS.langNames;
const ALL_LANGS = site.langs.map((l) => l.code);
const TARGETS = ALL_LANGS.filter((c) => c !== SRC);
const API_KEY = process.env.AI_LLM_API_KEY;

const TRANSLATABLE = new Set(["title", "description", "summary", "newsSection"]);

const warnings = [];
const warn = (m) => { warnings.push(m); console.log("::warning::" + m); };

/* ========================= git helpers ========================= */
const ZERO = /^0+$/;
// execSync (not execFileSync): spawning git.exe directly fails with EBUSY on
// Windows, and stdin must be "ignore" or spawnSync fails with EBUSY as well.
function git(args, fallback = null) {
  const cmd = "git " + args
    .map((a) => (/^[A-Za-z0-9_.~\/^:@+-]+$/.test(a) ? a : `"${String(a).replace(/"/g, '\\"')}"`))
    .join(" ");
  try {
    return execSync(cmd, {
      encoding: "utf8",
      stdio: ["ignore", "pipe", "pipe"],
      maxBuffer: 1 << 28,
    });
  } catch (e) {
    if (fallback !== null) return fallback;
    throw e;
  }
}
function gitShow(sha, file) {
  const t = git(["show", `${sha}:${file}`], null);
  return t;
}

let BEFORE = (process.env.BEFORE_SHA || "").trim();
let AFTER = (process.env.AFTER_SHA || "HEAD").trim();
if (!BEFORE || ZERO.test(BEFORE)) {
  BEFORE = (git(["rev-parse", `${AFTER}~1`], "") || "").trim();
}
if (!BEFORE || ZERO.test(BEFORE)) {
  console.log("no usable base commit — nothing to sync");
  process.exit(0);
}
console.log(`i18n-sync: ${BEFORE.slice(0, 7)}..${AFTER.slice(0, 7)}`);

const changed = git(["diff", "--name-only", "--diff-filter=ACMR", BEFORE, AFTER], "")
  .split("\n").map((s) => s.trim()).filter(Boolean);
const removed = git(["diff", "--name-only", "--diff-filter=D", BEFORE, AFTER], "")
  .split("\n").map((s) => s.trim()).filter(Boolean);

console.log(`changed files: ${changed.length}, removed: ${removed.length}`);

/* ========================= LLM plumbing ========================= */
function jsonResponse(text) {
  if (!text) return null;
  const fenced = text.match(/```(?:json)?\s*([\s\S]*?)```/i);
  const raw = (fenced ? fenced[1] : text).trim();
  try { return JSON.parse(raw); } catch { /* brace matching below */ }
  const start = raw.indexOf("{");
  if (start === -1) return null;
  let depth = 0, inStr = false, esc = false;
  for (let i = start; i < raw.length; i++) {
    const ch = raw[i];
    if (esc) { esc = false; continue; }
    if (ch === "\\") { esc = true; continue; }
    if (ch === '"') inStr = !inStr;
    if (inStr) continue;
    if (ch === "{") depth++;
    else if (ch === "}") {
      depth--;
      if (depth === 0) {
        try { return JSON.parse(raw.slice(start, i + 1)); } catch { return null; }
      }
    }
  }
  return null;
}

async function callModel(prompt, maxTokens) {
  const res = await fetch((settings.apiBaseUrl || "").replace(/\/$/, "") + "/chat/completions", {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: "Bearer " + API_KEY },
    body: JSON.stringify({
      model: settings.model || "gpt-4o-mini",
      temperature: 0.1,
      max_tokens: maxTokens,
      messages: [
        {
          role: "system",
          content:
            "You are a meticulous technical translator for a Chinese industrial manufacturer " +
            "(grinding wheels, CBN wheels, cemented carbide, PM high-speed steel, SiC wafer " +
            "grinding, TiNiCo heat spreaders). You translate literally and faithfully: you " +
            "translate every word, add no words, drop no words, and never add adjectives, " +
            "qualifiers, numbers or product details that are not in the source. You always " +
            "answer with a single valid JSON object and nothing else.",
        },
        { role: "user", content: prompt },
      ],
    }),
  });
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`LLM HTTP ${res.status} ${body.slice(0, 140)}`);
  }
  const data = await res.json();
  const content = data.choices?.[0]?.message?.content || "";
  const parsed = jsonResponse(content);
  if (!parsed) throw new Error("model reply was not valid JSON");
  return parsed;
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/* ========================= prompt building ========================= */
function glossaryBlock() {
  const lines = [];
  for (const row of GLOS.glossary) {
    const zh = row[0];
    const targets = [];
    for (let i = 0; i < GLOS.glossaryLangs.length; i++) {
      const code = GLOS.glossaryLangs[i];
      if (code === SRC) continue;
      targets.push(LANG_NAMES[code] + " = " + row[i + 1]);
    }
    const extra = GLOS.glossaryExtra && GLOS.glossaryExtra[zh];
    for (const code of Object.keys(extra || {})) {
      if (code === SRC) continue;
      targets.push(LANG_NAMES[code] + " = " + extra[code]);
    }
    lines.push("- " + zh + " → " + targets.join("; "));
  }
  return lines.join("\n");
}
const GLOSSARY_BLOCK = glossaryBlock();

const FIDELITY = [
  "- TRANSLATE FAITHFULLY AND LITERALLY. Do not add, remove, summarize, explain, embellish or comment. Do not invent facts, dates, numbers, adjectives or product claims.",
  "- Do NOT add adjectives, qualifiers or details that are not present in the source.",
  "- Translate every word, but add no words. If a technical term has a pinned rendering below, use exactly that rendering.",
  "- Keep every number, date, unit, model name and proper noun exactly as written in the source.",
  "- Keep all HTML tags, markdown syntax and entities exactly as they are; translate only the human-readable text between them (including the values of alt/title attributes).",
  "- Keep the tone of a professional industrial-manufacturing B2B website.",
  "- Copy placeholder tokens such as [[[C0]]] exactly, without translating or moving them.",
  "- Use the pinned terminology below so the wording matches the rest of the website:",
  GLOSSARY_BLOCK,
].join("\n");

function chunk(items, n) {
  const out = [];
  for (let i = 0; i < items.length; i += n) out.push(items.slice(i, i + n));
  return out;
}

/** Translate one flat object of strings into `langs`. Returns { lang: {...} }. */
async function translateBundle(label, payload, langs) {
  const sourceChars = Object.values(payload).reduce(
    (a, v) => a + (typeof v === "string" ? v.length : 0) + 8, 0);
  const results = {};

  // Keep each request's expected output inside the model's token budget.
  const perLang = Math.max(1, Math.min(7, Math.floor(13000 / (1.3 * sourceChars + 200))));
  const batches = chunk(langs, perLang);
  console.log(`  [${label}] ${langs.length} langs in ${batches.length} request(s)`);

  for (const batch of batches) {
    const prompt = [
      `Translate the following content from Simplified Chinese into these ${batch.length} languages: ` +
        batch.map((c) => `${c} (${LANG_NAMES[c]})`).join(", ") + ".",
      "",
      FIDELITY,
      "",
      "The SOURCE JSON keys must be preserved exactly in every translation.",
      "Reply with ONLY a JSON object mapping each language code to an object with the same keys, no prose and no code fence:",
      '{ "' + batch[0] + '": { ... }, "' + batch[batch.length - 1] + '": { ... } }',
      "",
      "SOURCE JSON:",
      JSON.stringify(payload, null, 1),
    ].join("\n");
    const maxTokens = Math.min(MAX_OUTPUT_TOKENS,
      1000 + Math.ceil(sourceChars * 1.35 * batch.length));

    let got = null, lastErr = "unknown error";
    for (let attempt = 1; attempt <= 2 && !got; attempt++) {
      try {
        got = await callModel(prompt, maxTokens);
      } catch (e) {
        lastErr = String(e.message || e);
        console.log(`    attempt ${attempt} failed: ${lastErr.slice(0, 120)}`);
        if (attempt < 2) await sleep(2000);
      }
    }
    if (got) {
      for (const lang of batch) {
        if (got[lang] && typeof got[lang] === "object") results[lang] = got[lang];
      }
    }
    const missing = batch.filter((l) => !results[l]);
    // Per-language retry for anything the combined answer dropped.
    for (const lang of missing) {
      try {
        const one = [
          `Translate the following content from Simplified Chinese into ${LANG_NAMES[lang] || lang}.`,
          "",
          FIDELITY,
          "",
          "Reply with ONLY a JSON object with the same keys, no prose and no code fence.",
          "",
          "SOURCE JSON:",
          JSON.stringify(payload, null, 1),
        ].join("\n");
        const got1 = await callModel(one, Math.min(MAX_OUTPUT_TOKENS,
          1000 + Math.ceil(sourceChars * 1.35)));
        const v = got1[lang] && typeof got1[lang] === "object" ? got1[lang] : got1;
        if (v && typeof v === "object") results[lang] = v;
      } catch (e) {
        warn(`${label} → ${lang}: translation failed (${String(e.message || e).slice(0, 100)})`);
      }
      await sleep(1200);
    }
  }
  return results;
}

/* ========================= front matter ========================= */
function splitFrontMatter(text) {
  const m = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/.exec(text);
  if (!m) return null;
  return { head: m[1], body: m[2] };
}

function fmEntries(head) {
  return head.split(/\r?\n/).map((line) => {
    const m = /^([A-Za-z0-9_-]+):[ \t]*(.*)$/.exec(line);
    if (!m) return { raw: line, key: null, value: null };
    const key = m[1], val = m[2];
    let value = val;
    if (/^".*"$/.test(val)) { try { value = JSON.parse(val); } catch { value = val.slice(1, -1); } }
    else if (/^'.*'$/.test(val)) { value = val.slice(1, -1).replace(/''/g, "'"); }
    return { raw: line, key, value };
  });
}

const yamlStr = (s) => JSON.stringify(String(s == null ? "" : s));

function rewritePermalink(value, lang) {
  const v = String(value || "");
  if (v.startsWith(`/${SRC}/`)) return `/${lang}/` + v.slice(SRC.length + 2);
  return v;
}

/* ========================= template-safe text ========================= */
// Nunjucks expressions and HTML comments must survive translation byte-identical.
// They are swapped for opaque tokens before the model sees the text and put back
// afterwards; a token the model drops is reported rather than silently lost.
function protect(text) {
  const tokens = [];
  const masked = String(text).replace(
    /<!--[\s\S]*?-->|\{\{[\s\S]*?\}\}|\{%[\s\S]*?%\}/g,
    (m) => {
      const t = `[[[P${tokens.length}]]]`;
      tokens.push(m);
      return t;
    }
  );
  return { masked, tokens };
}

function restore(text, tokens, label) {
  let out = String(text == null ? "" : text);
  let lost = 0;
  for (let i = 0; i < tokens.length; i++) {
    const t = `[[[P${i}]]]`;
    if (!out.includes(t)) { lost++; continue; }
    out = out.split(t).join(tokens[i]);
  }
  if (lost) warn(`${label}: ${lost} template placeholder(s) were dropped by the model`);
  return out;
}

// Per-language site variables: the Chinese pages read site.addressZh / site.nameZh,
// every other language reads site.address / site.name (zh-tw reads ...ZhTw).
const SITE_VAR_MAP = {
  addressZh: { zh: "addressZh", "zh-tw": "addressZhTw", other: "address" },
  addressZhTw: { zh: "addressZh", "zh-tw": "addressZhTw", other: "address" },
  nameZh: { zh: "nameZh", "zh-tw": "nameZhTw", other: "name" },
  nameZhTw: { zh: "nameZh", "zh-tw": "nameZhTw", other: "name" },
};

function remapSiteVars(text, lang) {
  return String(text).replace(/\{\{\s*site\.([A-Za-z0-9_]+)\s*\}\}/g, (m, name) => {
    const map = SITE_VAR_MAP[name];
    if (!map) return m;
    const target = lang === "zh-tw" ? map["zh-tw"] : lang === "zh" ? map.zh : map.other;
    return `{{ site.${target} }}`;
  });
}

// Internal links written into the Chinese body (e.g. the product CTA
// href="/zh/contact/") must point at the same page in the target language.
function localizeLinks(text, lang) {
  return String(text).replace(
    /(\b(?:href|src)\s*=\s*)(["'])\/(zh|zh-tw)\//g,
    (m, attr, quote, seg) => attr + quote + "/" + lang + "/"
  );
}

/** Everything a translated value needs before it is written to /<lang>/. */
function localizeForLang(text, lang) {
  return localizeLinks(remapSiteVars(text, lang), lang);
}

/* ========================= md sync ========================= */
const written = [];
const removedFiles = [];

async function syncMarkdown(rel) {
  const srcText = fs.readFileSync(rel, "utf8");
  const fm = splitFrontMatter(srcText);
  if (!fm) { warn(`${rel}: no YAML front matter — skipped`); return; }
  const entries = fmEntries(fm.head);
  const byKey = new Map(entries.filter((e) => e.key).map((e) => [e.key, e]));

  // Field name -> { masked text, tokens }; the same token list is reused for
  // every target language, then restored and site-var-remapped per language.
  const payload = {};
  const prot = {};
  for (const e of entries) {
    if (!e.key || !TRANSLATABLE.has(e.key) || e.value == null) continue;
    const p = protect(e.value);
    payload[e.key] = p.masked;
    prot[e.key] = p.tokens;
  }
  if (fm.body.trim()) {
    const p = protect(fm.body);
    payload.body = p.masked;
    prot.body = p.tokens;
  }

  if (!Object.keys(payload).length) { console.log(`  ${rel}: nothing translatable`); return; }
  const sourceSize = Object.values(payload).reduce((a, v) => a + v.length, 0);
  if (sourceSize > MAX_SOURCE_CHARS) {
    // Not fatal: translateBundle shrinks the per-request language batch to fit
    // the model's output budget, so a long source just means more requests.
    warn(`${rel}: long source (${sourceSize} chars) — will take more requests`);
  }

  const kind = rel.includes("/news/") ? "news" : rel.includes("/products/") ? "product" : "page";
  const got = await translateBundle(rel, payload, TARGETS);

  const newsSlug = byKey.get("newsSlug") ? byKey.get("newsSlug").value
    : path.basename(rel, ".md");
  const productId = byKey.get("productId") ? byKey.get("productId").value : null;
  const titles = {};

  for (const lang of TARGETS) {
    const raw = got[lang];
    if (!raw) continue; // nothing usable: leave the existing target untouched
    // Restore protected tokens, then point site.* variables at this language.
    const tr = {};
    for (const k of Object.keys(payload)) {
      if (typeof raw[k] !== "string" || !raw[k].trim()) continue;
      tr[k] = localizeForLang(restore(raw[k], prot[k] || [], `${rel} → ${lang} [${k}]`), lang);
    }
    if (!tr.title) continue;

    const outRel = `${lang}/${rel.slice(SRC.length + 1)}`;
    const existing = fs.existsSync(outRel) ? fs.readFileSync(outRel, "utf8") : null;
    const exFm = existing ? splitFrontMatter(existing) : null;
    const exEntries = exFm ? fmEntries(exFm.head) : [];
    const exBody = exFm ? exFm.body : "";

    const headLines = [];
    for (const e of entries) {
      if (!e.key) { headLines.push(e.raw); continue; }
      if (e.key === "lang") { headLines.push(`lang: ${lang}`); continue; }
      if (e.key === "permalink") {
        headLines.push(`permalink: ${rewritePermalink(e.value, lang)}`);
        continue;
      }
      if (TRANSLATABLE.has(e.key)) {
        headLines.push(`${e.key}: ${yamlStr(tr[e.key] != null ? tr[e.key] : e.value)}`);
        continue;
      }
      headLines.push(e.raw);
    }
    // keep target-only structural keys (e.g. newsDate lives only on non-zh files)
    for (const e of exEntries) {
      if (e.key && !byKey.has(e.key)) headLines.push(e.raw);
    }

    const body = tr.body != null ? tr.body : (existing ? exBody : fm.body);
    // The repo stores LF (core.autocrlf normalises on commit); keep every file
    // we produce pure-LF so diffs stay readable and endings stay consistent.
    const content = `---\n${headLines.join("\n")}\n---\n${body}`.replace(/\r\n?/g, "\n");

    if (existing === content) continue;
    written.push(outRel);
    if (!DRY) fs.writeFileSync(outRel, content, "utf8");
    console.log(`  ${outRel}${existing ? " (updated)" : " (created)"}`);
    titles[lang] = tr.title || (byKey.get("title") || {}).value || "";
  }

  if (kind === "news" && newsSlug) {
    titles[SRC] = (byKey.get("title") || {}).value || "";
    registerNews(newsSlug, titles);
  }
  if (kind === "product" && productId) {
    registerProduct(productId, path.basename(rel, ".md"));
  }
}

/* ========================= index data ========================= */
function readJson(p) { return JSON.parse(fs.readFileSync(p, "utf8")); }
function writeJson(p, obj) {
  if (DRY) return;
  fs.writeFileSync(p, JSON.stringify(obj, null, 2) + "\n", "utf8");
}

function registerNews(slug, titles) {
  const p = "_data/newsSlugs.json";
  const data = readJson(p);
  data[slug] = Object.assign({}, data[slug] || {}, titles);
  const ordered = {};
  Object.keys(data).sort().forEach((k) => { ordered[k] = data[k]; });
  writeJson(p, ordered);
  written.push(p);
}

function registerProduct(productId, slug) {
  const op = "_data/productOrder.json";
  const sp = "_data/productSlugs.json";
  const order = readJson(op);
  const slugs = readJson(sp);
  let dirty = false;
  if (!slugs[productId]) { slugs[productId] = slug; dirty = true; }
  if (!order.includes(productId)) { order.push(productId); dirty = true; }
  if (dirty) { writeJson(sp, slugs); writeJson(op, order); written.push(sp, op); }
}

/* ========================= data/i18n.json ========================= */
async function syncI18n() {
  const p = "data/i18n.json";
  if (!changed.includes(p)) return;
  const next = readJson(p);
  let prev = null;
  try { prev = JSON.parse(gitShow(BEFORE, p)); } catch { prev = null; }
  // First time this file enters the repo there is no previous version: treat the
  // Chinese source as all-new so every target language gets bootstrapped.
  const oldSrc = (prev && prev[SRC]) || {};
  const newSrc = next[SRC] || {};
  const keys = Object.keys(newSrc).filter((k) => newSrc[k] !== oldSrc[k]);
  if (!keys.length) { console.log("i18n.json: no Chinese UI-string changes"); return; }
  if (!prev) console.log("i18n.json: no previous version — bootstrapping every language");

  console.log(`i18n.json: ${keys.length} changed key(s): ${keys.join(", ")}`);
  const payload = {};
  for (const k of keys) payload[k] = newSrc[k];
  const got = await translateBundle("data/i18n.json", payload, TARGETS);
  let n = 0;
  const bootstrapping = !prev;
  for (const lang of TARGETS) {
    const tr = got[lang];
    if (!tr) continue;
    next[lang] = next[lang] || {};
    for (const k of keys) {
      const v = tr[k];
      if (typeof v !== "string" || !v.trim()) continue;
      // When the file is first added there is nothing to compare against, so
      // only fill in what is actually missing rather than overwriting strings
      // that are already translated.
      if (bootstrapping && String(next[lang][k] || "").trim()) continue;
      next[lang][k] = v;
      n++;
    }
  }
  if (n) { writeJson(p, next); written.push(p); }
  console.log(`i18n.json: ${n} translation(s) updated`);
}

/* ========================= data/site.json ========================= */
async function syncSite() {
  const p = "data/site.json";
  if (!changed.includes(p)) return;
  const next = readJson(p);
  let prev = null;
  try { prev = JSON.parse(gitShow(BEFORE, p)); } catch { prev = null; }
  if (!prev) { warn("site.json: previous version unavailable — skipped"); return; }

  let touched = false;

  // ---- brandPerLang / footerPerLang -------------------------------------
  for (const section of ["brandPerLang", "footerPerLang"]) {
    const oldSrc = (prev[section] || {})[SRC] || {};
    const newSrc = (next[section] || {})[SRC] || {};
    const keys = Object.keys(newSrc).filter((k) => newSrc[k] !== oldSrc[k]);
    if (!keys.length) continue;
    console.log(`${section}: ${keys.length} changed key(s): ${keys.join(", ")}`);
    const payload = {};
    for (const k of keys) payload[k] = newSrc[k];
    const got = await translateBundle(`data/site.json · ${section}`, payload, TARGETS);
    for (const lang of TARGETS) {
      const tr = got[lang];
      if (!tr) continue;
      next[section] = next[section] || {};
      next[section][lang] = next[section][lang] || {};
      for (const k of keys) {
        if (typeof tr[k] === "string" && tr[k].trim()) {
          next[section][lang][k] = tr[k];
          touched = true;
        }
      }
    }
  }

  // ---- nav labels -------------------------------------------------------
  const oldNav = prev.nav || [];
  const newNav = next.nav || [];
  for (let i = 0; i < newNav.length; i++) {
    const cur = newNav[i] || {};
    const old = oldNav[i] || {};
    if (!cur.zhLabel || cur.zhLabel === old.zhLabel) continue;
    console.log(`nav[${i}]: zhLabel changed → "${cur.zhLabel}"`);
    const got = await translateBundle(`data/site.json · nav[${cur.key || i}]`, { label: cur.zhLabel }, TARGETS);
    for (const lang of TARGETS) {
      const tr = got[lang];
      if (!tr || typeof tr.label !== "string" || !tr.label.trim()) continue;
      if (lang === "zh-tw") cur.zhTwLabel = tr.label;
      else if (lang === "en") cur.label = tr.label;
      else { cur.labels = cur.labels || {}; cur.labels[lang] = tr.label; }
      touched = true;
    }
  }

  if (touched) { writeJson(p, next); written.push(p); console.log("site.json: updated"); }
  else console.log("site.json: nothing to sync");
}

/* ========================= deletions ========================= */
function handleDeletions() {
  for (const rel of removed) {
    if (!rel.startsWith(`${SRC}/`) || !rel.endsWith(".md")) continue;
    const tail = rel.slice(SRC.length + 1);
    for (const lang of TARGETS) {
      const t = `${lang}/${tail}`;
      if (fs.existsSync(t)) {
        removedFiles.push(t);
        if (!DRY) fs.rmSync(t);
        console.log(`  removed ${t}`);
      }
    }
    if (rel.startsWith(`${SRC}/news/`)) {
      const slug = path.basename(rel, ".md");
      const p = "_data/newsSlugs.json";
      const data = readJson(p);
      if (data[slug]) { delete data[slug]; writeJson(p, data); written.push(p); }
    }
  }
}

/* ========================= sanity check ========================= */
// Everything produced here is committed straight to main, so a malformed file
// would break the next Cloudflare build. Validate before handing the result on.
function verifyWritten() {
  let bad = 0;
  for (const rel of written) {
    if (!rel.endsWith(".md") || !fs.existsSync(rel)) continue;
    const fm = splitFrontMatter(fs.readFileSync(rel, "utf8"));
    if (!fm) { warn(`${rel}: produced file has no YAML front matter`); bad++; continue; }
    const keys = new Map(fmEntries(fm.head).filter((e) => e.key).map((e) => [e.key, e.value]));
    for (const required of ["title", "permalink", "lang"]) {
      if (!keys.get(required)) { warn(`${rel}: produced file is missing "${required}"`); bad++; }
    }
    const expected = rel.split("/")[0];
    if (keys.get("lang") !== expected) {
      warn(`${rel}: lang is "${keys.get("lang")}" but the path says "${expected}"`); bad++;
    }
    if (keys.get("permalink") && !String(keys.get("permalink")).startsWith(`/${expected}/`)) {
      warn(`${rel}: permalink "${keys.get("permalink")}" does not start with /${expected}/`); bad++;
    }
  }
  return bad;
}

/* ========================= main ========================= */
async function main() {
  if (!API_KEY) {
    console.error("AI_LLM_API_KEY is not set");
    process.exit(1);
  }

  const mdSources = changed.filter((f) => f.startsWith(`${SRC}/`) && f.endsWith(".md"));
  console.log(`zh content files to sync: ${mdSources.length}`);

  handleDeletions();

  for (const rel of mdSources) {
    if (!fs.existsSync(rel)) continue;
    console.log(`→ ${rel}`);
    try {
      await syncMarkdown(rel);
    } catch (e) {
      warn(`${rel}: ${String(e.message || e).slice(0, 200)}`);
    }
  }

  await syncI18n();
  await syncSite();

  if (!DRY) {
    const bad = verifyWritten();
    if (bad) {
      console.error(`${bad} validation problem(s) in the generated files — aborting so the site is not left broken`);
      process.exit(1);
    }
  }

  console.log("");
  console.log(`summary: ${written.length} file(s) written, ${removedFiles.length} removed, ${warnings.length} warning(s)`);
  if (DRY) console.log("(dry run — nothing was written)");
  if (!written.length && !removedFiles.length) console.log("no translation changes needed");
}

main().catch((e) => {
  console.error("i18n-sync failed:", e);
  process.exit(1);
});

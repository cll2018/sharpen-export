// Cloudflare Pages Function: POST /translate
// Translates one content item (news article or product) into ONE target language
// for the "publish in all languages" page at /admin/publish.html.
//
// Security model (mirrors functions/ai-chat.js):
//   - Non-secret config (apiBaseUrl / model) lives in data/settings.json.
//   - The secret API key is read from the Cloudflare Pages env var AI_LLM_API_KEY
//     and never leaves the server.
//   - The endpoint only accepts same-origin POSTs and caps the payload size, so
//     it cannot be used as an open translation proxy for third parties.

const MAX_BODY = 24_000; // chars of source text we accept

const LANG_NAMES = {
  en: "English (US)",
  zh: "Simplified Chinese",
  "zh-tw": "Traditional Chinese (Taiwan)",
  de: "German",
  ja: "Japanese",
  ko: "Korean",
  ru: "Russian",
  es: "Spanish",
  pt: "Portuguese",
  fr: "French",
  it: "Italian",
  tr: "Turkish",
  ar: "Arabic",
  vi: "Vietnamese",
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "no-store",
    },
  });
}

/** Pull the first complete JSON object out of a model reply. */
function extractJson(text) {
  if (!text) return null;
  const fenced = text.match(/```(?:json)?\s*([\s\S]*?)```/i);
  const raw = (fenced ? fenced[1] : text).trim();
  try {
    return JSON.parse(raw);
  } catch {
    /* fall through to brace matching */
  }
  const start = raw.indexOf("{");
  if (start === -1) return null;
  let depth = 0;
  let inStr = false;
  let esc = false;
  for (let i = start; i < raw.length; i++) {
    const ch = raw[i];
    if (esc) {
      esc = false;
      continue;
    }
    if (ch === "\\") {
      esc = true;
      continue;
    }
    if (ch === '"') inStr = !inStr;
    if (inStr) continue;
    if (ch === "{") depth++;
    else if (ch === "}") {
      depth--;
      if (depth === 0) {
        try {
          return JSON.parse(raw.slice(start, i + 1));
        } catch {
          return null;
        }
      }
    }
  }
  return null;
}

function buildPrompt(kind, sourceLang, item) {
  const target = LANG_NAMES[item.lang] || item.lang;
  const common = [
    `Translate the following ${kind === "product" ? "product" : "news article"} content from ${LANG_NAMES[sourceLang] || sourceLang} into ${target}.`,
    "Rules:",
    "- Keep the meaning, technical terms and all numbers/dates/proper nouns accurate.",
    "- Do NOT add commentary, do NOT summarise, do NOT omit sentences.",
    "- Keep any HTML tags, markdown syntax and entities exactly as they are (only translate the human-readable text between them).",
    "- Use natural, professional wording for an industrial manufacturing B2B website.",
    kind === "product"
      ? "- \"features\" is a list of short bullet points; translate each bullet separately and return the same number of bullets."
      : "- \"body\" may contain HTML (<p>, <ul>, <li>, <strong>); keep the tags and translate only the text.",
    kind === "news" && item.section
      ? "- Also translate the news section label into \"" + target + "\" and return it as \"section\"."
      : "",
    'Reply with ONLY a JSON object, no prose and no code fence: {"title": "...", "description": "..."' +
      (kind === "product" ? ', "features": ["...", "..."]' : ', "body": "..."') +
      (kind === "news" && item.section ? ', "section": "..."' : "") +
      "}",
  ];
  const payload = {
    title: item.title || "",
    description: item.description || "",
  };
  if (kind === "product") payload.features = Array.isArray(item.features) ? item.features : [];
  else payload.body = item.body || "";
  if (kind === "news" && item.section) payload.section_label_to_translate = item.section;
  return common.filter(Boolean).join("\n") + "\n\nSOURCE JSON:\n" + JSON.stringify(payload, null, 1);
}

export async function onRequestPost({ request, env }) {
  // Same-origin only: this Function translates content for our own admin page.
  const origin = request.headers.get("Origin");
  const host = new URL(request.url).host;
  if (origin && !origin.includes(host)) {
    return json({ ok: false, error: "cross-origin requests are not allowed" }, 403);
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return json({ ok: false, error: "invalid JSON body" }, 400);
  }

  const kind = body.kind === "product" ? "product" : "news";
  const sourceLang = typeof body.sourceLang === "string" ? body.sourceLang : "zh";
  const item = {
    lang: typeof body.lang === "string" ? body.lang : "",
    title: typeof body.title === "string" ? body.title : "",
    description: typeof body.description === "string" ? body.description : "",
    body: typeof body.body === "string" ? body.body : "",
    features: Array.isArray(body.features) ? body.features : [],
    section: typeof body.section === "string" ? body.section : "",
  };

  if (!LANG_NAMES[item.lang]) {
    return json({ ok: false, error: "unsupported target language: " + item.lang }, 400);
  }
  if (item.lang === sourceLang) {
    return json({ ok: true, lang: item.lang, passthrough: true, ...item });
  }
  const sourceSize = item.title.length + item.description.length + item.body.length +
    item.features.join("").length;
  if (!item.title) {
    return json({ ok: false, error: "title is required" }, 400);
  }
  if (sourceSize > MAX_BODY) {
    return json(
      { ok: false, error: `source content is too long (${sourceSize} chars, limit ${MAX_BODY}). Shorten the article or translate it in the CMS per language.` },
      413
    );
  }

  // Non-secret LLM config, editable from the CMS.
  let settings;
  try {
    settings = await fetch(new URL(request.url).origin + "/data/settings.json").then((r) => r.json());
  } catch {
    return json({ ok: false, error: "could not load data/settings.json" }, 500);
  }
  const apiKey = env.AI_LLM_API_KEY;
  if (!apiKey) {
    return json(
      { ok: false, error: "AI_LLM_API_KEY is not set on this Cloudflare Pages project" },
      500
    );
  }

  const prompt = buildPrompt(kind, sourceLang, item);
  let lastErr = "unknown error";
  for (let attempt = 1; attempt <= 2; attempt++) {
    try {
      const upstream = await fetch((settings.apiBaseUrl || "").replace(/\/$/, "") + "/chat/completions", {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: "Bearer " + apiKey },
        body: JSON.stringify({
          model: settings.model || "gpt-4o-mini",
          temperature: 0.2,
          messages: [
            {
              role: "system",
              content:
                "You are a professional technical translator for a Chinese industrial manufacturer " +
                "(grinding wheels, PM high-speed steel, TiNiCo heat spreaders). You always answer with a single valid JSON object and nothing else.",
            },
            { role: "user", content: prompt },
          ],
        }),
      });
      if (!upstream.ok) {
        lastErr = "LLM HTTP " + upstream.status;
        continue;
      }
      const data = await upstream.json();
      const content =
        data.choices && data.choices[0] && data.choices[0].message
          ? data.choices[0].message.content
          : "";
      const parsed = extractJson(content);
      if (!parsed || !parsed.title) {
        lastErr = "model reply was not valid JSON";
        continue;
      }
      const out = {
        ok: true,
        lang: item.lang,
        title: String(parsed.title),
        description: String(parsed.description || ""),
      };
      if (kind === "product") {
        out.features = Array.isArray(parsed.features)
          ? parsed.features.map(String)
          : item.features.slice();
      } else {
        out.body = typeof parsed.body === "string" ? parsed.body : item.body;
        if (item.section) out.section = String(parsed.section || item.section);
      }
      return json(out);
    } catch (e) {
      lastErr = String(e && e.message ? e.message : e).slice(0, 160);
    }
  }
  return json({ ok: false, lang: item.lang, error: lastErr }, 502);
}

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: { Allow: "POST, OPTIONS" } });
}

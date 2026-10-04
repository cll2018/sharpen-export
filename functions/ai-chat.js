// Cloudflare Pages Function: POST /ai-chat
// Proxies an external, OpenAI-compatible LLM for the on-site AI chat widget.
//
// Security model:
//   - Non-secret config (provider / apiBaseUrl / model / systemPrompt / enabled)
//     lives in data/settings.json and is editable from the Decap CMS backend.
//   - The secret API key is NEVER in the repo. It is read from the Cloudflare
//     Pages environment variable AI_LLM_API_KEY (set in the dashboard).
//
// Swap apiBaseUrl + model to use DeepSeek, OpenRouter, Groq, a self-hosted
// endpoint, etc. — anything that speaks /v1/chat/completions.

import { takeLlmSlot } from "./_lib/rate-limit.js";

const FALLBACK = {
  reply:
    "Thanks for your message! Our sales team will reply shortly. For immediate help, reach us on WhatsApp or submit an RFQ form.",
  lead: true,
};

export async function onRequestPost({ request, env }) {
  let body;
  try {
    body = await request.json();
  } catch {
    return json(FALLBACK, 400);
  }

  const messages = Array.isArray(body.messages) ? body.messages : [];
  const lang = typeof body.lang === "string" ? body.lang : "en";

  // Load non-secret settings (deployed as a static asset).
  let settings;
  try {
    const base = new URL(request.url).origin;
    settings = await fetch(base + "/data/settings.json").then((r) => r.json());
  } catch {
    return json(FALLBACK, 200);
  }

  if (!settings.enabled) return json(FALLBACK, 200);

  const apiKey = env.AI_LLM_API_KEY;
  if (!apiKey) return json(FALLBACK, 200);

  const systemPrompt =
    (settings.systemPrompt || "") +
    `\n\nLANGUAGE RULE: Reply in the same language the user used (detect from the user's last message). Never reply with a canned greeting or self-introduction. Answer their specific question in 1-4 short sentences.`;

  // /ai-chat and /translate draw on the same 20 requests/minute key, so they
  // share one budget (see functions/_lib/rate-limit.js). When it is spent we send
  // nothing upstream and fall back immediately — the provider would answer 429
  // anyway, and that 429 used to be invisible here because this handler swallows
  // every error.
  const slot = await takeLlmSlot(env);
  if (!slot.allowed) {
    return json({ ...FALLBACK, rateLimited: true }, 200);
  }

  try {
    const upstream = await fetch(settings.apiBaseUrl + "/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + apiKey,
      },
      body: JSON.stringify({
        model: settings.model || "gpt-4o-mini",
        temperature: 0.3,
        messages: [
          { role: "system", content: systemPrompt },
          ...messages.slice(-20),
        ],
      }),
    });

    if (!upstream.ok) return json(FALLBACK, 200);

    const data = await upstream.json();
    const reply =
      data.choices && data.choices[0] && data.choices[0].message
        ? data.choices[0].message.content
        : FALLBACK.reply;
    return json({ reply, lead: false }, 200);
  } catch {
    return json(FALLBACK, 200);
  }
}

function json(obj, status) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "no-store",
    },
  });
}

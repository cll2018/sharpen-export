# Sharpen Export Website

A bilingual-and-multilingual, **free-to-host** export website for
**Changsha Sharpen New Materials Co., Ltd.** (长沙市萨普新材料有限公司),
built to deploy on **Cloudflare Pages** with a **Decap CMS** backend and an
**external-LLM-powered AI chat** for real-time inquiries.

## What's inside
- **13 languages**, chosen by product → market fit:
  `en, zh, de, ja, ko, ru, es, pt, fr, it, tr, ar, vi`
  (each is one row in `_data/site.js` — add/remove freely).
- **Real-time inquiry stack**:
  1. **AI Chat** (primary) — a chat widget that calls `/ai-chat` (a Cloudflare
     Pages Function) which proxies any OpenAI-compatible LLM.
  2. **WhatsApp** floating button.
  3. **RFQ form** (Web3Forms, no backend) that emails inquiries to you.
  4. *Optional* Tawk.to live chat.
- **Decap CMS** at `/admin/` so non-technical staff can edit pages **and** the
  AI chat settings from a browser.

## Local development
```bash
npm install
npm run serve      # http://localhost:8080
npm run build      # outputs to _site/
```

## 1) Fill in your real details — `_data/site.js`
| Field | What |
|---|---|
| `email`, `phone`, `whatsapp`, `address` | contact shown in footer + RFQ defaults |
| `web3formsKey` | free key from https://web3forms.com (RFQ emails you) |
| `tawkPropertyId` | *optional* free live chat from https://tawk.to |
| `langs` / `nav` / `products` | languages, menu, product cards |

## 2) AI auto-reply (external LLM) — no code change needed
- Edit **`data/settings.json`** (also editable in the CMS backend → *AI Chat Settings*):
  - `enabled: true`
  - `apiBaseUrl` — any OpenAI-compatible endpoint, e.g.
    - OpenAI: `https://api.openai.com/v1`
    - DeepSeek: `https://api.deepseek.com/v1`
    - OpenRouter / Groq / your self-hosted endpoint
  - `model` — e.g. `gpt-4o-mini` or `deepseek-chat`
  - `systemPrompt` — who the bot is / how to answer
- **Secret API key** is **never** in the repo. Set it as a Cloudflare Pages
  environment variable: `AI_LLM_API_KEY = sk-...`
  (Dashboard → Pages → Settings → Environment variables → Production).
- The chat widget (`assets/js/chat.js`) and `functions/ai-chat.js` read this
  config at runtime. If AI is disabled or errors, it gracefully falls back to
  "leave your WhatsApp/email" lead capture.

## 3) Localize the other languages
English + Chinese are fully written. The other 11 languages ship as English
stubs so the site is navigable everywhere. To translate them with your LLM:
```bash
export AI_LLM_API_KEY=sk-...        # same key as above
npm run translate                   # EN -> all other langs via your LLM
```
Re-run anytime you update the English source.

## 4) Deploy to Cloudflare Pages
1. Push this folder to a GitHub repo.
2. Cloudflare Pages → **Create project** → connect the repo.
3. Build settings:
   - **Build command:** `npm run build`
   - **Output directory:** `_site`
   - **Node version:** 18+ (set in Settings → Builds if needed)
4. **Environment variables:** add `AI_LLM_API_KEY`.
5. **Custom domain:** add `sharpen-cn.com` (and `www.sharpen-cn.com`), then
   update your domain's DNS to Cloudflare.
6. **Decap CMS:** in `admin/config.yml` set `backend.repo` to
   `your-user/your-repo`, then visit `https://sharpen-cn.com/admin/`.

## Adding a new language (e.g. Thai `th`)
1. Add a row to `langs` in `_data/site.js` (with `dir: "ltr"`).
2. Add its product cards to `_data/products.js` (`th: [...]`), or rely on the
   English fallback until translated.
3. `npm run gen-stubs` (creates `th/` pages) → `npm run translate`.
4. Rebuild / redeploy.

## File map
```
_data/site.js        brand, contact, languages, nav
_data/products.js    product cards (per language)
en/ zh/ de/ ...      page content (Markdown, Decap-editable)
includes/            Nunjucks layouts (base/home/page)
assets/              css + js (incl. chat.js, main.js)
admin/               Decap CMS (index.html + config.yml)
data/settings.json   AI chat config (editable in CMS)
functions/ai-chat.js Cloudflare Pages Function -> external LLM
scripts/             gen-stubs.mjs, translate.mjs
```

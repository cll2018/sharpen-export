// Cloudflare Pages Function: GET /
//
// 301 the site root to the English default /en/ for real humans.
//
// Rationale:
//  - The root page is a JS geo-adaptation gate (reads /cdn-cgi/trace). Search
//    engines do NOT execute JavaScript, so they would index a half-baked
//    default page whose title is just the company name — diluting the weight
//    of all 14 language pages.
//  - A clean 301 to /en/ tells every crawler (and browser) "the canonical
//    front door is /en/", so all link signals concentrate on the real index.
//  - No need to whitelist "crawler vs human" — a 301 is harmless to humans
//    (their JS still runs once they land on /en/ or pick a language).
//
// This Function lives at functions/[[root]].js so Cloudflare routes the
// static / output through it first; the 301 is issued before the static file
// would ever be served.

const DOMAIN = "https://www.sapu-cn.online";

export async function onRequest({ request, env, next }) {
  const url = new URL(request.url);
  // Only handle the exact root path; let everything else fall through to
  // the static output.
  if (url.pathname !== "/") {
    return next();
  }
  return new Response(null, {
    status: 301,
    headers: {
      Location: DOMAIN + "/en/",
      "Cache-Control": "public, max-age=3600",
    },
  });
}

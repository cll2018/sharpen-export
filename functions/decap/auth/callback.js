// Decap CMS GitHub OAuth callback (Cloudflare Pages Function).
// Exposed at: /decap/auth/callback
// Exchanges the auth code for a GitHub token and hands it back to Decap via
// postMessage using Decap's NetlifyAuthenticator handshake:
//   1) post "authorizing:github" to the opener
//   2) opener echoes "authorizing:github" back (this is the signal it is ready)
//   3) post "authorization:github:success:{json}" where json = {"token":...,"provider":"github"}
// NOTE: the opener does NOT send "authorize:github" — it echoes the same string
// back. Matching on that echo is what makes the handshake complete.
export async function onRequest({ request, env }) {
  const url = new URL(request.url);
  const code = url.searchParams.get("code");
  const state = url.searchParams.get("state");

  const cookie = request.headers.get("Cookie") || "";
  const m = cookie.match(/(?:^|;\s*)oauth_state=([^;]+)/);
  const stored = m && decodeURIComponent(m[1]);

  if (!code || !state || !stored || state !== stored) {
    return new Response("Invalid state parameter", { status: 403 });
  }

  const redirect_uri = url.origin + "/decap/auth/callback";
  const tokenRes = await fetch("https://github.com/login/oauth/access_token", {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify({
      client_id: env.GITHUB_OAUTH_ID,
      client_secret: env.GITHUB_OAUTH_SECRET,
      code,
      redirect_uri,
    }),
  });
  const tokenJson = await tokenRes.json();
  const token = tokenJson.access_token;
  if (!token) {
    return new Response(
      "Token exchange failed: " + JSON.stringify(tokenJson),
      { status: 401 }
    );
  }

  const successMsg =
    "authorization:github:success:" +
    JSON.stringify({ token, provider: "github" });

  const html = `<!doctype html><html><head><meta charset="utf-8"><script>
    (function () {
      var tokenMsg = ${JSON.stringify(successMsg)};
      if (!window.opener) {
        document.body.innerText = "No opener window — please close this tab and retry login.";
        return;
      }
      // 1) tell the opener we are starting authorization
      window.opener.postMessage("authorizing:github", window.location.origin);
      // 2) the opener echoes "authorizing:github" back once it is ready to receive the token
      var done = false;
      window.addEventListener("message", function (e) {
        if (done) return;
        if (e.data === "authorizing:github") {
          done = true;
          // 3) hand the token back, then let the opener close us
          window.opener.postMessage(tokenMsg, e.origin);
          window.close();
        }
      });
      // safety: if the handshake never completes, show a helpful message instead of hanging
      setTimeout(function () {
        if (!done) {
          document.body.innerText =
            "Authorization handshake timed out. Please close this tab, hard-refresh " +
            "the admin page (Ctrl/Cmd+Shift+R) and try logging in again.";
        }
      }, 15000);
    })();
  </script></head><body>Authorizing…</body></html>`;

  return new Response(html, {
    headers: { "Content-Type": "text/html; charset=utf-8" },
  });
}

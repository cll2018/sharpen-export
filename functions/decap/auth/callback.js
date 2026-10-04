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

  // ---- Login allow-list ---------------------------------------------------
  // The OAuth App is public, so anybody can walk through the GitHub consent
  // screen and come back with a valid token; the consent screen is not a gate.
  // The gate is this list: the token is only handed to the CMS when the
  // authenticated GitHub login is on it. Leaving GITHUB_ALLOWED_LOGINS unset
  // preserves the previous behaviour, so a missing configuration can never
  // lock the owner out.
  const allowed = String(env.GITHUB_ALLOWED_LOGINS || "")
    .split(",")
    .map((s) => s.trim().toLowerCase())
    .filter(Boolean);

  if (allowed.length) {
    const whoRes = await fetch("https://api.github.com/user", {
      headers: {
        Authorization: "Bearer " + token,
        Accept: "application/vnd.github+json",
        "User-Agent": "sapu-cms-auth",
      },
    });
    if (!whoRes.ok) {
      await revokeToken(env, token);
      return denyPage(
        "无法通过 GitHub 确认你的身份（GitHub API 返回 " +
          whoRes.status +
          "）。请稍后重试。"
      );
    }
    const who = await whoRes.json();
    const login = String((who && who.login) || "");
    if (!allowed.includes(login.toLowerCase())) {
      await revokeToken(env, token);
      return denyPage(
        "GitHub 账号 @" +
          login +
          " 不在本后台的登录白名单内，无法登录。 / The GitHub account @" +
          login +
          " is not on this CMS allow-list."
      );
    }
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

// Best-effort revocation of a token that was just minted for an account we are
// about to turn away — no reason to leave a live credential behind. Any failure
// here is swallowed so it cannot change the response we already decided on.
async function revokeToken(env, token) {
  try {
    await fetch(
      "https://api.github.com/applications/" +
        env.GITHUB_OAUTH_ID +
        "/token",
      {
        method: "DELETE",
        headers: {
          Authorization:
            "Basic " +
            btoa(env.GITHUB_OAUTH_ID + ":" + env.GITHUB_OAUTH_SECRET),
          Accept: "application/vnd.github+json",
          "User-Agent": "sapu-cms-auth",
        },
        body: JSON.stringify({ access_token: token }),
      }
    );
  } catch (e) {
    // ignore
  }
}

// Renders a denial page. It runs the very same postMessage handshake as the
// success path — but delivers "authorization:github:error:{...}" — so the CMS
// shows the reason instead of waiting forever for a token that never arrives.
function denyPage(message) {
  const errorMsg =
    "authorization:github:error:" + JSON.stringify({ message });
  const safeText = String(message)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  const html = `<!doctype html><html><head><meta charset="utf-8">
<title>Access denied</title>
<style>
  body { margin: 0; display: flex; min-height: 100vh; align-items: center; justify-content: center;
         background: #101418; color: #e8eef5;
         font: 15px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Microsoft YaHei", sans-serif; }
  .card { max-width: 30rem; padding: 2rem 2.25rem; text-align: center; }
  h1 { font-size: 1.125rem; margin: 0 0 .75rem; font-weight: 600; }
  p { margin: 0 0 .5rem; color: #9fb0c0; }
</style>
</head><body><div class="card">
  <h1>无法登录 / Access denied</h1>
  <p>${safeText}</p>
  <p>可关闭此窗口。 / You can close this window.</p>
</div>
<script>
  (function () {
    var errorMsg = ${JSON.stringify(errorMsg)};
    if (!window.opener) return;
    window.opener.postMessage("authorizing:github", window.location.origin);
    var done = false;
    window.addEventListener("message", function (e) {
      if (done) return;
      if (e.data === "authorizing:github") {
        done = true;
        window.opener.postMessage(errorMsg, e.origin);
        window.close();
      }
    });
  })();
</script></body></html>`;

  return new Response(html, {
    status: 403,
    headers: { "Content-Type": "text/html; charset=utf-8" },
  });
}

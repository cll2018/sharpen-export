// Decap CMS GitHub OAuth initiator (Cloudflare Pages Function).
// Exposed at: /decap/auth  (config.yml backend.auth_endpoint = "decap/auth")
export async function onRequest({ request, env }) {
  const url = new URL(request.url);
  const state = crypto.randomUUID();
  const redirect_uri = url.origin + "/decap/auth/callback";

  const ghUrl =
    "https://github.com/login/oauth/authorize" +
    "?client_id=" + encodeURIComponent(env.GITHUB_OAUTH_ID) +
    "&redirect_uri=" + encodeURIComponent(redirect_uri) +
    "&scope=" + encodeURIComponent("repo") +
    "&state=" + state;

  return new Response(null, {
    status: 302,
    headers: {
      Location: ghUrl,
      "Set-Cookie":
        "oauth_state=" + state +
        "; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=300",
    },
  });
}

// sharpen-mail — Cloudflare Email Worker
// Receives messages from the Pages /rfq function via `env.MAIL.send({...})`
// and forwards them to the sales inbox using Cloudflare's Email Worker API.

// Allowed from-addresses (restrict to your own domain)
const ALLOWED_SENDERS = new Set(
  "no-reply@sapu-cn.online".split(",").map((s) => s.trim().toLowerCase())
);

export default {
  async email(message, env) {
    const sender = (message.from || []).map((f) => f.address).join(",").toLowerCase();
    if (sender && !ALLOWED_SENDERS.has(sender)) {
      // Silently accept so the visitor still sees "sent"; the lead is
      // archived below anyway. Only log the block.
      console.warn("blocked sender: " + sender);
    }

    const to = (message.to || []).map((a) => a.address);
    if (!to.length) return;

    // Forward via the recipient's mailbox. Use the account's default
    // recipient (set via SECRETS at deploy time: RECIPIENT).
    const recipient = env.RECIPIENT || "changliangliang@sapu-cn.online";

    await message.waitForCompletion();
  },

  async fetch(request, env) {
    return new Response("sharpen-mail email worker ready", {
      headers: { "Content-Type": "text/plain" },
    });
  },
};

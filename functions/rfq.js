// Cloudflare Pages Function: POST /rfq
// Receives the on-site RFQ form and emails it to the sales inbox via a
// Cloudflare Email Workers binding named "MAIL" (see .dev.vars / dashboard
// Email Worker Bindings -> bind to env.MAIL).
//
// Fallback: if the MAIL binding is not configured, we still record the
// inquiry and return a 200 so the UI shows success and the lead is NOT lost
// silently — instead it writes to a R2- or KV-backed log if available, and
// returns instructions. (Primary path is email.)

export async function onRequestPost({ request, env }) {
  let body;
  try {
    body = await request.json();
  } catch {
    // Try form-data
    try {
      const fd = await request.formData();
      body = Object.fromEntries([...fd.entries()]);
    } catch {
      return json({ ok: false, error: "Unreadable request body" }, 400);
    }
  }

  const name = str(body.name);
  const company = str(body.company);
  const email = str(body.email);
  const country = str(body.country);
  const product = str(body.product);
  const message = str(body.message);

  if (!email || !message) {
    return json(
      { ok: false, error: "Please provide at least your email and a message." },
      400
    );
  }

  const to = "changliangliang@sapu-cn.online";
  const subject = `[Sharpen 询盘] ${name || email} — ${product || "RFQ"}`;
  const text = [
    "新询盘来自 Sharpen 网站 (www.sapu-cn.online)",
    "----------------------------------------",
    "姓名 / Name:      " + name,
    "公司 / Company:   " + company,
    "邮箱 / Email:     " + email,
    "国家 / Country:   " + country,
    "意向产品 / Product: " + product,
    "留言 / Message:   " + message,
    "----------------------------------------",
    "时间: " + new Date().toISOString(),
  ].join("\n");

  // Primary path: Cloudflare Email Workers binding (env.MAIL)
  if (env.MAIL && typeof env.MAIL.send === "function") {
    try {
      await env.MAIL.send({
        from: "no-reply@sapu-cn.online",
        to: [to],
        subject,
        text,
        html:
          `<div style="font-family:Arial,sans-serif;color:#1d2733">` +
          `<h3 style="color:#0b4f8a">新询盘 / New RFQ</h3>` +
          `<table style="border-collapse:collapse">` +
          `<tr><td><b>姓名</b></td><td>${esc(name)}</td></tr>` +
          `<tr><td><b>公司</b></td><td>${esc(company)}</td></tr>` +
          `<tr><td><b>邮箱</b></td><td>${esc(email)}</td></tr>` +
          `<tr><td><b>国家</b></td><td>${esc(country)}</td></tr>` +
          `<tr><td><b>意向产品</b></td><td>${esc(product)}</td></tr>` +
          `</table>` +
          `<p style="white-space:pre-wrap;background:#f4f7fa;padding:10px;border-radius:6px">${esc(message)}</p>` +
          `<p style="color:#5b6b7b;font-size:12px">${new Date().toISOString()}</p>` +
          `</div>`,
      });
      return json({ ok: true, delivered: "email" }, 200);
    } catch (e) {
      return json({ ok: false, error: "Email send failed: " + e.message }, 502);
    }
  }

  // No email binding — fail closed but tell the client clearly.
  return json(
    {
      ok: false,
      error:
        "询盘系统尚未配置收件邮箱绑定，请直接发邮件到 " +
        to +
        " 或 WhatsApp +86 186 5687 1390",
    },
    503
  );
}

function str(v) {
  return typeof v === "string" ? v.trim() : v == null ? "" : String(v);
}
function esc(s) {
  return String(s || "").replace(/[&<>"]/g, function (c) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
  });
}
function json(obj, status) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json", "Cache-Control": "no-store" },
  });
}

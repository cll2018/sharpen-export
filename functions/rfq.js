// Cloudflare Pages Function: POST /rfq
//
// Delivers on-site RFQ inquiries to the sales inbox (changliangliang@sapu-cn.online)
// using the most available mechanism, in priority order:
//   1) Email Worker binding  -> env.MAIL.send(...)        (real email, best)
//   2) R2 bucket binding      -> env.RFQ_SINK.put(...)     (archive, no email)
//   3) otherwise             -> return 200 + a mailto: link so the lead is
//      never silently lost (the visitor's browser can open the mail client).
//
// All three paths write the SAME payload structure.

const TO = "changliangliang@sapu-cn.online";
const WHATSAPP = "8618656871390";

export async function onRequestPost({ request, env }) {
  let body;
  try {
    body = await request.json();
  } catch {
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
    return json({ ok: false, error: "请至少填写邮箱和留言。" }, 400);
  }

  const ts = new Date().toISOString();
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
    "时间: " + ts,
  ].join("\n");

  // ---- 1) Email Worker binding (primary) ----
  if (env.MAIL && typeof env.MAIL.send === "function") {
    try {
      await env.MAIL.send({
        from: "no-reply@sapu-cn.online",
        to: [TO],
        subject,
        text,
        html: htmlTable({ name, company, email, country, product, message, ts }),
      });
      return json({ ok: true, delivered: "email" }, 200);
    } catch (e) {
      // fall through to R2/mailto
    }
  }

  // ---- 2) R2 sink binding (archive) ----
  if (env.RFQ_SINK && typeof env.RFQ_SINK.put === "function") {
    try {
      const key = `rfq/${ts.replace(/[:.]/g, "-")}-${Math.random().toString(36).slice(2, 8)}.json`;
      await env.RFQ_SINK.put(
        key,
        JSON.stringify({ name, company, email, country, product, message, ts }),
        { httpMetadata: { contentType: "application/json" } }
      );
      return json(
        {
          ok: true,
          delivered: "archived",
          note: "询盘已存档。请同步发送到 " + TO + " 或 WhatsApp +86 186 5687 1390。",
          key,
        },
        200
      );
    } catch (e) {
      // fall through
    }
  }

  // ---- 3) mailto fallback (lead never lost) ----
  const mailto =
    "mailto:" +
    TO +
    "?subject=" +
    encodeURIComponent(subject) +
    "&body=" +
    encodeURIComponent(text);
  return json(
    {
      ok: true,
      delivered: "mailto",
      mailto,
      note:
        "询盘已生成邮件草稿，请在下方点击“打开邮件”发送给 " +
        TO +
        "；或直接用 WhatsApp +86 186 5687 1390。",
      to: TO,
      whatsapp: "https://wa.me/" + WHATSAPP,
    },
    200
  );
}

function htmlTable(d) {
  return (
    `<div style="font-family:Arial,sans-serif;color:#1d2733;max-width:560px">` +
    `<h3 style="color:#0b4f8a">新询盘 / New RFQ</h3>` +
    `<table style="border-collapse:collapse;width:100%">` +
    row("姓名", d.name) + row("公司", d.company) + row("邮箱", d.email) +
    row("国家", d.country) + row("意向产品", d.product) +
    `</table>` +
    `<p style="white-space:pre-wrap;background:#f4f7fa;padding:10px;border-radius:6px">${esc(d.message)}</p>` +
    `<p style="color:#5b6b7b;font-size:12px">${esc(d.ts)}</p>` +
    `</div>`
  );
}
function row(label, val) {
  return `<tr><td style="padding:6px 8px;color:#5b6b7b;white-space:nowrap">${label}</td><td style="padding:6px 8px">${esc(val)}</td></tr>`;
}

function str(v) {
  return typeof v === "string" ? v.trim() : v == null ? "" : String(v);
}
function esc(s) {
  return String(s || "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}
function json(obj, status) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json", "Cache-Control": "no-store" },
  });
}

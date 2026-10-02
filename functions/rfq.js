// Cloudflare Pages Function: POST /rfq
//
// Delivers on-site RFQ inquiries to the sales inbox via Zoho SMTP
// (smtp.zoho.com:465, implicit TLS, AUTH LOGIN), using credentials stored in
// Cloudflare Pages environment variable ZOHO_SMTP_PASS.
//
// Fallback: if SMTP send fails, return a mailto: link so the lead is never lost.

import { connect } from "node:tls";

const TO = "changliangliang@sapu-cn.online";
const FROM = "changliangliang@sapu-cn.online";
const WHATSAPP = "8618656871390";
const SMTP_HOST = "smtp.zoho.com";
const SMTP_PORT = 465;

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

  // Honeypot: a hidden field real users never see. Bots that fill it in are
  // dropped silently so they don't trigger a sales email.
  if (str(body.website)) {
    return json({ ok: true, delivered: "none" }, 200);
  }

  if (!email || !message) {
    return json({ ok: false, error: "请至少填写邮箱和留言。" }, 400);
  }

  const ts = new Date().toISOString();
  const subject = `[Sharpen 询盘] ${name || email} — ${product || "RFQ"}`;
  const textBody = [
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

  const pass = env.ZOHO_SMTP_PASS;
  if (pass) {
    try {
      await sendViaZohoSmtp({ user: FROM, pass, subject, text: textBody, html: htmlTable({ name, company, email, country, product, message, ts }) });
      return json({ ok: true, delivered: "email" }, 200);
    } catch (e) {
      return json({
        ok: true,
        delivered: "mailto",
        mailto: mailtoOf(subject, textBody),
        note: "邮件服务暂不可用(" + e.message + ")，请改用下方邮件链接或 WhatsApp +86 186 5687 1390。",
        to: TO,
        whatsapp: "https://wa.me/" + WHATSAPP,
      }, 200);
    }
  }

  // No SMTP credential configured — mailto fallback (lead never lost).
  return json({
    ok: true,
    delivered: "mailto",
    mailto: mailtoOf(subject, textBody),
    note: "询盘已生成邮件草稿，请点下方按钮发送给 " + TO + "；或用 WhatsApp +86 186 5687 1390。",
    to: TO,
    whatsapp: "https://wa.me/" + WHATSAPP,
  }, 200);
}

// ---- Minimal Zoho SMTP over TLS (implicit 465, AUTH LOGIN) ----
function sendViaZohoSmtp({ user, pass, subject, text, html }) {
  return new Promise((resolve, reject) => {
    let buf = "";
    let state = 0;
    const socket = connect({ host: SMTP_HOST, port: SMTP_PORT, servername: SMTP_HOST }, () => {
      socket.on("data", (chunk) => {
        buf += chunk.toString("utf8");
        let idx;
        while ((idx = buf.indexOf("\r\n")) !== -1) {
          const line = buf.slice(0, idx);
          buf = buf.slice(idx + 2);
          handle(line);
        }
      });
      socket.on("error", (e) => { socket.destroy(); reject(e); });
      socket.setTimeout(20000, () => { socket.destroy(); reject(new Error("smtp timeout")); });

      function handle(line) {
        const code = line.slice(0, 3);
        switch (state) {
          case 0: if (code === "220") { socket.write("EHLO sharpen.local\r\n"); state = 1; } break;
          case 1: if (code === "250") { socket.write("AUTH LOGIN\r\n"); state = 2; } break;
          case 2: if (code === "334") { socket.write(Buffer.from(user).toString("base64") + "\r\n"); state = 3; } break;
          case 3: if (code === "334") { socket.write(Buffer.from(pass).toString("base64") + "\r\n"); state = 4; } break;
          case 4:
            if (code === "235") { socket.write("MAIL FROM:<" + user + ">\r\n"); state = 5; }
            else if (code === "535" || code === "5") { finish("auth failed: " + line); }
            break;
          case 5: if (code === "250") { socket.write("RCPT TO:<" + TO + ">\r\n"); state = 6; } break;
          case 6: if (code === "250") {
            const data =
              "Date: " + new Date().toUTCString() + "\r\n" +
              "From: Sharpen Export <" + user + ">\r\n" +
              "To: " + TO + "\r\n" +
              "Subject: " + b64Header(subject) + "\r\n" +
              "MIME-Version: 1.0\r\n" +
              'Content-Type: multipart/alternative; boundary="SHARPEN_ALT"\r\n\r\n' +
              '--SHARPEN_ALT\r\nContent-Type: text/plain; charset="UTF-8"\r\n\r\n' + text + "\r\n" +
              '--SHARPEN_ALT\r\nContent-Type: text/html; charset="UTF-8"\r\n\r\n' + html + "\r\n" +
              '--SHARPEN_ALT--\r\n.\r\n';
            socket.write("DATA\r\n");
            state = 7;
            // Wait for 354 then send data — but write in one go (TCP ordering preserved)
            socket.write(data);
          } break;
          case 7:
            if (code === "354") { socket.write("QUIT\r\n"); state = 8; }
            else if (code === "250") { finish(null); }
            else if (code === "5") { finish("smtp data error: " + line); }
            break;
          case 8: if (code === "250" || code === "221") { finish(null); } break;
        }
      }
      function finish(err) {
        socket.end();
        if (err) reject(new Error(err)); else resolve();
      }
    });
  });
}

function b64Header(s) {
  return "=?UTF-8?B?" + Buffer.from(s, "utf8").toString("base64") + "?=";
}
function mailtoOf(subject, text) {
  return "mailto:" + TO + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(text);
}
function htmlTable(d) {
  return (
    '<div style="font-family:Arial,sans-serif;color:#1d2733;max-width:560px">' +
    '<h3 style="color:#0b4f8a">新询盘 / New RFQ</h3>' +
    '<table style="border-collapse:collapse;width:100%">' +
    row("姓名", d.name) + row("公司", d.company) + row("邮箱", d.email) +
    row("国家", d.country) + row("意向产品", d.product) + "</table>" +
    '<p style="white-space:pre-wrap;background:#f4f7fa;padding:10px;border-radius:6px">' + esc(d.message) + "</p>" +
    '<p style="color:#5b6b7b;font-size:12px">' + esc(d.ts) + "</p>" + "</div>"
  );
}
function row(label, val) {
  return '<tr><td style="padding:6px 8px;color:#5b6b7b;white-space:nowrap">' + label + '</td><td style="padding:6px 8px">' + esc(val) + "</td></tr>";
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

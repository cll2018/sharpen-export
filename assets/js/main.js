// Site interactions: RFQ form submission (POST /rfq -> changliangliang@sapu-cn.online)
// + mobile nav.
//
// Delivery happens server-side via Cloudflare Pages Function, then Zoho SMTP.
// This keeps Zoho credentials out of the browser.
(function () {
  "use strict";

  var INBOX = "changliangliang@sapu-cn.online";
  var WHATSAPP = "https://wa.me/8618656871390";

  function rfqEndpoint() {
    return "/rfq";
  }

  document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("rfqForm");
    if (!form) return;
    var msg = document.getElementById("rfqMsg");
    var okText =
      form.dataset.ok ||
      "Thanks! Your inquiry has been sent. We'll reply shortly.";
    var errText =
      form.dataset.err ||
      "Something went wrong. Please email " + INBOX + " or use WhatsApp.";

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var fd = new FormData(form);
      var payload = {};
      fd.forEach(function (v, k) { payload[k] = v; });

      // Client-side honeypot: never submit if the hidden field is filled.
      if (payload.website) { return; }

      var btn = form.querySelector('button[type="submit"]');
      var prevLabel = btn ? btn.textContent : "";
      if (btn) { btn.disabled = true; btn.textContent = "提交中…"; }

      function showOk(html) { msg.className = "form-msg ok"; msg.innerHTML = html; }
      function showErr(text) { msg.className = "form-msg err"; msg.textContent = text; }
      function done() { if (btn) { btn.disabled = false; btn.textContent = prevLabel; } }

      var lead =
        '<div style="margin-top:8px;display:flex;gap:8px;flex-wrap:wrap">' +
        '<a class="btn btn-primary" style="text-decoration:none" target="_blank" rel="noopener" href="mailto:' + INBOX + '?subject=' +
        encodeURIComponent("[Sharpen 询盘] " + (payload.name || "") + " — " + (payload.product || "RFQ")) +
        ' body=' +
        encodeURIComponent(
          "姓名: " + (payload.name || "") + "\n公司: " + (payload.company || "") +
          "\n邮箱: " + (payload.email || "") + "\n国家: " + (payload.country || "") +
          "\n意向产品: " + (payload.product || "") + "\n留言: " + (payload.message || "")
        ) + '">📧 发邮件到 ' + INBOX + '</a>' +
        '<a class="btn" style="text-decoration:none;background:#25d366;color:#fff" target="_blank" rel="noopener" href="' + WHATSAPP + '">💬 WhatsApp</a></div>';

      fetch(rfqEndpoint(), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      })
      .then(function (res) {
        if (!res.ok) throw new Error("HTTP " + res.status);
        return res.json();
      })
      .then(function (res) {
        form.reset();
        var note = res.note || "";
        showOk(okText + (note ? '<div style="margin-top:8px;color:#5b6b7b">' + note + lead + '</div>' : ""));
      })
      .catch(function (err) {
        showErr(errText + " " + lead + (err && err.message ? "（" + err.message + "）" : ""));
      })
      .finally(done);
    });
  });
})();

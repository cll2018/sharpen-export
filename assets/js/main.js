// Site interactions: RFQ form submission (Cloudflare Function /rfq -> email)
// + mobile nav.
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("rfqForm");
    if (!form) return;
    var msg = document.getElementById("rfqMsg");
    var okText =
      form.dataset.ok ||
      "Thanks! Your inquiry has been sent. We'll reply shortly.";
    var errText =
      form.dataset.err ||
      "Something went wrong. Please email us directly or use WhatsApp.";

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var fd = new FormData(form);
      var payload = {};
      fd.forEach(function (v, k) { payload[k] = v; });
      var btn = form.querySelector('button[type="submit"]');
      var prevLabel = btn ? btn.textContent : "";
      if (btn) { btn.disabled = true; btn.textContent = "提交中…"; }

      fetch("/rfq", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })
        .then(function (r) { return r.json(); })
        .then(function (res) {
          if (res && res.ok) {
            form.reset();
            if (res.delivered === "email" || res.delivered === "archived") {
              msg.className = "form-msg ok";
              msg.innerHTML =
                (res.note ? res.note + " " : "") + okText;
              msg.innerHTML = okText;
              if (res.delivered === "archived" && res.note) {
                msg.innerHTML =
                  res.note + " <br><small>（可直接邮件：" +
                  (res.to || "changliangliang@sapu-cn.online") +
                  " 或 WhatsApp）</small>";
              }
            } else if (res.delivered === "mailto" && res.mailto) {
              // Email Worker / R2 未配置 —— 引导访客用自带邮件客户端
              msg.className = "form-msg ok";
              msg.innerHTML =
                "我们已为您生成邮件草稿，点击下方按钮即可完成发送：" +
                '<div style="margin-top:8px;display:flex;gap:8px;flex-wrap:wrap">' +
                '<a class="btn btn-primary" style="text-decoration:none" href="' +
                res.mailto + '">📧 打开邮件发送给 ' +
                (res.to || "changliangliang@sapu-cn.online") +
                "</a>" +
                '<a class="btn" style="text-decoration:none;background:#25d366;color:#fff" target="_blank" rel="noopener" href="' +
                (res.whatsapp || "https://wa.me/8618656871390") +
                '">💬 或 WhatsApp</a></div>';
            } else {
              msg.className = "form-msg ok";
              msg.textContent = okText;
            }
          } else {
            msg.className = "form-msg err";
            msg.textContent = (res && res.error) || errText;
          }
        })
        .catch(function () {
          msg.className = "form-msg err";
          msg.textContent = errText;
        })
        .finally(function () {
          if (btn) { btn.disabled = false; btn.textContent = prevLabel; }
        });
    });
  });
})();

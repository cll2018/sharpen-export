// Site interactions: RFQ form submission (EmailJS -> changliangliang@sapu-cn.online)
// + mobile nav.
//
// EmailJS config (fill in after https://emailjs.com / https://formspark.io).
// FREE: 200 requests/month — plenty for a B2B inquiry site.
(function () {
  "use strict";

  // ----- EmailJS config -----
  var EMAILJS_SERVICE_ID = "sapu";                       // 你在 EmailJS 里配的服务 ID
  var EMAILJS_TEMPLATE_ID = "YOUR_TEMPLATE_ID";           // 在 EmailJS 后台 "Templates" 里复制 template_xxx
  var EMAILJS_PUBLIC_KEY = "xc4UpP8S4E-QHoSpw";          // 你的 public key
  var EMAILJS_PRIVATE_KEY = "3YHHysFfcXfWrkRykjy6m";     // private key, 仅本地保留

  var INBOX = "changliangliang@sapu-cn.online";
  var WHATSAPP = "https://wa.me/8618656871390";

  function configured() {
    return (
      EMAILJS_SERVICE_ID &&
      EMAILJS_TEMPLATE_ID &&
      EMAILJS_PUBLIC_KEY &&
      EMAILJS_SERVICE_ID.indexOf("YOUR_") !== 0 &&
      EMAILJS_TEMPLATE_ID.indexOf("YOUR_") !== 0 &&
      EMAILJS_PUBLIC_KEY.indexOf("YOUR_") !== 0
    );
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

      if (!configured()) {
        showOk("询盘已生成邮件草稿，点击下方按钮即可完成发送：" + lead);
        return;
      }

      // Load EmailJS if not present
      if (!window.emailjs) {
        var s = document.createElement("script");
        s.src = "https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js";
        s.async = true;
        s.onload = function () { doSend(); };
        s.onerror = function () {
          showErr(errText);
          done();
        };
        document.head.appendChild(s);
      } else {
        doSend();
      }

      function doSend() {
        window.emailjs.init(EMAILJS_PUBLIC_KEY);
        window.emailjs
          .send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, {
            from_name: payload.name || "",
            from_email: payload.email || "",
            company: payload.company || "",
            country: payload.country || "",
            product: payload.product || "",
            message: payload.message || "",
            to: INBOX,
          })
          .then(function () {
            form.reset();
            showOk(okText);
          })
          .catch(function (err) {
            showErr("提交未成功，请改用邮件或 WhatsApp：" + lead + (err && err.message ? "（" + err.message + "）" : ""));
          })
          .finally(done);
      }
    });
  });
})();

// Site interactions: RFQ form submission (POST /rfq -> changliangliang@sapu-cn.online)
// + mobile nav.
//
// Delivery happens server-side via Cloudflare Pages Function, then Zoho SMTP.
// This keeps Zoho credentials out of the browser.
(function () {
  "use strict";

  var INBOX = "changliangliang@sapu-cn.online";
  var WHATSAPP = "https://wa.me/8618656871390";

  // Shown when /rfq refuses a submission because this network has hit the
  // per-IP limit (see functions/_lib/rate-limit.js). Kept here as a small table
  // rather than in the 14 contact.md files, so the wording can change without
  // touching the zh -> 13 languages content pipeline.
  var BLOCKED = {
    "zh": "提交过于频繁，已被临时拦截。请稍后再试，或直接发邮件 / WhatsApp 联系我们。",
    "zh-tw": "提交過於頻繁，已被暫時攔截。請稍後再試，或直接以電子郵件 / WhatsApp 聯絡我們。",
    "en": "Too many submissions from your network. Please try again later, or email / WhatsApp us directly.",
    "de": "Zu viele Anfragen von Ihrem Netzwerk. Bitte versuchen Sie es später erneut oder kontaktieren Sie uns direkt per E-Mail / WhatsApp.",
    "ja": "送信が多すぎます。しばらくしてから再試行するか、メール / WhatsApp でご連絡ください。",
    "ko": "제출이 너무 많습니다. 잠시 후 다시 시도하시거나 이메일 / WhatsApp으로 연락해 주세요.",
    "ru": "Слишком много заявок с вашей сети. Попробуйте позже или напишите нам по электронной почте / WhatsApp.",
    "es": "Demasiados envíos desde su red. Inténtelo más tarde o escríbanos por correo electrónico / WhatsApp.",
    "pt": "Demasiados envios da sua rede. Tente novamente mais tarde ou contacte-nos por e-mail / WhatsApp.",
    "fr": "Trop d'envois depuis votre réseau. Réessayez plus tard ou écrivez-nous par e-mail / WhatsApp.",
    "it": "Troppi invii dalla tua rete. Riprova più tardi o scrivici via e-mail / WhatsApp.",
    "tr": "Ağınızdan çok fazla gönderim yapıldı. Lütfen daha sonra tekrar deneyin veya bize e-posta / WhatsApp ile ulaşın.",
    "ar": "عدد كبير جدًا من الطلبات من شبكتكم. يرجى المحاولة لاحقًا أو مراسلتنا عبر البريد الإلكتروني / واتساب.",
    "vi": "Có quá nhiều lần gửi từ mạng của bạn. Vui lòng thử lại sau hoặc liên hệ qua email / WhatsApp."
  };

  function blockedText() {
    var lang = (document.documentElement.lang || "en").toLowerCase();
    return BLOCKED[lang] || BLOCKED[lang.split("-")[0]] || BLOCKED.en;
  }

  function escapeHtml(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

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
      // `lead` is markup (the mailto / WhatsApp buttons), so the plain-text part
      // has to be escaped rather than assigned wholesale — the previous version
      // used textContent, which printed the buttons as raw HTML on every error.
      function showErr(text) { msg.className = "form-msg err"; msg.innerHTML = escapeHtml(text) + lead; }
      function showBlocked() {
        msg.className = "form-msg err";
        msg.innerHTML = escapeHtml(blockedText()) + lead;
      }
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
        // Read the body even on a failure status: /rfq explains a block in JSON.
        return res.json().catch(function () { return {}; }).then(function (data) {
          return { status: res.status, data: data };
        });
      })
      .then(function (r) {
        if (r.status === 429) {
          form.reset();
          showBlocked();
          return;
        }
        if (r.status < 200 || r.status >= 300 || r.data.ok === false) {
          throw new Error(r.data.error || ("HTTP " + r.status));
        }
        form.reset();
        var note = r.data.note || "";
        showOk(okText + (note ? '<div style="margin-top:8px;color:#5b6b7b">' + note + lead + '</div>' : ""));
      })
      .catch(function (err) {
        showErr(errText + (err && err.message ? "（" + err.message + "）" : ""));
      })
      .finally(done);
    });
  });
})();

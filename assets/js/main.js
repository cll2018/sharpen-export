// Site interactions: RFQ form submission (Cloudflare Function /rfq -> email)
// + mobile nav.
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    // ---- RFQ form -> Cloudflare /rfq Function (emails changliangliang@sapu-cn.online) ----
    var form = document.getElementById("rfqForm");
    if (form) {
      var msg = document.getElementById("rfqMsg");
      var okText = form.dataset.ok || "Thanks! Your inquiry has been sent. We'll reply shortly.";
      var errText =
        form.dataset.err ||
        "Something went wrong. Please email us directly or use WhatsApp.";
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var fd = new FormData(form);
        var payload = {};
        fd.forEach(function (v, k) { payload[k] = v; });
        var btn = form.querySelector('button[type="submit"]');
        if (btn) { btn.disabled = true; btn.textContent = "提交中…"; }
        fetch("/rfq", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        })
          .then(function (r) { return r.json(); })
          .then(function (res) {
            if (res && res.ok) {
              msg.className = "form-msg ok";
              msg.textContent = okText;
              form.reset();
            } else {
              // Show server-provided guidance (e.g. direct email / WhatsApp).
              msg.className = "form-msg err";
              msg.textContent = (res && res.error) || errText;
            }
          })
          .catch(function () {
            msg.className = "form-msg err";
            msg.textContent = errText;
          })
          .finally(function () {
            if (btn) { btn.disabled = false; btn.textContent = "提交询盘"; }
          });
      });
    }
  });
})();

// Site interactions: RFQ form submission (Web3Forms, no backend) + mobile nav.
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    // ---- RFQ form -> Web3Forms (emails the inquiry, no server needed) ----
    var form = document.getElementById("rfqForm");
    if (form) {
      var msg = document.getElementById("rfqMsg");
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var data = new FormData(form);
        data.append("subject", "New RFQ from Sharpen website");
        data.append("from_name", "Sharpen Website");
        fetch("https://api.web3forms.com/submit", {
          method: "POST",
          body: data,
        })
          .then(function (r) { return r.json(); })
          .then(function (res) {
            if (res.success) {
              msg.className = "form-msg ok";
              msg.textContent =
                form.dataset.ok || "Thanks! Your inquiry has been sent. We'll reply shortly.";
              form.reset();
            } else {
              throw new Error(res.message || "submit failed");
            }
          })
          .catch(function () {
            msg.className = "form-msg err";
            msg.textContent =
              form.dataset.err || "Something went wrong. Please email us directly or use WhatsApp.";
          });
      });
    }
  });
})();

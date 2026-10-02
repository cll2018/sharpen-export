// AI chat widget: opens the panel, talks to the /ai-chat Pages Function,
// which proxies an external (OpenAI-compatible) LLM. Config + API key live in
// data/settings.json (editable in the CMS backend) and the secret key in a
// Cloudflare Pages env var. If AI is disabled, we capture a lead instead.
(function () {
  "use strict";

  var panel = document.getElementById("chat-panel");
  var body = document.getElementById("chat-body");
  var log = document.getElementById("chat-log");
  var form = document.getElementById("chat-form");
  var input = document.getElementById("chat-input");
  var toggles = ["chat-toggle", "chat-toggle-2", "chat-toggle-3"];
  var history = [];
  var minBtn = document.getElementById("chat-min");

  function openChat() {
    if (!panel) return;
    panel.hidden = false;
    // re-expand a collapsed panel
    if (body) body.classList.remove("is-collapsed");
    if (minBtn) minBtn.textContent = "—";
    var t = document.getElementById("chat-toggle");
    if (t) t.setAttribute("aria-expanded", "true");
    if (log && !log.dataset.greeted) {
      log.dataset.greeted = "1";
      addBot(
        window.__sharpenChatWelcome ||
        (document.documentElement.lang === "zh"
          ? "您好！我是萨普的 AI 销售助手，请问有什么可以帮您？（产品、规格、交期、报价都可以问）"
          : "Hi! I'm Sharpen's AI assistant. Ask me about products, specs, lead time or quotes.")
      );
    }
    if (input) input.focus();
  }
  function closeChat() {
    if (!panel) return;
    panel.hidden = true;
    var t = document.getElementById("chat-toggle");
    if (t) t.setAttribute("aria-expanded", "false");
  }
  function toggleMin() {
    if (!panel || !body) return;
    var collapsed = body.classList.toggle("is-collapsed");
    if (minBtn) minBtn.textContent = collapsed ? "+" : "—";
    if (!collapsed && input) input.focus();
  }
  if (minBtn) minBtn.addEventListener("click", toggleMin);
  function addMsg(text, who) {
    var el = document.createElement("div");
    el.className = "chat-msg " + who;
    el.textContent = text;
    log.appendChild(el);
    log.scrollTop = log.scrollHeight;
  }
  var addBot = function (t) { addMsg(t, "bot"); };
  var addUser = function (t) { addMsg(t, "user"); };

  toggles.forEach(function (id) {
    var b = document.getElementById(id);
    if (b) b.addEventListener("click", openChat);
  });
  var closeBtn = document.getElementById("chat-close");
  if (closeBtn) closeBtn.addEventListener("click", closeChat);

  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var text = input.value.trim();
      if (!text) return;
      addUser(text);
      input.value = "";
      history.push({ role: "user", content: text });

      var lang = document.documentElement.lang || "en";
      addBot("…");
      fetch("/ai-chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: history, lang: lang }),
      })
        .then(function (r) { return r.json(); })
        .then(function (res) {
          // remove the "…" placeholder
          if (log.lastChild) log.removeChild(log.lastChild);
          var reply = res.reply || "(no response)";
          addBot(reply);
          history.push({ role: "assistant", content: reply });
          if (res.lead) {
            var wa =
              "https://wa.me/" +
              (window.__sharpenWhatsapp || "");
            var note = document.createElement("div");
            note.className = "chat-msg bot";
            note.innerHTML =
              '📩 <a href="' + wa + '" target="_blank" rel="noopener">WhatsApp</a> · ' +
              '<a href="/' + lang + '/contact/">RFQ form</a>';
            log.appendChild(note);
          }
        })
        .catch(function () {
          if (log.lastChild) log.removeChild(log.lastChild);
          addBot("Network error. Please try WhatsApp or the RFQ form.");
        });
    });
  }
})();

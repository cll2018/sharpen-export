---
layout: page.njk
lang: de
permalink: /de/contact/
title: "Kontakt & Angebot"
description: "Kontaktieren Sie Changsha Sharpen New Materials für Angebote zu Diamant-/CBN-Scheiben, Sinterwerkzeugstahl (PM) und TiNiCo-Wärmeableitern. Sofortige Anfrage per KI-Chat oder WhatsApp."
---

<div class="rfq">
  <div>
    <h2>Anfrage senden</h2>
    <p>Nennen Sie uns Material, Größe, Menge und Anwendung. Wir antworten innerhalb von 1 Arbeitstag.</p>
    <form id="rfqForm" data-ok="Vielen Dank! Ihre Anfrage wurde gesendet. Wir werden uns in Kürze melden." data-err="Etwas ist schiefgelaufen. Bitte kontaktieren Sie uns per E-Mail oder nutzen Sie WhatsApp.">
      <input type="hidden" name="access_key" value="{{ site.web3formsKey }}" />
      <label>Name *<input type="text" name="name" required /></label>
      <label>Firma<input type="text" name="company" /></label>
      <label>E-Mail *<input type="email" name="email" required /></label>
      <label>Land / Region<input type="text" name="country" /></label>
      <label>Interessantes Produkt
        <select name="product">
          <option>Diamantschleifscheiben</option>
          <option>CBN-Schleifscheiben</option>
          <option>Pulvermetallurgischer Hochgeschwindigkeitsstahl</option>
          <option>TiNiCo-Superlegierungswärmeableiter</option>
          <option>Stahlgebundener Hartmetall</option>
          <option>Andere / Unsicher</option>
        </select>
      </label>
      <label>Nachricht *<textarea name="message" required placeholder="Material, Abmessungen, Menge, Anwendung..."></textarea></label>
            <div class="hp-field" aria-hidden="true"><label>Please leave this field empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
      <label class="consent"><input type="checkbox" name="consent" required /> Ich stimme zu, bezüglich meiner Anfrage kontaktiert zu werden.</label>
<button class="btn btn-primary" type="submit">Anfrage senden</button>
      <div id="rfqMsg" class="form-msg" role="status"></div>
    </form>
  </div>
  <div class="contact-info">
    <h2>Direktkontakt</h2>
    <p><strong>WhatsApp:</strong> <a href="https://wa.me/{{ site.whatsapp }}" target="_blank" rel="noopener">wa.me/{{ site.whatsapp }}</a></p>
    <p><strong>E-Mail:</strong> <a href="mailto:{{ site.email }}">{{ site.email }}</a></p>
    <p><strong>Telefon:</strong> {{ site.phone }}</p>
    <p><strong>WeChat:</strong> {{ site.wechat }}</p>
    <p><strong>Adresse:</strong> {{ site.address }}</p>
    <p style="margin-top:18px"><a class="btn btn-chat" href="#" onclick="document.getElementById('chat-toggle').click();return false;">💬 KI-Chat (sofort)</a></p>
  </div>
</div>
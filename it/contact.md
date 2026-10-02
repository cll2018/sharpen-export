---
layout: page.njk
lang: it
permalink: /it/contact/
title: "Contatti e Richiesta di preventivo"
description: "Contatta Changsha Sharpen New Materials per i preventivi di mole diamantate/CBN, acciai rapidi a sinterizzazione e spreaders termici in TiNiCo. Richiesta in tempo reale tramite chat AI o WhatsApp."
---

<div class="rfq">
  <div>
    <h2>Invia una richiesta di preventivo</h2>
    <p>Indicanoci materiale, dimensioni, quantità e applicazione. Rispondiamo entro 1 giorno lavorativo.</p>
    <form id="rfqForm" data-ok="Grazie! La tua richiesta è stata inviata. Ti risponderemo a breve." data-err="Qualcosa è andato storto. Ti preghiamo di inviarci un'e-mail direttamente o di utilizzare WhatsApp.">
      <input type="hidden" name="access_key" value="{{ site.web3formsKey }}" />
      <label>Nome *<input type="text" name="name" required /></label>
      <label>Azienda<input type="text" name="company" /></label>
      <label>E-mail *<input type="email" name="email" required /></label>
      <label>Paese / Regione<input type="text" name="country" /></label>
      <label>Prodotto di interesse
        <select name="product">
          <option>Carburo con lega di acciaio</option>
          <option>Mole diamantate per rettifica</option>
          <option>Mole CBN per rettifica</option>
          <option>Acci rapidi a sinterizzazione (PM)</option>
          <option>Spreaders termici in superlega TiNiCo</option>
          <option>Altro / Non sono sicuro</option>
        </select>
      </label>
      <label>Messaggio *<textarea name="message" required placeholder="Materiale, dimensioni, quantità, applicazione..."></textarea></label>
      <button class="btn btn-primary" type="submit">Invia la richiesta</button>
      <div id="rfqMsg" class="form-msg" role="status"></div>
    </form>
  </div>
  <div class="contact-info">
    <h2>Contatti diretti</h2>
    <p><strong>WhatsApp:</strong> <a href="https://wa.me/{{ site.whatsapp }}" target="_blank" rel="noopener">wa.me/{{ site.whatsapp }}</a></p>
    <p><strong>E-mail:</strong> <a href="mailto:{{ site.email }}">{{ site.email }}</a></p>
    <p><strong>Telefono:</strong> {{ site.phone }}</p>
    <p><strong>WeChat:</strong> {{ site.wechat }}</p>
    <p><strong>Indirizzo:</strong> {{ site.address }}</p>
    <p style="margin-top:18px"><a class="btn btn-chat" href="#" onclick="document.getElementById('chat-toggle').click();return false;">💬 Chat AI (immediata)</a></p>
  </div>
</div>
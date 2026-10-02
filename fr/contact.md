---
layout: page.njk
lang: fr
permalink: /fr/contact/
title: "Contact et demande de devis"
description: "Contactez Changsha Sharpen New Materials pour obtenir des devis sur les meules diamant/CBN, les aciers rapides haute vitesse en fonderie de poudres (PM) et les diffuseurs de chaleur en superalliage TiNiCo. Demande en temps réel via chat IA ou WhatsApp."
---

<div class="rfq">
  <div>
    <h2>Envoyer une demande de devis</h2>
    <p>Indiquez-nous votre matériau, vos dimensions, la quantité et l'application. Nous répondons sous 1 jour ouvrable.</p>
    <form id="rfqForm" data-ok="Merci ! Votre demande a été envoyée. Nous vous répondrons sous peu." data-err="Une erreur s'est produite. Veuillez nous envoyer un e-mail directement ou utiliser WhatsApp.">
      <input type="hidden" name="access_key" value="{{ site.web3formsKey }}" />
      <label>Nom *<input type="text" name="name" required /></label>
      <label>Société<input type="text" name="company" /></label>
      <label>E-mail *<input type="email" name="email" required /></label>
      <label>Pays / Région<input type="text" name="country" /></label>
      <label>Produit d'intérêt
        <select name="product">
          <option>Meules de meulage diamant</option>
          <option>Meules de meulage CBN</option>
          <option>Acier rapide haute vitesse en métallurgie des poudres</option>
          <option>Diffuseur de chaleur en superalliage TiNiCo</option>
          <option>Autre / Incertain</option>
        </select>
      </label>
      <label>Message *<textarea name="message" required placeholder="Matériau, dimensions, quantité, application..."></textarea></label>
      <button class="btn btn-primary" type="submit">Envoyer la demande</button>
      <div id="rfqMsg" class="form-msg" role="status"></div>
    </form>
  </div>
  <div class="contact-info">
    <h2>Contact direct</h2>
    <p><strong>WhatsApp :</strong> <a href="https://wa.me/{{ site.whatsapp }}" target="_blank" rel="noopener">wa.me/{{ site.whatsapp }}</a></p>
    <p><strong>E-mail :</strong> <a href="mailto:{{ site.email }}">{{ site.email }}</a></p>
    <p><strong>Tél :</strong> {{ site.phone }}</p>
    <p><strong>WeChat :</strong> {{ site.wechat }}</p>
    <p><strong>Adresse :</strong> {{ site.address }}</p>
    <p style="margin-top:18px"><a class="btn btn-chat" href="#" onclick="document.getElementById('chat-toggle').click();return false;">💬 Chat IA (immédiat)</a></p>
  </div>
</div>
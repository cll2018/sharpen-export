---
layout: page.njk
lang: es
permalink: /es/contact/
title: "Contacto y presupuesto"
description: "Contacte a Changsha Sharpen New Materials para obtener presupuestos sobre discos de diamante/CBN, acero rapidometalúrgico y disipadores de calor TiNiCo. Consulta en tiempo real mediante chat de IA o WhatsApp."
---

<div class="rfq">
  <div>
    <h2>Enviar un presupuesto</h2>
    <p>Indíquenos su material, tamaño, cantidad y aplicación. Respondemos en un día hábil.</p>
    <form id="rfqForm" data-ok="¡Gracias! Su consulta ha sido enviada. Le responderemos en breve." data-err="Algo salió mal. Por favor, envíenos un correo electrónico directamente o utilice WhatsApp.">
      <input type="hidden" name="access_key" value="{{ site.web3formsKey }}" />
      <label>Nombre *<input type="text" name="name" required /></label>
      <label>Empresa<input type="text" name="company" /></label>
      <label>Correo electrónico *<input type="email" name="email" required /></label>
      <label>País / Región<input type="text" name="country" /></label>
      <label>Producto de interés
        <select name="product">
          <option>Carburo con ligante de acero</option>
          <option>Discos de pulido de diamante</option>
          <option>Discos de pulido de CBN</option>
          <option>Acero rapidometalúrgico (PM)</option>
          <option>Disipador de calor de superaleación TiNiCo</option>
          <option>Otro / No seguro</option>
        </select>
      </label>
      <label>Mensaje *<textarea name="message" required placeholder="Material, dimensiones, cantidad, aplicación..."></textarea></label>
      <button class="btn btn-primary" type="submit">Enviar consulta</button>
      <div id="rfqMsg" class="form-msg" role="status"></div>
    </form>
  </div>
  <div class="contact-info">
    <h2>Directo</h2>
    <p><strong>WhatsApp:</strong> <a href="https://wa.me/{{ site.whatsapp }}" target="_blank" rel="noopener">wa.me/{{ site.whatsapp }}</a></p>
    <p><strong>Correo electrónico:</strong> <a href="mailto:{{ site.email }}">{{ site.email }}</a></p>
    <p><strong>Teléfono:</strong> {{ site.phone }}</p>
    <p><strong>WeChat:</strong> {{ site.wechat }}</p>
    <p><strong>Dirección:</strong> {{ site.address }}</p>
    <p style="margin-top:18px"><a class="btn btn-chat" href="#" onclick="document.getElementById('chat-toggle').click();return false;">💬 Chat de IA (inmediato)</a></p>
  </div>
</div>

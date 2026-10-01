---
layout: page.njk
lang: it
permalink: /it/contact/
title: "Contact & RFQ"
description: "Contact Changsha Sharpen New Materials for quotes on diamond/CBN wheels, PM high-speed steel and TiNiCo heat spreaders. Real-time inquiry via AI chat or WhatsApp."
---

<div class="rfq">
  <div>
    <h2>Send an RFQ</h2>
    <p>Tell us your material, size, quantity and application. We reply within 1 business day.</p>
    <form id="rfqForm" data-ok="Thanks! Your inquiry has been sent. We'll reply shortly." data-err="Something went wrong. Please email us directly or use WhatsApp.">
      <input type="hidden" name="access_key" value="{{ site.web3formsKey }}" />
      <label>Name *<input type="text" name="name" required /></label>
      <label>Company<input type="text" name="company" /></label>
      <label>Email *<input type="email" name="email" required /></label>
      <label>Country / Region<input type="text" name="country" /></label>
      <label>Product of interest
        <select name="product">
          <option>Diamond Grinding Wheels</option>
          <option>CBN Grinding Wheels</option>
          <option>Powder Metallurgy High-Speed Steel</option>
          <option>TiNiCo Superalloy Heat Spreader</option>
          <option>Other / Not sure</option>
        </select>
      </label>
      <label>Message *<textarea name="message" required placeholder="Material, dimensions, quantity, application..."></textarea></label>
      <button class="btn btn-primary" type="submit">Submit Inquiry</button>
      <div id="rfqMsg" class="form-msg" role="status"></div>
    </form>
  </div>
  <div class="contact-info">
    <h2>Direct</h2>
    <p><strong>WhatsApp:</strong> <a href="https://wa.me/{{ site.whatsapp }}" target="_blank" rel="noopener">wa.me/{{ site.whatsapp }}</a></p>
    <p><strong>Email:</strong> <a href="mailto:{{ site.email }}">{{ site.email }}</a></p>
    <p><strong>Tel:</strong> {{ site.phone }}</p>
    <p><strong>Address:</strong> {{ site.address }}</p>
    <p style="margin-top:18px"><a class="btn btn-chat" href="#" onclick="document.getElementById('chat-toggle').click();return false;">💬 AI Chat (instant)</a></p>
  </div>
</div>

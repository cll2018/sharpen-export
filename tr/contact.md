---
layout: page.njk
lang: tr
permalink: /tr/contact/
title: "İletişim ve Teklif Talebi"
description: "Elmas/CBN tekerlekleri, toz metalurjisi yüksek hızlı çelik ve TiNiCo ısı dağıtıcıları için Changsha Sharpen New Materials'ten fiyat teklifi alın. Gerçek zamanlı başvuru için yapay zeka sohbeti veya WhatsApp kullanın."
---

<div class="rfq">
  <div>
    <h2>Teklif Talebi Gönderin</h2>
    <p>Malzemeniz, boyutu, miktarı ve uygulaması hakkında bize bilgi verin. 1 iş günü içinde yanıt veririz.</p>
    <form id="rfqForm" data-ok="Teşekkürler! Başvurunuz gönderildi. Kısa süre içinde yanıt vereceğiz." data-err="Bir şeyler ters gitti. Lütfen bize doğrudan e-posta gönderin veya WhatsApp kullanın.">
      <input type="hidden" name="access_key" value="{{ site.web3formsKey }}" />
      <label>Ad *<input type="text" name="name" required /></label>
      <label>Şirket<input type="text" name="company" /></label>
      <label>E-posta *<input type="email" name="email" required /></label>
      <label>Ülke / Bölge<input type="text" name="country" /></label>
      <label>İlgi duyduğunuz ürün
        <select name="product">
          <option>Elmas Taşlama Tekerlekleri</option>
          <option>CBN Taşlama Tekerlekleri</option>
          <option>Toz Metalurjisi Yüksek Hızlı Çelik</option>
          <option>TiNiCo Süper Alaşım Isı Dağıtıcı</option>
          <option>Diğer / Emin Değilim</option>
        </select>
      </label>
      <label>Mesaj *<textarea name="message" required placeholder="Malzeme, boyutlar, miktar, uygulama..."></textarea></label>
      <button class="btn btn-primary" type="submit">Başvuruyu Gönder</button>
      <div id="rfqMsg" class="form-msg" role="status"></div>
    </form>
  </div>
  <div class="contact-info">
    <h2>Direkt</h2>
    <p><strong>WhatsApp:</strong> <a href="https://wa.me/{{ site.whatsapp }}" target="_blank" rel="noopener">wa.me/{{ site.whatsapp }}</a></p>
    <p><strong>E-posta:</strong> <a href="mailto:{{ site.email }}">{{ site.email }}</a></p>
    <p><strong>Telefon:</strong> {{ site.phone }}</p>
    <p><strong>WeChat:</strong> {{ site.wechat }}</p>
    <p><strong>Adres:</strong> {{ site.address }}</p>
    <p style="margin-top:18px"><a class="btn btn-chat" href="#" onclick="document.getElementById('chat-toggle').click();return false;">💬 Yapay Zeka Sohbeti (anında)</a></p>
  </div>
</div>
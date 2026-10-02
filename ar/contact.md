---
layout: page.njk
lang: ar
permalink: /ar/contact/
title: "الاتصال واستفسار متطلبات الشراء"
description: "تواصل مع Changsha Sharpen New Materials للحصول على أسعار لأقراص اللياسة الماسية/CBN، الفولاذ السريع عالي السرعة بالمعالجة بالفريز، ومُوزِّعات حرارية من TiNiCo. استفسار فوري عبر الدردشة الذكية أو واتساب."
---

<div class="rfq">
  <div>
    <h2>إرسال استفسار متطلبات شراء</h2>
    <p>أخبرنا عن المادة، والحجم، والكمية، وتطبيق الاستخدام. نرد خلال يوم عمل واحد.</p>
    <form id="rfqForm" data-ok="شكرًا لك! تم إرسال استفسارك. سنرد عليك قريبًا." data-err="حدث خطأ ما. يرجى مراسلتنا مباشرة عبر البريد الإلكتروني أو استخدام واتساب.">
      <input type="hidden" name="access_key" value="{{ site.web3formsKey }}" />
      <label>الاسم *<input type="text" name="name" required /></label>
      <label>الشركة<input type="text" name="company" /></label>
      <label>البريد الإلكتروني *<input type="email" name="email" required /></label>
      <label>الدولة / المنطقة<input type="text" name="country" /></label>
      <label>المنتج محل الاهتمام
        <select name="product">
          <option>كربيد مربوط بالصلب</option>
          <option>أقراص لياسة ماسية</option>
          <option>أقراص لياسة CBN</option>
          <option>فولاذ سريع عالي السرعة بالمعالجة بالفريز</option>
          <option>مُوزِّع حراري من سبيكة TiNiCo فائقة التحمل</option>
          <option>أخرى / غير متأكد</option>
        </select>
      </label>
      <label>الرسالة *<textarea name="message" required placeholder="المادة، الأبعاد، الكمية، تطبيق الاستخدام..."></textarea></label>
      <button class="btn btn-primary" type="submit">إرسال الاستفسار</button>
      <div id="rfqMsg" class="form-msg" role="status"></div>
    </form>
  </div>
  <div class="contact-info">
    <h2>اتصال مباشر</h2>
    <p><strong>واتساب:</strong> <a href="https://wa.me/{{ site.whatsapp }}" target="_blank" rel="noopener">wa.me/{{ site.whatsapp }}</a></p>
    <p><strong>البريد الإلكتروني:</strong> <a href="mailto:{{ site.email }}">{{ site.email }}</a></p>
    <p><strong>الهاتف:</strong> {{ site.phone }}</p>
    <p><strong>وي تشات:</strong> {{ site.wechat }}</p>
    <p><strong>العنوان:</strong> {{ site.address }}</p>
    <p style="margin-top:18px"><a class="btn btn-chat" href="#" onclick="document.getElementById('chat-toggle').click();return false;">💬 دردشة ذكية (فورية)</a></p>
  </div>
</div>
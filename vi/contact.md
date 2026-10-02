---
layout: page.njk
lang: vi
permalink: /vi/contact/
title: "Liên hệ & Yêu cầu báo giá"
description: "Liên hệ Changsha Sharpen New Materials để được báo giá về bánh mài kim cương/CBN, thép tốc độ cao PM và dàn tản nhiệt TiNiCo. Nhận tư vấn theo thời gian thực qua AI chat hoặc WhatsApp."
---

<div class="rfq">
  <div>
    <h2>Gửi yêu cầu báo giá</h2>
    <p>Vui lòng cung cấp cho chúng tôi loại vật liệu, kích thước, số lượng và ứng dụng. Chúng tôi sẽ phản hồi trong vòng 1 ngày làm việc.</p>
    <form id="rfqForm" data-ok="Cảm ơn! Yêu cầu của bạn đã được gửi. Chúng tôi sẽ phản hồi sớm." data-err="Đã xảy ra lỗi. Vui lòng gửi email trực tiếp cho chúng tôi hoặc sử dụng WhatsApp.">
      <input type="hidden" name="access_key" value="{{ site.web3formsKey }}" />
      <label>Tên *<input type="text" name="name" required /></label>
      <label>Công ty<input type="text" name="company" /></label>
      <label>Email *<input type="email" name="email" required /></label>
      <label>Quốc gia / Khu vực<input type="text" name="country" /></label>
      <label>Sản phẩm quan tâm
        <select name="product">
          <option>Thép kết hợp với hạt cứng</option>
          <option>Bánh mài kim cương</option>
          <option>Bánh mài CBN</option>
          <option>Thép tốc độ cao luyện粉末</option>
          <option>Dàn tản nhiệt hợp kim siêu TiNiCo</option>
          <option>Khác / Chưa rõ</option>
        </select>
      </label>
      <label>Nhắn *<textarea name="message" required placeholder="Vật liệu, kích thước, số lượng, ứng dụng..."></textarea></label>
      <button class="btn btn-primary" type="submit">Gửi yêu cầu</button>
      <div id="rfqMsg" class="form-msg" role="status"></div>
    </form>
  </div>
  <div class="contact-info">
    <h2>Liên hệ trực tiếp</h2>
    <p><strong>WhatsApp:</strong> <a href="https://wa.me/{{ site.whatsapp }}" target="_blank" rel="noopener">wa.me/{{ site.whatsapp }}</a></p>
    <p><strong>Email:</strong> <a href="mailto:{{ site.email }}">{{ site.email }}</a></p>
    <p><strong>Điện thoại:</strong> {{ site.phone }}</p>
    <p><strong>WeChat:</strong> {{ site.wechat }}</p>
    <p><strong>Địa chỉ:</strong> {{ site.address }}</p>
    <p style="margin-top:18px"><a class="btn btn-chat" href="#" onclick="document.getElementById('chat-toggle').click();return false;">💬 AI Chat (liền tức)</a></p>
  </div>
</div>
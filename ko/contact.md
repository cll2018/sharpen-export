---
layout: page.njk
lang: ko
permalink: /ko/contact/
title: "문의 및 견적 요청"
description: "치앙사 샤브펜 신소재에서 다이아몬드/CBN 휠, PM 고속강합금, TiNiCo 열 확산체에 대한 견적을 문의하세요. AI 채팅 또는 WhatsApp으로 실시간 문의가 가능합니다."
---

<div class="rfq">
  <div>
    <h2>견적 요청</h2>
    <p>재료, 크기, 수량 및 용도를 알려주세요. 영업일 1일 이내에 회신드립니다.</p>
    <form id="rfqForm" data-ok="감사합니다! 문의가 전송되었습니다. 조만간 회신드리겠습니다." data-err="문제가 발생했습니다. 이메일 또는 WhatsApp을 이용해 주세요.">
      <input type="hidden" name="access_key" value="{{ site.web3formsKey }}" />
      <label>이름 *<input type="text" name="name" required /></label>
      <label>회사명<input type="text" name="company" /></label>
      <label>이메일 *<input type="email" name="email" required /></label>
      <label>국가 / 지역<input type="text" name="country" /></label>
      <label>관심 제품
        <select name="product">
          <option>다이아몬드 연삭 휠</option>
          <option>CBN 연삭 휠</option>
          <option>분말 야금 고속강합금</option>
          <option>TiNiCo 합금 열 확산체</option>
          <option>기타 / 모름</option>
        </select>
      </label>
      <label>메시지 *<textarea name="message" required placeholder="재료, 치수, 수량, 용도..."></textarea></label>
      <button class="btn btn-primary" type="submit">문의 제출</button>
      <div id="rfqMsg" class="form-msg" role="status"></div>
    </form>
  </div>
  <div class="contact-info">
    <h2>직접 연락</h2>
    <p><strong>WhatsApp:</strong> <a href="https://wa.me/{{ site.whatsapp }}" target="_blank" rel="noopener">wa.me/{{ site.whatsapp }}</a></p>
    <p><strong>이메일:</strong> <a href="mailto:{{ site.email }}">{{ site.email }}</a></p>
    <p><strong>전화:</strong> {{ site.phone }}</p>
    <p><strong>WeChat:</strong> {{ site.wechat }}</p>
    <p><strong>주소:</strong> {{ site.address }}</p>
    <p style="margin-top:18px"><a class="btn btn-chat" href="#" onclick="document.getElementById('chat-toggle').click();return false;">💬 AI 채팅 (즉시)</a></p>
  </div>
</div>
---
layout: page.njk
lang: zh-tw
permalink: /zh-tw/contact/
title: "聯繫與詢盤"
description: "聯繫長沙市薩普新材料有限公司，獲取金剛石/CBN砂輪、粉末冶金高速鋼、TiNiCo均熱板報價。支持AI在線客服與WhatsApp實時詢盤。"
---

<div class="rfq">
  <div>
    <h2>提交詢盤</h2>
    <p>請告知材料、規格、數量與應用場景，我們將在 1 個工作日內回覆。</p>
    <form id="rfqForm" data-ok="已收到您的詢盤，我們會盡快回復！" data-err="提交失敗，請直接郵件或 WhatsApp 聯繫我們。">
      <input type="hidden" name="access_key" value="{{ site.web3formsKey }}" />
      <label>姓名 *<input type="text" name="name" required /></label>
      <label>公司<input type="text" name="company" /></label>
      <label>郵箱 *<input type="email" name="email" required /></label>
      <label>國家 / 地區<input type="text" name="country" /></label>
      <label>意向產品
        <select name="product">
          <option>金剛石砂輪</option>
          <option>立方氮化硼砂輪</option>
          <option>粉末冶金高速鋼</option>
          <option>TiNiCo 超合金均熱板</option>
          <option>鋼結硬質合金</option>
          <option>其他 / 不確定</option>
        </select>
      </label>
      <label>留言 *<textarea name="message" required placeholder="材料、尺寸、數量、應用場景……"></textarea></label>
            <div class="hp-field" aria-hidden="true"><label>Please leave this field empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
      <label class="consent"><input type="checkbox" name="consent" required /> 我同意就本次詢盤與我聯繫。</label>
<button class="btn btn-primary" type="submit">提交詢盤</button>
      <div id="rfqMsg" class="form-msg" role="status"></div>
    </form>
  </div>
  <div class="contact-info">
    <h2>直接聯繫</h2>
    <p><strong>WhatsApp：</strong> <a href="https://wa.me/{{ site.whatsapp }}" target="_blank" rel="noopener">wa.me/{{ site.whatsapp }}</a></p>
    <p><strong>郵箱：</strong> <a href="mailto:{{ site.email }}">{{ site.email }}</a></p>
    <p><strong>電話：</strong> {{ site.phone }}</p>
    <p><strong>微信：</strong> {{ site.wechat }}</p>
    <p><strong>地址：</strong> {{ site.addressZhTw }}</p>
    <p style="margin-top:18px"><a class="btn btn-chat" href="#" onclick="document.getElementById('chat-toggle').click();return false;">💬 AI 在線客服（即時）</a></p>
  </div>
</div>

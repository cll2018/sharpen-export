---
layout: page.njk
lang: zh
permalink: /zh/contact/
title: "联系与询盘"
description: "联系长沙市萨普新材料有限公司，获取金刚石/CBN砂轮、粉末冶金高速钢、TiNiCo均热板报价。支持AI在线客服与WhatsApp实时询盘。"
---

<div class="rfq">
  <div>
    <h2>提交询盘</h2>
    <p>请告知材料、规格、数量与应用场景，我们将在 1 个工作日内回复。</p>
    <form id="rfqForm" data-ok="已收到您的询盘，我们会尽快回复！" data-err="提交失败，请直接邮件或 WhatsApp 联系我们。">
      <input type="hidden" name="access_key" value="{{ site.web3formsKey }}" />
      <label>姓名 *<input type="text" name="name" required /></label>
      <label>公司<input type="text" name="company" /></label>
      <label>邮箱 *<input type="email" name="email" required /></label>
      <label>国家 / 地区<input type="text" name="country" /></label>
      <label>意向产品
        <select name="product">
          <option>金刚石砂轮</option>
          <option>立方氮化硼砂轮</option>
          <option>粉末冶金高速钢</option>
          <option>TiNiCo 超合金均热板</option>
          <option>钢结硬质合金</option>
          <option>其他 / 不确定</option>
        </select>
      </label>
      <label>留言 *<textarea name="message" required placeholder="材料、尺寸、数量、应用场景……"></textarea></label>
            <div class="hp-field" aria-hidden="true"><label>Please leave this field empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
      <label class="consent"><input type="checkbox" name="consent" required /> 我同意就本次询盘与我联系。</label>
<button class="btn btn-primary" type="submit">提交询盘</button>
      <div id="rfqMsg" class="form-msg" role="status"></div>
    </form>
  </div>
  <div class="contact-info">
    <h2>直接联系</h2>
    <p><strong>WhatsApp：</strong> <a href="https://wa.me/{{ site.whatsapp }}" target="_blank" rel="noopener">wa.me/{{ site.whatsapp }}</a></p>
    <p><strong>邮箱：</strong> <a href="mailto:{{ site.email }}">{{ site.email }}</a></p>
    <p><strong>电话：</strong> {{ site.phone }}</p>
    <p><strong>微信：</strong> {{ site.wechat }}</p>
    <p><strong>地址：</strong> {{ site.addressZh }}</p>
    <p style="margin-top:18px"><a class="btn btn-chat" href="#" onclick="document.getElementById('chat-toggle').click();return false;">💬 AI 在线客服（即时）</a></p>
  </div>
</div>

---
layout: page.njk
lang: ja
permalink: /ja/contact/
title: "お問い合わせ & 見積依頼（RFQ）"
description: "長沙シャープ・ニュー・マテリアルへのダイヤモンド/CBN砥輪、粉末冶金高速鋼、TiNiCo放熱板のお見積り相談。AIチャットまたはWhatsAppでリアルタイムにお問い合わせいただけます。"
---

<div class="rfq">
  <div>
    <h2>見積依頼（RFQ）を送る</h2>
    <p>素材、寸法、数量、用途をご記入ください。営業日1日以内にご回答いたします。</p>
    <form id="rfqForm" data-ok="ありがとうございます！お問い合わせが送信されました。ほどなくしてご連絡いたします。" data-err="問題が発生しました。直接メールするか、WhatsAppをご利用ください。">
      <input type="hidden" name="access_key" value="{{ site.web3formsKey }}" />
      <label>氏名 *<input type="text" name="name" required /></label>
      <label>会社名<input type="text" name="company" /></label>
      <label>メールアドレス *<input type="email" name="email" required /></label>
      <label>国 / 地域<input type="text" name="country" /></label>
      <label>ご関心のある製品
        <select name="product">
          <option>ダイヤモンド砥輪</option>
          <option>CBN（超硬）砥輪</option>
          <option>粉末冶金高速鋼</option>
          <option>TiNiCo 高耐熱合金放熱板</option>
          <option>鋼結硬質合金</option>
          <option>その他 / 不明</option>
        </select>
      </label>
      <label>メッセージ *<textarea name="message" required placeholder="素材、寸法、数量、用途など..."></textarea></label>
      <button class="btn btn-primary" type="submit">お問い合わせを送信</button>
      <div id="rfqMsg" class="form-msg" role="status"></div>
    </form>
  </div>
  <div class="contact-info">
    <h2>直接連絡先</h2>
    <p><strong>WhatsApp:</strong> <a href="https://wa.me/{{ site.whatsapp }}" target="_blank" rel="noopener">wa.me/{{ site.whatsapp }}</a></p>
    <p><strong>メール:</strong> <a href="mailto:{{ site.email }}">{{ site.email }}</a></p>
    <p><strong>電話:</strong> {{ site.phone }}</p>
    <p><strong>WeChat:</strong> {{ site.wechat }}</p>
    <p><strong>住所:</strong> {{ site.address }}</p>
    <p style="margin-top:18px"><a class="btn btn-chat" href="#" onclick="document.getElementById('chat-toggle').click();return false;">💬 AIチャット（即時対応）</a></p>
  </div>
</div>
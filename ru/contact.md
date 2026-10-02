---
layout: page.njk
lang: ru
permalink: /ru/contact/
title: "Контакты и запрос котировки"
description: "Свяжитесь с Changsha Sharpen New Materials для получения котировок по алмазным/СВС кругам, быстрорежущей стали порошковой металлургии и теплоотводам из сплава TiNiCo. Мгновенный запрос через ИИ-чат или WhatsApp."
---

<div class="rfq">
  <div>
    <h2>Отправить запрос котировки</h2>
    <p>Укажите материал, размер, количество и область применения. Мы ответим в течение 1 рабочего дня.</p>
    <form id="rfqForm" data-ok="Спасибо! Ваш запрос отправлен. Мы скоро ответим." data-err="Что-то пошло не так. Пожалуйста, напишите нам по электронной почте или используйте WhatsApp.">
      <input type="hidden" name="access_key" value="{{ site.web3formsKey }}" />
      <label>Имя *<input type="text" name="name" required /></label>
      <label>Компания<input type="text" name="company" /></label>
      <label>Email *<input type="email" name="email" required /></label>
      <label>Страна / Регион<input type="text" name="country" /></label>
      <label>Интересующий продукт
        <select name="product">
          <option>Сталепромежиточный твердосплав</option>
          <option>Алмазные шлифовальные круги</option>
          <option>СВС шлифовальные круги</option>
          <option>Быстрорежущая сталь порошковой металлургии</option>
          <option>Теплоотвод из жаропрочного сплава TiNiCo</option>
          <option>Другое / Не уверен</option>
        </select>
      </label>
      <label>Сообщение *<textarea name="message" required placeholder="Материал, размеры, количество, область применения..."></textarea></label>
            <div class="hp-field" aria-hidden="true"><label>Please leave this field empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
      <label class="consent"><input type="checkbox" name="consent" required /> Я согласен на контакт по моему запросу.</label>
<button class="btn btn-primary" type="submit">Отправить запрос</button>
      <div id="rfqMsg" class="form-msg" role="status"></div>
    </form>
  </div>
  <div class="contact-info">
    <h2>Прямой контакт</h2>
    <p><strong>WhatsApp:</strong> <a href="https://wa.me/{{ site.whatsapp }}" target="_blank" rel="noopener">wa.me/{{ site.whatsapp }}</a></p>
    <p><strong>Email:</strong> <a href="mailto:{{ site.email }}">{{ site.email }}</a></p>
    <p><strong>Тел:</strong> {{ site.phone }}</p>
    <p><strong>WeChat:</strong> {{ site.wechat }}</p>
    <p><strong>Адрес:</strong> {{ site.address }}</p>
    <p style="margin-top:18px"><a class="btn btn-chat" href="#" onclick="document.getElementById('chat-toggle').click();return false;">💬 ИИ-чат (мгновенно)</a></p>
  </div>
</div>
---
layout: page.njk
lang: pt
permalink: /pt/contact/
title: "Contato & Orçamento"
description: "Entre em contato com a Changsha Sharpen New Materials para obter orçamentos de discos de diamante/CBN, aços-rapidos de alta velocidade por metalurgia do pó e dissipadores de calor de superliga TiNiCo. Consulta em tempo real via chat IA ou WhatsApp."
---

<div class="rfq">
  <div>
    <h2>Enviar um RFQ</h2>
    <p>Informe-nos o material, tamanho, quantidade e aplicação. Responderemos em 1 dia útil.</p>
    <form id="rfqForm" data-ok="Obrigado! Sua consulta foi enviada. Responderemos em breve." data-err="Ocorreu um erro. Por favor, envie-nos um e-mail diretamente ou use o WhatsApp.">
      <input type="hidden" name="access_key" value="{{ site.web3formsKey }}" />
      <label>Nome *<input type="text" name="name" required /></label>
      <label>Empresa<input type="text" name="company" /></label>
      <label>E-mail *<input type="email" name="email" required /></label>
      <label>País / Região<input type="text" name="country" /></label>
      <label>Produto de interesse
        <select name="product">
          <option>Carbeto com ligação de aço</option>
          <option>Discos de Retificação de Diamante</option>
          <option>Discos de Retificação de CBN</option>
          <option>Aço-Rapido de Metalurgia do Pó</option>
          <option>Dissipador de Calor de Superliga TiNiCo</option>
          <option>Outros / Não sei</option>
        </select>
      </label>
      <label>Mensagem *<textarea name="message" required placeholder="Material, dimensões, quantidade, aplicação..."></textarea></label>
            <div class="hp-field" aria-hidden="true"><label>Please leave this field empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
      <label class="consent"><input type="checkbox" name="consent" required /> Concordo em ser contatado sobre meu pedido.</label>
<button class="btn btn-primary" type="submit">Enviar Consulta</button>
      <div id="rfqMsg" class="form-msg" role="status"></div>
    </form>
  </div>
  <div class="contact-info">
    <h2>Direto</h2>
    <p><strong>WhatsApp:</strong> <a href="https://wa.me/{{ site.whatsapp }}" target="_blank" rel="noopener">wa.me/{{ site.whatsapp }}</a></p>
    <p><strong>E-mail:</strong> <a href="mailto:{{ site.email }}">{{ site.email }}</a></p>
    <p><strong>Telefone:</strong> {{ site.phone }}</p>
    <p><strong>WeChat:</strong> {{ site.wechat }}</p>
    <p><strong>Endereço:</strong> {{ site.address }}</p>
    <p style="margin-top:18px"><a class="btn btn-chat" href="#" onclick="document.getElementById('chat-toggle').click();return false;">💬 Chat IA (instantâneo)</a></p>
  </div>
</div>
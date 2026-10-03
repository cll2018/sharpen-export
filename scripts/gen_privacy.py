# -*- coding: utf-8 -*-
"""Generate the privacy-policy page for all 14 languages.

Each page reuses the site's page.njk layout and pulls {{ site.email }} /
{{ site.phone }} from _data/site.js so the contact details stay in sync.
The body is a concise, GDPR/CCPA/PIPL-aware policy translated into every
language. Idempotent: rewrites the 14 <lang>/privacy.md files.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

P = {
"en": {
 "title": "Privacy Policy",
 "desc": "How Changsha Sharpen New Materials collects, uses and protects your personal data \u2014 inquiries, analytics, cookies, your GDPR/CCPA/PIPL rights and contact.",
 "body": """# Privacy Policy

_Last updated: 3 October 2026_

Changsha Sharpen New Materials Co., Ltd. ("Sharpen", "we") is committed to protecting your privacy. This policy explains what personal data we collect through www.sapu-cn.online, why, and the choices you have.

## 1. Information We Collect
- **Inquiry data** \u2014 When you send an RFQ, message or chat via our contact form, AI assistant or WhatsApp, we collect your name, email, company, country and the content you provide.
- **Usage data** \u2014 We use privacy-friendly analytics to understand site usage (pages viewed, approximate region, device type). We do **not** use advertising trackers.
- **Cookies** \u2014 Essential cookies keep the site working; optional analytics cookies can be disabled in your browser.

## 2. How We Use Your Data
To answer inquiries, prepare quotes, improve our products and website, and meet legal obligations.

## 3. Data Sharing
We never sell your personal data. We share it only with processors that operate the site (email delivery, Cloudflare hosting) or when the law requires it.

## 4. Retention
Inquiry records are kept only as long as needed to serve you and for our business records (generally up to 3 years), then deleted or anonymized.

## 5. Your Rights
Under the GDPR, CCPA and PIPL you may request access, correction, export or deletion of your data, and object to its processing. Email {{ site.email }} to exercise these rights.

## 6. Contact
Questions? Email {{ site.email }} or call {{ site.phone }}."""
},
"zh": {
 "title": "隐私政策",
 "desc": "长沙市萨普新材料有限公司如何收集、使用和保护您的个人信息\u2014\u2014询盘、分析、Cookie、您的 GDPR/CCPA/PIPL 权利与联系方式。",
 "body": """# 隐私政策

_最后更新：2026年10月3日_

长沙市萨普新材料有限公司（简称\u201c萨普\u201d、\u201c我们\u201d）致力于保护您的隐私。本政策说明我们通过 www.sapu-cn.online 收集的个人信息、收集原因以及您拥有的选择。

## 1. 我们收集的信息
- **询盘信息** \u2014\u2014 当您通过联系表单、AI 助手或 WhatsApp 提交询盘、留言或对话时，我们收集您的姓名、邮箱、公司、国家/地区以及您提供的内容。
- **使用数据** \u2014\u2014 我们使用注重隐私的分析工具了解网站使用情况（浏览页面、大致地区、设备类型）。我们**不**使用广告追踪器。
- **Cookie** \u2014\u2014 必要 Cookie 保障网站运行；可选的分析 Cookie 可在浏览器中关闭。

## 2. 我们如何使用数据
用于回复询盘、准备报价、改进产品与网站，以及履行法律义务。

## 3. 数据共享
我们绝不出售您的个人信息。仅在运营网站所需的处理方（邮件发送、Cloudflare 托管）之间共享，或法律要求时共享。

## 4. 数据保留
询盘记录仅在为您提供服务及业务存档所需期限内保留（通常不超过 3 年），随后删除或匿名化。

## 5. 您的权利
根据 GDPR、CCPA 与 PIPL，您可要求访问、更正、导出或删除您的个人数据，并反对对其进行处理。请发送邮件至 {{ site.email }} 行使上述权利。

## 6. 联系方式
如有疑问？请发送邮件至 {{ site.email }} 或致电 {{ site.phone }}。"""
},
"zh-tw": {
 "title": "隱私權政策",
 "desc": "長沙市薩普新材料有限公司如何收集、使用與保護您的個人資料\u2014\u2014詢問、分析、Cookie、您的 GDPR/CCPA/PIPL 權利與聯絡方式。",
 "body": """# 隱私權政策

_最後更新：2026年10月3日_

長沙市薩普新材料有限公司（簡稱\u201c薩普\u201d、\u201c我們\u201d）致力於保護您的隱私。本政策說明我們透過 www.sapu-cn.online 收集的個人資料、收集原因以及您擁有的選擇。

## 1. 我們收集的資料
- **詢問資料** \u2014\u2014 當您透過聯絡表單、AI 助手或 WhatsApp 提交詢問、留言或對話時，我們收集您的姓名、電子郵件、公司、國家/地區以及您提供的內容。
- **使用資料** \u2014\u2014 我們使用注重隱私的分析工具了解網站使用情況（瀏覽頁面、大致地區、裝置類型）。我們**不**使用廣告追蹤器。
- **Cookie** \u2014\u2014 必要 Cookie 保障網站運作；可選的分析 Cookie 可在瀏覽器中關閉。

## 2. 我們如何使用資料
用於回覆詢問、準備報價、改進產品與網站，以及履行法律義務。

## 3. 資料共用
我們絕不出售您的個人資料。僅在營運網站所需的處理方（郵件發送、Cloudflare 託管）之間共用，或法律要求時共用。

## 4. 資料保留
詢問記錄僅在為您提供服務及業務存檔所需期限內保留（通常不超過 3 年），隨後刪除或匿名化。

## 5. 您的權利
根據 GDPR、CCPA 與 PIPL，您可要求存取、更正、匯出或刪除您的個人資料，並反對對其進行處理。請傳送電子郵件至 {{ site.email }} 行使上述權利。

## 6. 聯絡方式
如有疑問？請傳送電子郵件至 {{ site.email }} 或致電 {{ site.phone }}。"""
},
"de": {
 "title": "Datenschutz",
 "desc": "Wie Changsha Sharpen New Materials Ihre personenbezogenen Daten erhebt, nutzt und sch\u00fctzt \u2014 Anfragen, Analytik, Cookies, Ihre Rechte nach DSGVO/CCPA/PIPL, Kontakt.",
 "body": """# Datenschutz

_Zuletzt aktualisiert: 3. Oktober 2026_

Die Changsha Sharpen New Materials Co., Ltd. ("Sharpen", "wir") verpflichtet sich, Ihre Privatsph\u00e4re zu sch\u00fctzen. Diese Richtlinie erkl\u00e4rt, welche personenbezogenen Daten wir \u00fcber www.sapu-cn.online erheben, warum wir dies tun und welche Wahlm\u00f6glichkeiten Sie haben.

## 1. Daten, die wir erheben
- **Anfragedaten** \u2014 Wenn Sie ein Angebot, eine Nachricht oder einen Chat \u00fcber unser Kontaktformular, den KI-Assistenten oder WhatsApp senden, erheben wir Ihren Namen, Ihre E-Mail, Ihr Unternehmen, Ihr Land und den \u00fcbermittelten Inhalt.
- **Nutzungsdaten** \u2014 Wir verwenden datenschutzfreundliche Analysen, um die Nutzung der Website zu verstehen (aufgerufene Seiten, ungef\u00e4hres Region, Ger\u00e4tetyp). Wir verwenden **keine** Werbe-Tracker.
- **Cookies** \u2014 Notwendige Cookies halten die Website funktionsf\u00e4hig; optionale Analyse-Cookies k\u00f6nnen im Browser deaktiviert werden.

## 2. Wie wir Ihre Daten nutzen
Um Anfragen zu beantworten, Angebote vorzubereiten, unsere Produkte und Website zu verbessern und gesetzliche Pflichten zu erf\u00fcllen.

## 3. Weitergabe von Daten
Wir verkaufen Ihre personenbezogenen Daten niemals. Wir geben sie nur an Auftragsverarbeiter weiter, die die Website betreiben (E-Mail-Versand, Cloudflare-Hosting), oder wenn es gesetzlich vorgeschrieben ist.

## 4. Aufbewahrung
Anfrageunterlagen werden nur so lange aufbewahrt, wie es f\u00fcr die Bearbeitung und unsere Gesch\u00e4ftsunterlagen n\u00f6tig ist (in der Regel bis zu 3 Jahre), dann gel\u00f6scht oder anonymisiert.

## 5. Ihre Rechte
Nach DSGVO, CCPA und PIPL k\u00f6nnen Sie Auskunft, Berichtigung, Daten\u00fcbertragung oder L\u00f6schung Ihrer Daten verlangen und der Verarbeitung widersprechen. Schreiben Sie an {{ site.email }}, um diese Rechte auszu\u00fcben.

## 6. Kontakt
Fragen? E-Mail an {{ site.email }} oder Anruf unter {{ site.phone }}."""
},
"ja": {
 "title": "プライバシーポリシー",
 "desc": "Changsha Sharpen New Materials がどのように個人データを収集・利用・保護するか\u2014\u2014お問い合わせ、分析、Cookie、GDPR/CCPA/PIPL 上の権利、連絡先。",
 "body": """# プライバシーポリシー

_最終更新：2026年10月3日_

Changsha Sharpen New Materials Co., Ltd.（「Sharpen」、「当社」）はお客様のプライバシー保護に努めます。本ポリシーは、www.sapu-cn.online を通じて収集する個人データ、その理由、およびお客様の選択肢を説明します。

## 1. 収集する情報
- **お問い合わせデータ** \u2014 お見積り、メッセージ、チャットを当社のお問い合わせフォーム、AI アシスタント、または WhatsApp から送信する際、氏名、メール、会社、国、および提供いただいた内容を収集します。
- **利用データ** \u2014 プライバシーに配慮した分析でサイトの利用状況（閲覧ページ、おおよその地域、デバイス種別）を把握します。広告トラッカーは**使用していません**。
- **Cookie** \u2014 必須 Cookie はサイトの動作に必要です。任意の分析 Cookie はブラウザで無効にできます。

## 2. データの利用目的
お問い合わせへの回答、見積りの作成、製品とサイトの改善、および法的義務の履行のため。

## 3. データの共有
個人データを販売することは一切ありません。サイト運営に必要な処理者（メール配信、Cloudflare ホスティング）とのみ共有、または法令に基づき共有します。

## 4. 保存期間
お問い合わせ記録は、対応および当社の業務記録に必要な期間のみ（原則3年以内）保存し、その後削除または匿名化します。

## 5. お客様の権利
GDPR、CCPA、PIPL に基づき、データの開示・訂正・移植・削除を要求し、処理に異議を申し立てることができます。行使には {{ site.email }} までご連絡ください。

## 6. お問い合わせ
ご質問は {{ site.email }} までメール、または {{ site.phone }} までお電話ください。"""
},
"ko": {
 "title": "개인정보 처리방침",
 "desc": "Changsha Sharpen New Materials가 개인정보를 수집\u00b7이용\u00b7보호하는 방법 \u2014 문의, 분석, 쿠키, GDPR/CCPA/PIPL 상의 권리 및 연락처.",
 "body": """# 개인정보 처리방침

_최종 업데이트: 2026년 10월 3일_

Changsha Sharpen New Materials Co., Ltd.("Sharpen", "당사")는 귀하의 개인정보 보호에 최선을 다합니다. 본 방침은 www.sapu-cn.online을 통해 수집하는 개인정보, 수집 이유 및 귀하의 선택권을 설명합니다.

## 1. 수집하는 정보
- **문의 데이터** \u2014 견적, 메시지, 채팅을 당사의 문의 양식, AI 어시스턴트 또는 WhatsApp으로 보낼 때 이름, 이메일, 회사, 국가 및 제공 내용을 수집합니다.
- **이용 데이터** \u2014 개인정보 보호 친화적인 분석으로 사이트 이용(조회 페이지, 대략적 지역, 기기 유형)을 파악합니다. 광고 추적기는 **사용하지 않습니다**.
- **쿠키** \u2014 필수 쿠키는 사이트 작동에 필요하며, 선택적 분석 쿠키는 브라우저에서 비활성화할 수 있습니다.

## 2. 데이터 이용 목적
문의 응답, 견적 준비, 제품 및 사이트 개선, 법적 의무 이행을 위해 이용합니다.

## 3. 데이터 공유
개인정보를 절대 판매하지 않습니다. 사이트 운영에 필요한 처리자(이메일 발송, Cloudflare 호스팅)와만 공유하거나 법령에 따라 공유합니다.

## 4. 보관 기간
문의 기록은 귀하에게 서비스하고 업무 기록을 유지하는 데 필요한 기간(일반적으로 최대 3년)까지만 보관한 후 삭제 또는 익명화합니다.

## 5. 귀하의 권리
GDPR, CCPA, PIPL에 따라 데이터 접근, 정정, 이동, 삭제를 요청하고 처리에 반대할 수 있습니다. 권리 행사는 {{ site.email }}으로 문의하세요.

## 6. 연락처
문의사항은 {{ site.email }}으로 이메일 또는 {{ site.phone }}으로 전화해 주세요."""
},
"ru": {
 "title": "Политика конфиденциальности",
 "desc": "Как Changsha Sharpen New Materials собирает, использует и защищает ваши персональные данные \u2014 запросы, аналитика, файлы cookie, ваши права по GDPR/CCPA/PIPL и контакты.",
 "body": """# Политика конфиденциальности

_Обновлено: 3 октября 2026 г._

Changsha Sharpen New Materials Co., Ltd. («Sharpen», «мы») обязуется защищать вашу частную жизнь. Эта политика объясняет, какие персональные данные мы собираем через www.sapu-cn.online, зачем и какие у вас есть варианты.

## 1. Какие данные мы собираем
- **Данные запросов** \u2014 когда вы отправляете запрос, сообщение или пишете в чат через форму контакта, ИИ-помощника или WhatsApp, мы собираем ваше имя, e-mail, компанию, страну и переданное содержание.
- **Данные об использовании** \u2014 мы применяем аналитику, бережно относящуюся к приватности, чтобы понять использование сайта (просмотренные страницы, примерный регион, тип устройства). **Никаких** рекламных трекеров мы не используем.
- **Файлы cookie** \u2014 необходимые cookie обеспечивают работу сайта; необязательные аналитические cookie можно отключить в браузере.

## 2. Как мы используем данные
Чтобы отвечать на запросы, готовить предложения, улучшать продукцию и сайт и соблюдать законы.

## 3. Передача данных
Мы никогда не продаём ваши персональные данные. Делимся ими только с подрядчиками, обеспечивающими работу сайта (рассылка e-mail, хостинг Cloudflare), либо когда этого требует закон.

## 4. Срок хранения
Записи запросов хранятся только пока это нужно для обслуживания и наших деловых архивов (обычно до 3 лет), затем удаляются или обезличиваются.

## 5. Ваши права
По GDPR, CCPA и PIPL вы можете запросить доступ, исправление, экспорт или удаление данных и возразить против их обработки. Пишите на {{ site.email }}, чтобы воспользоваться этими правами.

## 6. Контакты
Вопросы? Пишите на {{ site.email }} или звоните по {{ site.phone }}."""
},
"es": {
 "title": "Pol\u00edtica de Privacidad",
 "desc": "C\u00f3mo Changsha Sharpen New Materials recopila, usa y protege sus datos personales \u2014 consultas, anal\u00edtica, cookies, sus derechos GDPR/CCPA/PIPL y contacto.",
 "body": """# Pol\u00edtica de Privacidad

_\u00daltima actualizaci\u00f3n: 3 de octubre de 2026_

Changsha Sharpen New Materials Co., Ltd. ("Sharpen", "nosotros") se compromete a proteger su privacidad. Esta pol\u00edtica explica qu\u00e9 datos personales recopilamos a trav\u00e9s de www.sapu-cn.online, por qu\u00e9 y las opciones de las que dispone.

## 1. Informaci\u00f3n que recopilamos
- **Datos de consulta** \u2014 Cuando env\u00eda una solicitud de cotizaci\u00f3n, un mensaje o un chat mediante nuestro formulario de contacto, asistente de IA o WhatsApp, recopilamos su nombre, correo, empresa, pa\u00eds y el contenido que aporta.
- **Datos de uso** \u2014 Usamos anal\u00edtica respetuosa con la privacidad para entender el uso del sitio (p\u00e1ginas vistas, regi\u00f3n aproximada, tipo de dispositivo). **No** usamos rastreadores publicitarios.
- **Cookies** \u2014 Las cookies esenciales mantienen el sitio funcional; las cookies anal\u00edticas opcionales se pueden desactivar en el navegador.

## 2. C\u00f3mo usamos sus datos
Para responder consultas, preparar cotizaciones, mejorar nuestros productos y sitio, y cumplir obligaciones legales.

## 3. Compartir datos
Nunca vendemos sus datos personales. Los compartimos solo con procesadores que operan el sitio (env\u00edo de correo, alojamiento Cloudflare) o cuando la ley lo exige.

## 4. Conservaci\u00f3n
Los registros de consulta se conservan solo el tiempo necesario para atenderle y para nuestros registros comerciales (generalmente hasta 3 a\u00f1os), luego se eliminan o anonimizan.

## 5. Sus derechos
Seg\u00fan el GDPR, CCPA y PIPL, puede solicitar acceso, rectificaci\u00f3n, exportaci\u00f3n o eliminaci\u00f3n de sus datos y oponerse a su tratamiento. Escriba a {{ site.email }} para ejercerlos.

## 6. Contacto
\u00bfPreguntas? Escr\u00edbanos a {{ site.email }} o ll\u00e1menos al {{ site.phone }}."""
},
"pt": {
 "title": "Pol\u00edtica de Privacidade",
 "desc": "Como a Changsha Sharpen New Materials coleta, usa e protege seus dados pessoais \u2014 solicita\u00e7\u00f5es, an\u00e1lises, cookies, seus direitos GDPR/CCPA/PIPL e contato.",
 "body": """# Pol\u00edtica de Privacidade

_\u00daltima atualiza\u00e7\u00e3o: 3 de outubro de 2026_

A Changsha Sharpen New Materials Co., Ltd. ("Sharpen", "n\u00f3s") est\u00e1 comprometida em proteger sua privacidade. Esta pol\u00edtica explica quais dados pessoais coletamos por meio de www.sapu-cn.online, por que motivo e as op\u00e7\u00f5es dispon\u00edveis.

## 1. Informa\u00e7\u00f5es que coletamos
- **Dados de solicita\u00e7\u00e3o** \u2014 Ao enviar uma cota\u00e7\u00e3o, mensagem ou bate-papo pelo formul\u00e1rio de contato, assistente de IA ou WhatsApp, coletamos seu nome, e-mail, empresa, pa\u00eds e o conte\u00fado fornecido.
- **Dados de uso** \u2014 Usamos an\u00e1lises que respeitam a privacidade para entender o uso do site (p\u00e1ginas vistas, regi\u00e3o aproximada, tipo de dispositivo). **N\u00e3o** usamos rastreadores publicit\u00e1rios.
- **Cookies** \u2014 Cookies essenciais mant\u00eam o site funcional; cookies anal\u00edticos opcionais podem ser desativados no navegador.

## 2. Como usamos seus dados
Para responder solicita\u00e7\u00f5es, preparar cota\u00e7\u00f5es, melhorar produtos e site, e cumprir obriga\u00e7\u00f5es legais.

## 3. Compartilhamento de dados
Nunca vendemos seus dados pessoais. Os compartilhamos apenas com processadores que operam o site (envio de e-mail, hospedagem Cloudflare) ou quando a lei exige.

## 4. Reten\u00e7\u00e3o
Os registros de solicita\u00e7\u00e3o s\u00e3o mantidos apenas pelo tempo necess\u00e1rio para atend\u00ea-lo e para nossos registros comerciais (geralmente at\u00e9 3 anos), depois exclu\u00eddos ou anonimizado.

## 5. Seus direitos
Sob o GDPR, CCPA e PIPL, voc\u00ea pode solicitar acesso, corre\u00e7\u00e3o, exporta\u00e7\u00e3o ou exclus\u00e3o de seus dados e opor-se ao tratamento. Escreva para {{ site.email }} para exercer esses direitos.

## 6. Contato
D\u00favidas? Escreva para {{ site.email }} ou ligue para {{ site.phone }}."""
},
"fr": {
 "title": "Politique de Confidentialit\u00e9",
 "desc": "Comment Changsha Sharpen New Materials collecte, utilise et prot\u00e8ge vos donn\u00e9es personnelles \u2014 demandes, analyse, cookies, vos droits RGPD/CCPA/PIPL et contact.",
 "body": """# Politique de Confidentialit\u00e9

_Derni\u00e8re mise \u00e0 jour : 3 octobre 2026_

Changsha Sharpen New Materials Co., Ltd. (\u00ab Sharpen \u00bb, \u00ab nous \u00bb) s'engage \u00e0 prot\u00e9ger votre vie priv\u00e9e. Cette politique explique quelles donn\u00e9es personnelles nous collectons via www.sapu-cn.online, pourquoi, et les choix qui s'offrent \u00e0 vous.

## 1. Donn\u00e9es collect\u00e9es
- **Donn\u00e9es de demande** \u2014 Lorsque vous envoyez un devis, un message ou un chat via notre formulaire de contact, l'assistant IA ou WhatsApp, nous collectons votre nom, e-mail, soci\u00e9t\u00e9, pays et le contenu fourni.
- **Donn\u00e9es d'usage** \u2014 Nous utilisons une analytique respectueuse de la vie priv\u00e9e pour comprendre l'usage du site (pages vues, r\u00e9gion approximative, type d'appareil). Nous n'utilisons **aucun** traceur publicitaire.
- **Cookies** \u2014 Les cookies essentiels font fonctionner le site ; les cookies analytiques optionnels peuvent \u00eatre d\u00e9sactiv\u00e9s dans le navigateur.

## 2. Comment nous utilisons vos donn\u00e9es
Pour r\u00e9pondre aux demandes, pr\u00e9parer des devis, am\u00e9liorer nos produits et le site, et respecter nos obligations l\u00e9gales.

## 3. Partage des donn\u00e9es
Nous ne vendons jamais vos donn\u00e9es personnelles. Nous les partageons uniquement avec les sous-traitants qui font fonctionner le site (envoi d'e-mails, h\u00e9bergement Cloudflare) ou lorsque la loi l'exige.

## 4. Conservation
Les demandes sont conserv\u00e9es uniquement le temps n\u00e9cessaire au service et \u00e0 nos registres (g\u00e9n\u00e9ralement jusqu'\u00e0 3 ans), puis supprim\u00e9es ou anonymis\u00e9es.

## 5. Vos droits
Conform\u00e9ment au RGPD, CCPA et PIPL, vous pouvez demander l'acc\u00e8s, la rectification, l'export ou la suppression de vos donn\u00e9es et vous opposer \u00e0 leur traitement. \u00c9crivez \u00e0 {{ site.email }} pour exercer ces droits.

## 6. Contact
Des questions ? \u00c9crivez \u00e0 {{ site.email }} ou appelez au {{ site.phone }}."""
},
"it": {
 "title": "Informativa sulla Privacy",
 "desc": "Come Changsha Sharpen New Materials raccoglie, usa e protegge i tuoi dati personali \u2014 richieste, analisi, cookie, i tuoi diritti GDPR/CCPA/PIPL e contatti.",
 "body": """# Informativa sulla Privacy

_Ultimo aggiornamento: 3 ottobre 2026_

Changsha Sharpen New Materials Co., Ltd. ("Sharpen", "noi") \u00e8 impegnata a proteggere la tua privacy. Questa informativa spiega quali dati personali raccogliamo tramite www.sapu-cn.online, perch\u00e9 e quali scelte hai.

## 1. Dati che raccogliamo
- **Dati di richiesta** \u2014 Quando invii un preventivo, un messaggio o una chat tramite il modulo di contatto, l'assistente IA o WhatsApp, raccogliamo nome, e-mail, azienda, paese e il contenuto fornito.
- **Dati di utilizzo** \u2014 Usiamo analisi rispettose della privacy per capire l'uso del sito (pagine viste, regione approssimativa, tipo di dispositivo). **Non** usiamo tracker pubblicitari.
- **Cookie** \u2014 I cookie essenziali mantengono il sito funzionante; i cookie analitici opzionali possono essere disattivati nel browser.

## 2. Come usiamo i dati
Per rispondere alle richieste, preparare preventivi, migliorare prodotti e sito e adempiere agli obblighi di legge.

## 3. Condivisione dei dati
Non vendiamo mai i tuoi dati personali. Li condividiamo solo con responsabili che gestiscono il sito (invio e-mail, hosting Cloudflare) o quando richiesto dalla legge.

## 4. Conservazione
I registri delle richieste sono conservati solo per il tempo necessario a servirti e ai nostri archivi (generalmente fino a 3 anni), poi eliminati o anonimizzati.

## 5. I tuoi diritti
Ai sensi di GDPR, CCPA e PIPL puoi richiedere accesso, rettifica, esportazione o cancellazione dei dati e opporti al trattamento. Scrivi a {{ site.email }} per esercitare questi diritti.

## 6. Contatti
Domande? Scrivi a {{ site.email }} o chiama il {{ site.phone }}."""
},
"tr": {
 "title": "Gizlilik Politikas\u0131",
 "desc": "Changsha Sharpen New Materials ki\u015fisel verilerinizi nas\u0131l toplar, kullan\u0131r ve korur \u2014 talepler, analiz, \u00e7erezler, GDPR/CCPA/PIPL kapsam\u0131ndaki haklar\u0131n\u0131z ve ileti\u015fim.",
 "body": """# Gizlilik Politikas\u0131

_Son g\u00fcncelleme: 3 Ekim 2026_

Changsha Sharpen New Materials Co., Ltd. ("Sharpen", "biz"), gizlili\u011finizi korumaya kararl\u0131d\u0131r. Bu politika, www.sapu-cn.online \u00fczerinden hangi ki\u015fisel verileri toplad\u0131\u011f\u0131m\u0131z\u0131, nedenini ve se\u00e7eneklerinizi a\u00e7\u0131klar.

## 1. Toplad\u0131\u011f\u0131m\u0131z bilgiler
- **Talep verileri** \u2014 \u0130leti\u015fim formumuz, AI asistan\u0131m\u0131z veya WhatsApp \u00fczerinden bir teklif, mesaj veya sohbet g\u00f6nderdi\u011finizde ad\u0131n\u0131z\u0131, e-postan\u0131z\u0131, \u015firketinizi, \u00fclkenizi ve sa\u011flad\u0131\u011f\u0131n\u0131z i\u00e7eri\u011fi toplar\u0131z.
- **Kullan\u0131m verileri** \u2014 Site kullan\u0131m\u0131n\u0131 (g\u00f6r\u00fcnt\u00fclenen sayfalar, yakla\u015f\u0131k b\u00f6lge, cihaz t\u00fcr\u00fc) anlamak i\u00e7in gizlilik dostu analiz kullan\u0131r\u0131z. Reklam izleyicisi **kullanmay\u0131z**.
- **\u00c7erezler** \u2014 Temel \u00e7erezler sitenin \u00e7al\u0131\u015fmas\u0131n\u0131 sa\u011flar; iste\u011fe ba\u011fl\u0131 analiz \u00e7erezleri taray\u0131c\u0131da devre d\u0131\u015f\u0131 b\u0131rak\u0131labilir.

## 2. Verilerinizi nas\u0131l kullan\u0131yoruz
Talepleri yan\u0131tlamak, teklif haz\u0131rlamak, \u00fcr\u00fcnleri ve sitemizi iyile\u015ftirmek ve yasal y\u00fck\u00fcml\u00fcl\u00fckleri yerine getirmek i\u00e7in.

## 3. Veri payla\u015f\u0131m\u0131
Kis\u0131sel verilerinizi asla satmay\u0131z. Yaln\u0131zca siteyi i\u015fleten i\u015flemcilerle (e-posta g\u00f6nderimi, Cloudflare bar\u0131nd\u0131rma) veya yasa zorunlu k\u0131ld\u0131\u011f\u0131nda payla\u015f\u0131r\u0131z.

## 4. Saklama
Talep kay\u0131tlar\u0131, size hizmet ve i\u015f kay\u0131tlar\u0131m\u0131z i\u00e7in gerekli s\u00fcre boyunca (genellikle en fazla 3 y\u0131l) tutulur, ard\u0131ndan silinir veya anonimle\u015ftirilir.

## 5. Haklar\u0131n\u0131z
GDPR, CCPA ve PIPL kapsam\u0131nda verilerinize eri\u015fim, d\u00fczeltme, d\u0131\u015fa aktarma veya silme talep edebilir ve i\u015flenmesine itiraz edebilirsiniz. Bu haklar\u0131 kullanmak i\u00e7in {{ site.email }} adresine yaz\u0131n.

## 6. \u0130leti\u015fim
Sorular\u0131n\u0131z m\u0131 var? {{ site.email }} adresine e-posta g\u00f6nderin veya {{ site.phone }} numaras\u0131n\u0131 aray\u0131n."""
},
"ar": {
 "title": "\u0633\u064a\u0627\u0633\u0629 \u0627\u0644\u062e\u0635\u0648\u0635\u064a\u0629",
 "desc": "كيف تجمع Changsha Sharpen New Materials وتستخدم وتحمي بياناتك الشخصية \u2014 الطلبات والتحليلات وملفات تعريف الارتباط وحقوقك بموجب GDPR/CCPA/PIPL ووسائل الاتصال.",
 "body": """# \u0633\u064a\u0627\u0633\u0629 \u0627\u0644\u062e\u0635\u0648\u0635\u064a\u0629

_\u0622\u062e\u0631 \u062a\u062d\u062f\u064a\u062b: 3 \u0623\u0643\u062a\u0648\u0628\u0631 2026_

\u062a\u0644\u062a\u0632\u0645 Changsha Sharpen New Materials Co., Ltd. ("Sharpen"\u060c "\u0646\u062d\u0646") \u0628\u062d\u0645\u0627\u064a\u0629 \u062e\u0635\u0648\u0635\u064a\u062a\u0643. \u062a\u0648\u0636\u062d \u0647\u0630\u0647 \u0627\u0644\u0633\u064a\u0627\u0633\u0629 \u0645\u0627 \u0646\u062c\u0645\u0639\u0647 \u0645\u0646 \u0628\u064a\u0627\u0646\u0627\u062a \u0634\u062e\u0635\u064a\u0629 \u0639\u0628\u0631 www.sapu-cn.online \u0648\u0644\u0645\u0627\u0630\u0627 \u0648\u0627\u0644\u062e\u064a\u0627\u0631\u0627\u062a \u0627\u0644\u0645\u062a\u0627\u062d\u0629 \u0644\u0643.

## 1. \u0627\u0644\u0645\u0639\u0644\u0648\u0645\u0627\u062a \u0627\u0644\u062a\u064a \u0646\u062c\u0645\u0639\u0647\u0627
- **\u0628\u064a\u0627\u0646\u0627\u062a \u0627\u0644\u0637\u0644\u0628\u0627\u062a** \u2014 \u0639\u0646\u062f \u0625\u0631\u0633\u0627\u0644 \u0639\u0631\u0636 \u0633\u0639\u0631 \u0623\u0648 \u0631\u0633\u0627\u0644\u0629 \u0623\u0648 \u0645\u062d\u0627\u062f\u062b\u0629 \u0639\u0628\u0631 \u0646\u0645\u0648\u0630\u062c \u0627\u0644\u062a\u0648\u0627\u0635\u0644 \u0623\u0648 \u0645\u0633\u0627\u0639\u062f \u0627\u0644\u0630\u0643\u0627\u0621 \u0627\u0644\u0627\u0635\u0637\u0646\u0627\u0639\u064a \u0623\u0648 \u0648\u0627\u062a\u0633\u0627\u0628\u060c \u0646\u062c\u0645\u0639 \u0627\u0633\u0645\u0643 \u0648\u0628\u0631\u064a\u062f\u0643 \u0627\u0644\u0625\u0644\u0643\u062a\u0631\u0648\u0646\u064a \u0648\u0634\u0631\u0643\u062a\u0643 \u0648\u0628\u0644\u062f\u0643 \u0648\u0627\u0644\u0645\u062d\u062a\u0648\u0649 \u0627\u0644\u0630\u064a \u062a\u0642\u062f\u0645\u0647.
- **\u0628\u064a\u0627\u0646\u0627\u062a \u0627\u0644\u0627\u0633\u062a\u062e\u062f\u0627\u0645** \u2014 \u0646\u0633\u062a\u062e\u062f\u0645 \u062a\u062d\u0644\u064a\u0644\u0627\u062a \u062a\u062d\u062a\u0631\u0645 \u0627\u0644\u062e\u0635\u0648\u0635\u064a\u0629 \u0644\u0641\u0647\u0645 \u0627\u0633\u062a\u062e\u062f\u0627\u0645 \u0627\u0644\u0645\u0648\u0642\u0639 (\u0627\u0644\u0635\u0641\u062d\u0627\u062a \u0627\u0644\u062a\u064a \u062a\u0645\u062a \u0645\u0634\u0627\u0647\u062f\u062a\u0647\u0627 \u0648\u0627\u0644\u0645\u0646\u0637\u0642\u0629 \u0627\u0644\u062a\u0642\u0631\u064a\u0628\u064a\u0629 \u0648\u0646\u0648\u0639 \u0627\u0644\u062c\u0647\u0627\u0632). \u0644\u0627 \u0646\u0633\u062a\u062e\u062f\u0645 **\u0623\u064a** \u0645\u062a\u062a\u0628\u0639\u0627\u062a \u0625\u0639\u0644\u0627\u0646\u064a\u0629.
- **\u0645\u0644\u0641\u0627\u062a \u062a\u0639\u0631\u064a\u0641 \u0627\u0644\u0627\u0631\u062a\u0628\u0627\u0637** \u2014 \u062a\u0628\u0642\u064a \u0645\u0644\u0641\u0627\u062a \u062a\u0639\u0631\u064a\u0641 \u0627\u0644\u0627\u0631\u062a\u0628\u0627\u0637 \u0627\u0644\u0636\u0631\u0648\u0631\u064a\u0629 \u0627\u0644\u0645\u0648\u0642\u0639 \u064a\u0639\u0645\u0644\u061b \u0648\u064a\u0645\u0643\u0646 \u062a\u0639\u0637\u064a\u0644 \u0645\u0644\u0641\u0627\u062a \u0627\u0644\u062a\u062d\u0644\u064a\u0644 \u0627\u0644\u0627\u062e\u062a\u064a\u0627\u0631\u064a\u0629 \u0641\u064a \u0627\u0644\u0645\u062a\u0635\u0641\u062d.

## 2. \u0643\u064a\u0641 \u0646\u0633\u062a\u062e\u062f\u0645 \u0628\u064a\u0627\u0646\u0627\u062a\u0643
\u0644\u0644\u0631\u062f \u0639\u0644\u0649 \u0627\u0644\u0637\u0644\u0628\u0627\u062a \u0648\u0625\u0639\u062f\u0627\u062f \u0639\u0631\u0648\u0636 \u0627\u0644\u0623\u0633\u0639\u0627\u0631 \u0648\u062a\u062d\u0633\u064a\u0646 \u0645\u0646\u062a\u062c\u0627\u062a\u0646\u0627 \u0648\u0645\u0648\u0642\u0639\u0646\u0627 \u0648\u0627\u0644\u0648\u0641\u0627\u0621 \u0628\u0627\u0644\u0627\u0644\u062a\u0632\u0627\u0645\u0627\u062a \u0627\u0644\u0642\u0627\u0646\u0648\u0646\u064a\u0629.

## 3. \u0645\u0634\u0627\u0631\u0643\u0629 \u0627\u0644\u0628\u064a\u0627\u0646\u0627\u062a
\u0644\u0627 \u0646\u0628\u064a\u0639 \u0628\u064a\u0627\u0646\u0627\u062a\u0643 \u0627\u0644\u0634\u062e\u0635\u064a\u0629 \u0645\u0637\u0644\u0642\u064b\u0627. \u0646\u062a\u0634\u0627\u0631\u0643\u0647\u0627 \u0641\u0642\u0637 \u0645\u0639 \u0627\u0644\u0645\u0639\u0627\u0644\u062c\u064a\u0646 \u0627\u0644\u0630\u064a\u0646 \u064a\u0634\u063a\u0651\u0644\u0648\u0646 \u0627\u0644\u0645\u0648\u0642\u0639 (\u0625\u0631\u0633\u0627\u0644 \u0627\u0644\u0628\u0631\u064a\u062f\u060c \u0627\u0633\u062a\u0636\u0627\u0641\u0629 Cloudflare) \u0623\u0648 \u0639\u0646\u062f\u0645\u0627 \u064a\u0642\u062a\u0636\u064a \u0627\u0644\u0642\u0627\u0646\u0648\u0646 \u0630\u0644\u0643.

## 4. \u0627\u0644\u0627\u062d\u062a\u0641\u0627\u0638
\u062a\u064f\u062d\u0641\u0638 \u0633\u062c\u0644\u0627\u062a \u0627\u0644\u0637\u0644\u0628\u0627\u062a \u0641\u0642\u0637 \u0628\u0627\u0644\u0642\u062f\u0631 \u0627\u0644\u0644\u0627\u0632\u0645 \u0644\u062e\u062f\u0645\u062a\u0643 \u0648\u0633\u062c\u0644\u0627\u062a \u0623\u0639\u0645\u0627\u0644\u0646\u0627 (\u0639\u0627\u062f\u0629\u064b\u0627 \u062d\u062a\u0649 3 \u0633\u0646\u0648\u0627\u062a)\u060c \u062b\u0645 \u062a\u064f\u062d\u0630\u0641 \u0623\u0648 \u062a\u064f\u062c\u0647\u0651\u0644.

## 5. \u062d\u0642\u0648\u0642\u0643
\u0628\u0645\u0648\u062c\u0628 GDPR \u0648CCPA \u0648PIPL\u060c \u064a\u0645\u0643\u0646\u0643 \u0637\u0644\u0628 \u0627\u0644\u0648\u0635\u0648\u0644 \u0625\u0644\u0649 \u0628\u064a\u0627\u0646\u0627\u062a\u0643 \u0623\u0648 \u062a\u0635\u062d\u064a\u062d\u0647\u0627 \u0623\u0648 \u062a\u0635\u062f\u064a\u0631\u0647\u0627 \u0623\u0648 \u062d\u0630\u0641\u0647\u0627 \u0648\u0627\u0644\u0627\u0639\u062a\u0631\u0627\u0636 \u0639\u0644\u0649 \u0645\u0639\u0627\u0644\u062c\u062a\u0647\u0627. \u0631\u0627\u0633\u0644\u0646\u0627 \u0639\u0644\u0649 {{ site.email }} \u0644\u0645\u0627\u0631\u0633\u0629 \u0647\u0630\u0647 \u0627\u0644\u062d\u0642\u0648\u0642.

## 6. \u0627\u0644\u062a\u0648\u0627\u0635\u0644
\u0623\u0633\u0626\u0644\u0629\u061f \u0631\u0627\u0633\u0644\u0646\u0627 \u0639\u0644\u0649 {{ site.email }} \u0623\u0648 \u0627\u062a\u0635\u0644 \u0628\u0650 {{ site.phone }}."""
},
"vi": {
 "title": "Ch\u00ednh s\u00e1ch B\u1ea3o m\u1eadt",
 "desc": "Changsha Sharpen New Materials thu th\u1ea7p, s\u1eed d\u1ee5ng v\u00e0 b\u1ea3o v\u1ec7 d\u1eef li\u1ec7u c\u00e1 nh\u00e2n c\u1ee7a b\u1ea1n nh\u01b0 th\u1ebf n\u00e0o \u2014 y\u00eau c\u1ea7u, ph\u00e2n t\u00edch, cookie, quy\u1ec1n GDPR/CCPA/PIPL v\u00e0 li\u00ean h\u1ec7.",
 "body": """# Ch\u00ednh s\u00e1ch B\u1ea3o m\u1eadt

_C\u1eadp nh\u1eadt l\u1ea7n cu\u1ed1i: 3 th\u00e1ng 10 n\u0103m 2026_

Changsha Sharpen New Materials Co., Ltd. ("Sharpen", "ch\u00fang t\u00f4i") cam k\u1ebft b\u1ea3o v\u1ec7 quy\u1ec1n ri\u00eang t\u01b0 c\u1ee7a b\u1ea1n. Ch\u00ednh s\u00e1ch n\u00e0y gi\u1ea3i th\u00edch d\u1eef li\u1ec7u c\u00e1 nh\u00e2n n\u00e0o ch\u00fang t\u00f4i thu th\u1ea7p qua www.sapu-cn.online, v\u00ec sao v\u00e0 c\u00e1c l\u1ef1a ch\u1ecdn c\u1ee7a b\u1ea1n.

## 1. Th\u00f4ng tin ch\u00fang t\u00f4i thu th\u1ea7p
- **D\u1eef li\u1ec7u y\u00eau c\u1ea7u** \u2014 Khi b\u1ea1n g\u1eedi b\u00e1o gi\u00e1, tin nh\u1eafn ho\u1eb7c tr\u00f2 chuy\u1ec7n qua bi\u1ec3u m\u1eabu li\u00ean h\u1ec7, tr\u1ee3 l\u00fd AI ho\u1eb7c WhatsApp, ch\u00fang t\u00f4i thu th\u1ea7p t\u00ean, email, c\u00f4ng ty, qu\u1ed1c gia v\u00e0 n\u1ed9i dung b\u1ea1n cung c\u1ea5p.
- **D\u1eef li\u1ec7u s\u1eed d\u1ee5ng** \u2014 Ch\u00fang t\u00f4i d\u00f9ng ph\u00e2n t\u00edch th\u00e2n thi\u1ec7n v\u1edbi quy\u1ec1n ri\u00eang t\u01b0 \u0111\u1ec3 hi\u1ec3u c\u00e1ch site \u0111\u01b0\u1ee3c d\u00f9ng (trang xem, khu v\u1ef1c x\u1ea5p x\u1ec9, lo\u1ea1i thi\u1ebft b\u1ecb). Ch\u00fang t\u00f4i **kh\u00f4ng** d\u00f9ng tr\u00ecnh theo d\u00f5i qu\u1ea3ng c\u00e1o.
- **Cookie** \u2014 Cookie c\u1ea7n thi\u1ebft gi\u00fap site ho\u1ea1t \u0111\u1ed9ng; cookie ph\u00e2n t\u00edch t\u00f9y ch\u1ecdn c\u00f3 th\u1ec3 t\u1eaft trong tr\u00ecnh duy\u1ec7t.

## 2. C\u00e1ch ch\u00fang t\u00f4i d\u00f9ng d\u1eef li\u1ec7u
\u0110\u1ec3 tr\u1ea3 l\u1eddi y\u00eau c\u1ea7u, chu\u1ea9n b\u1ecb b\u00e1o gi\u00e1, c\u1ea3i thi\u1ec7n s\u1ea3n ph\u1ea9m v\u00e0 site, v\u00e0 tu\u00e2n th\u1ee7 ngh\u0129a v\u1ee5 ph\u00e1p l\u00fd.

## 3. Chia s\u1ebb d\u1eef li\u1ec7u
Ch\u00fang t\u00f4i kh\u00f4ng bao gi\u1edd b\u00e1n d\u1eef li\u1ec7u c\u00e1 nh\u00e2n c\u1ee7a b\u1ea1n. Ch\u1ec9 chia s\u1ebb v\u1edbi b\u00ean x\u1eed l\u00fd v\u1eadn h\u00e0nh site (g\u1eedi email, l\u01b0u tr\u1eef Cloudflare) ho\u1eb7c khi lu\u1eadt y\u00eau c\u1ea7u.

## 4. L\u01b0u gi\u1eef
H\u1ed3 s\u01a1 y\u00eau c\u1ea7u ch\u1ec9 \u0111\u01b0\u1ee3c gi\u1eef trong th\u1eddi gian c\u1ea7n \u0111\u1ec3 ph\u1ee5c v\u1ee5 b\u1ea1n v\u00e0 l\u01b0u tr\u1eef kinh doanh (th\u01b0\u1eddng t\u1ed1i \u0111a 3 n\u0103m), sau \u0111\u00f3 b\u1ecb x\u00f3a ho\u1eb7c \u1ea9n danh h\u00f3a.

## 5. Quy\u1ec1n c\u1ee7a b\u1ea1n
Theo GDPR, CCPA v\u00e0 PIPL, b\u1ea1n c\u00f3 th\u1ec3 y\u00eau c\u1ea7u truy c\u1eadp, ch\u1ec9nh s\u1eeda, xu\u1ea5t ho\u1eb7c x\u00f3a d\u1eef li\u1ec7u v\u00e0 ph\u1ea3n \u0111\u1ed1i x\u1eed l\u00fd. G\u1eedi email \u0111\u1ebfn {{ site.email }} \u0111\u1ec3 th\u1ef1c hi\u1ec7n c\u00e1c quy\u1ec1n n\u00e0y.

## 6. Li\u00ean h\u1ec7
Th\u1eafc m\u1eafc? G\u1eedi email \u0111\u1ebfn {{ site.email }} ho\u1eb7c g\u1ecdi {{ site.phone }}."""
},
}

def main():
    n = 0
    for lang, d in P.items():
        out = os.path.join(ROOT, lang, "privacy.md")
        content = (
            "---\n"
            "layout: page.njk\n"
            "lang: " + lang + "\n"
            "permalink: /" + lang + "/privacy/\n"
            'title: "' + d["title"] + '"\n'
            'description: "' + d["desc"] + '"\n'
            "---\n\n" + d["body"] + "\n"
        )
        open(out, "w", encoding="utf-8").write(content)
        n += 1
    print("privacy pages written:", n)

if __name__ == "__main__":
    main()

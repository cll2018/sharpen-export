# -*- coding: utf-8 -*-
"""Localize the 14 news titles that were left in English across the 11
non-English, non-Chinese languages (de, ja, ko, ru, es, pt, fr, it, tr, ar, vi).

The 11 languages' news.md files were already converted to the GENERATED card
grid, so the English titles now live in:
  * _data/newsSlugs.json        (title per lang per slug)
  * <lang>/news/<slug>.md        (front-matter title:)
  * <lang>/news.md               (card <a href=".../<slug>/">TITLE</a>)

This script writes the localized titles into all three places. It does NOT touch
article bodies (those are a separate, larger translation task).

Idempotent: re-running just re-applies the same translations.

Usage: python scripts/translate_news_titles.py
"""
import os, re, json, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Languages that still had English news titles.
LANGS = ["de", "ja", "ko", "ru", "es", "pt", "fr", "it", "tr", "ar", "vi"]

# Localized titles. Keyed by slug -> lang -> title.
# (Bodies of these articles remain English; only titles are localized here.)
TITLES = {
    "ceramic-phone-shell-forum-2017": {
        "de": "Sharpen auf dem 2. PM-/Keramik-Handygehäuse-Forum",
        "ja": "Sharpen、第2回 PM／セラミック携帯ケースフォーラムに出展",
        "ko": "Sharpen, 제2회 PM/세라믹 휴대폰 케이스 포럼 참가",
        "ru": "Sharpen на 2-м форуме по PM и керамическим корпусам для телефонов",
        "es": "Sharpen en el 2.º Foro de PM y Carcasas de Teléfono de Cerámica",
        "pt": "Sharpen no 2.º Fórum de PM e Carcasas de Telefone em Cerâmica",
        "fr": "Sharpen au 2e forum PM / boîtiers de téléphone en céramique",
        "it": "Sharpen al 2° forum sulla PM / involucri telefonici in ceramica",
        "tr": "Sharpen, 2. PM / Seramik Telefon Kapağı Forumu'nda",
        "ar": "Sharpen في المنتدى الثاني لصناعة المساحيق والمحافظ الخزفية للهواتف",
        "vi": "Sharpen tham gia Diễn đàn PM / Vỏ điện thoại gốm sứ lần thứ 2",
    },
    "simm2014": {
        "de": "Sharpen auf der SIMM 2014 (Shenzhen)",
        "ja": "Sharpen、SIMM 2014（深圳）に出展",
        "ko": "Sharpen, SIMM 2014(선전) 참가",
        "ru": "Sharpen на SIMM 2014 (Шэньчжэнь)",
        "es": "Sharpen en SIMM 2014 (Shenzhen)",
        "pt": "Sharpen na SIMM 2014 (Shenzhen)",
        "fr": "Sharpen à SIMM 2014 (Shenzhen)",
        "it": "Sharpen a SIMM 2014 (Shenzhen)",
        "tr": "Sharpen, SIMM 2014'te (Shenzhen)",
        "ar": "Sharpen في SIMM 2014 (شنتشن)",
        "vi": "Sharpen tham gia SIMM 2014 (Thâm Quyến)",
    },
    "manual-grinder-wheels": {
        "de": "Erfolg der Manuell-Schleifscheiben bei einem Unternehmen in Zhuzhou",
        "ja": "株洲の企業における手動研削盤用砥石の成功",
        "ko": "주저우 기업에서의 수동 연마기용 휠 성공 사례",
        "ru": "Успех ручных шлифовальных кругов на предприятии в Чжучжоу",
        "es": "Éxito de las muelas para rectificadoras manuales en una empresa de Zhuzhou",
        "pt": "Sucesso das rodas para retificadoras manuais em uma empresa de Zhuzhou",
        "fr": "Succès des meules pour rectifieuses manuelles dans une entreprise de Zhuzhou",
        "it": "Successo delle mole per rettificatrici manuali presso un'azienda di Zhuzhou",
        "tr": "Zhuzhou'daki bir işletmede manuel taşlama tezgâhı taşlarının başarısı",
        "ar": "نجاح عجلات الطحن اليدوية في شركة بمدينة تشوتشو",
        "vi": "Thành công của bánh mài máy mài thủ công tại doanh nghiệp Chu Châu",
    },
    "o400-1a1-batch-production": {
        "de": "Ø400mm 1A1 Cermet-gebundene Diamant- und CBN-Schleifscheiben in Serienfertigung",
        "ja": "Ø400mm 1A1 金属セラミック結合剤ダイヤモンド・CBN砥石の量産",
        "ko": "Ø400mm 1A1 세라메트 결합 다이아몬드 및 CBN 휠 양산",
        "ru": "Серийное производство алмазных и CBN кругов Ø400мм 1А1 на металлокерамической связке",
        "es": "Ruedas de diamante y CBN con liga cermet 1A1 de Ø400mm en producción en serie",
        "pt": "Rodas de diamante e CBN com liga cermet 1A1 de Ø400mm em produção em série",
        "fr": "Meules diamant et CBN à liant cermet 1A1 de Ø400mm en production de série",
        "it": "Mole diamantate e CBN con legante cermet 1A1 da Ø400mm in produzione di serie",
        "tr": "Ø400mm 1A1 sermet bağlı elmas ve CBN taşları seri üretimde",
        "ar": "عجلات الماس وCBN بقطر 400 ملم 1A1 مربوطة بالميتال سيراميك في الإنتاج المتسلسل",
        "vi": "Bánh mài kim cương và CBN liên kết xê-ramen 1A1 Ø400mm sản xuất hàng loạt",
    },
    "first-30000-sic-fine-grinding": {
        "de": "Chinas erste inländische 30000# SiC-Substrat-Feinschleifscheibe",
        "ja": "中国初の国産 30000# SiC基板用精密研削砥石",
        "ko": "중국 최초 국산 30000# SiC 기판 정밀 연삭 휠",
        "ru": "Первая в Китае отечественная тонкошлифовальная круг для SiC-подложек 30000#",
        "es": "Primera muela de rectificado fino para sustratos SiC 30000# nacional de China",
        "pt": "Primeira roda de retificação fina para substratos SiC 30000# nacional da China",
        "fr": "Première meule de finition pour substrats SiC 30000# nationale en Chine",
        "it": "Prima mola di rettifica fine per substrati SiC 30000# nazionale cinese",
        "tr": "Çin'in ilk yerli 30000# SiC altlık ince taşlama taşı",
        "ar": "أول حجر صقل دقيق للركائز SiC 30000# محلي الصنع في الصين",
        "vi": "Bánh mài tinh chế rãnh SiC 30000# nội địa đầu tiên của Trung Quốc",
    },
    "tinico-heat-spreader-dev": {
        "de": "Sharpen entwickelt TiNiCo-Superlegierungs-Wärmeverteiler für 3D-Heißbiegen",
        "ja": "Sharpen、3Dホットベンディング用TiNiCo超合金均熱板を開発",
        "ko": "Sharpen, 3D 핫 벤딩용 TiNiCo 초합금 히트 스프레더 개발",
        "ru": "Sharpen разработала теплораспределитель из суперсаплава TiNiCo для 3D-горячего гиба",
        "es": "Sharpen desarrolla un disipador de superaleación TiNiCo para el plegado en caliente 3D",
        "pt": "Sharpen desenvolve dissipador de superliga TiNiCo para dobra a quente 3D",
        "fr": "Sharpen développe un dissipateur de chaleur en superalliage TiNiCo pour le cintrage à chaud 3D",
        "it": "Sharpen sviluppa uno spreader di calore in superlega TiNiCo per la piegatura a caldo 3D",
        "tr": "Sharpen, 3D sıcak bükme için TiNiCo süperalaşım ısı dağıtıcı geliştirdi",
        "ar": "Sharpen تطور مشتت حرارة من سبيكة TiNiCo الفائقة للثني الساخن ثلاثي الأبعاد",
        "vi": "Sharpen phát triển tản nhiệt hợp kim siêu TiNiCo cho uốn nóng 3D",
    },
    "shanghai-customer-endmills": {
        "de": "Durchbruch bei der Radnutzung bei einem Shanghai-Kunden",
        "ja": "上海の顧客における砥石使用の飛躍的進展",
        "ko": "상하이 고객사의 휠 사용 성공 돌파",
        "ru": "Прорыв в применении кругов у шанхайского заказчика",
        "es": "Avance en el uso de muelas en un cliente de Shanghái",
        "pt": "Avanço no uso de rodas em um cliente de Xangai",
        "fr": "Percée dans l'utilisation des meules chez un client de Shanghai",
        "it": "Svolta nell'uso delle mole presso un cliente di Shanghai",
        "tr": "Shanghai'daki bir müşteride takım kullanımında atılım",
        "ar": "اختراق في استخدام العجلات لدى عميل في شنغهاي",
        "vi": "Đột phá trong sử dụng bánh mài tại khách hàng Thượng Hải",
    },
    "cnc-tool-failure-modes": {
        "de": "Ausfallarten von CNC-Werkzeugen und Gegenmaßnahmen",
        "ja": "CNC工具の故障形態と対策",
        "ko": "CNC 공구의 고장 형태 및 대책",
        "ru": "Виды отказов CNC-инструмента и меры противодействия",
        "es": "Modos de fallo de las herramientas CNC y contramedidas",
        "pt": "Modos de falha de ferramentas CNC e contramedidas",
        "fr": "Modes de défaillance des outils CNC et contre-mesures",
        "it": "Modalità di guasto degli utensili CNC e contromisure",
        "tr": "CNC takımlarının arıza modları ve karşı önlemler",
        "ar": "أنماط فشل أدوات CNC وإجراءات المواجهة",
        "vi": "Các dạng hỏng của dụng cụ CNC và biện pháp khắc phục",
    },
    "manufacturing-trends-abrasives": {
        "de": "Fertigungstrends erhöhen die Anforderungen an Schleifmittel",
        "ja": "製造業の動向が研削工具への要求を高める",
        "ko": "제조업 동향이 연마재에 대한 기준을 높이다",
        "ru": "Тенденции производства повышают планку для абразивов",
        "es": "Las tendencias de fabricación elevan el listón para los abrasivos",
        "pt": "Tendências de fabricação elevam o nível dos abrasivos",
        "fr": "Les tendances de fabrication relèvent l'exigence pour les abrasifs",
        "it": "Le tendenze manifatturiere alzano l'asticella per gli abrasivi",
        "tr": "Üretim trendleri aşındırıcılar için çıtayı yükseltiyor",
        "ar": "اتجاهات التصنيع ترفع سقف المتطلبات للمنتجات الكاشطة",
        "vi": "Xu hướng sản xuất nâng cao tiêu chuẩn cho vật liệu mài",
    },
    "diamond-product-storage": {
        "de": "Lagerungstipps für Diamantprodukte",
        "ja": "ダイヤモンド製品の保管のヒント",
        "ko": "다이아몬드 제품 보관 요령",
        "ru": "Советы по хранению алмазной продукции",
        "es": "Consejos de almacenamiento para productos de diamante",
        "pt": "Dicas de armazenamento para produtos de diamante",
        "fr": "Conseils de stockage pour les produits diamant",
        "it": "Consigli di stoccaggio per i prodotti in diamante",
        "tr": "Elmas ürünler için saklama ipuçları",
        "ar": "نصائح تخزين للمنتجات الماسية",
        "vi": "Mẹo bảo quản sản phẩm kim cương",
    },
    "cutting-tool-industry-sustainable": {
        "de": "Wie sich Chinas Schneidwerkzeugindustrie nachhaltig entwickeln kann",
        "ja": "中国の切削工具産業の持続可能な発展のために",
        "ko": "중국 절삭공구 산업의 지속 가능한 발전 방안",
        "ru": "Как устойчиво развиваться китайской отрасли режущего инструмента",
        "es": "Cómo puede desarrollarse de forma sostenible la industria de herramientas de corte de China",
        "pt": "Como a indústria chinesa de ferramentas de corte pode se desenvolver de forma sustentável",
        "fr": "Comment l'industrie chinoise de l'outil de coupe peut se développer durablement",
        "it": "Come l'industria cinese degli utensili da taglio può svilupparsi in modo sostenibile",
        "tr": "Çin'in kesici takım endüstrisi nasıl sürdürülebilir gelişebilir",
        "ar": "كيف يمكن لصناعة أدوات القطع في الصين أن تتطور بشكل مستدام",
        "vi": "Ngành công cụ cắt gọt Trung Quốc phát triển bền vững như thế nào",
    },
    "product-application-scope": {
        "de": "Produktanwendungsbereich",
        "ja": "製品の適用範囲",
        "ko": "제품 적용 범위",
        "ru": "Область применения продукции",
        "es": "Ámbito de aplicación de productos",
        "pt": "Escopo de aplicação de produtos",
        "fr": "Domaine d'application des produits",
        "it": "Ambito di applicazione dei prodotti",
        "tr": "Ürün uygulama kapsamı",
        "ar": "نطاق تطبيق المنتجات",
        "vi": "Phạm vi ứng dụng sản phẩm",
    },
    "tinico-hot-bending-frontier": {
        "de": "TiNiCo-Superlegierungs-Wärmeverteiler für 3D-Heißbiegen",
        "ja": "3Dホットベンディング用TiNiCo超合金均熱板",
        "ko": "3D 핫 벤딩용 TiNiCo 초합금 히트 스프레더",
        "ru": "Теплораспределитель из суперсаплава TiNiCo для 3D-горячего гиба",
        "es": "Disipador de superaleación TiNiCo para el plegado en caliente 3D",
        "pt": "Dissipador de superliga TiNiCo para dobra a quente 3D",
        "fr": "Dissipateur de chaleur en superalliage TiNiCo pour le cintrage à chaud 3D",
        "it": "Spreader di calore in superlega TiNiCo per la piegatura a caldo 3D",
        "tr": "3D sıcak bükme için TiNiCo süperalaşım ısı dağıtıcı",
        "ar": "مشتت حرارة من سبيكة TiNiCo الفائقة للثني الساخن ثلاثي الأبعاد",
        "vi": "Tản nhiệt hợp kim siêu TiNiCo cho uốn nóng 3D",
    },
    "pm-hss-introduction": {
        "de": "Einführung in den PM-Hochgeschwindigkeitsstahl von SAP",
        "ja": "SAP 粉末冶金高速鋼の概要",
        "ko": "SAP 분말야금 고속강 소개",
        "ru": "Введение в порошковую металлургию быстрорежущей стали SAP",
        "es": "Introducción al acero rápido de metalurgia de polvos SAP",
        "pt": "Introdução ao aço rápido de metalurgia do pó SAP",
        "fr": "Introduction à l'acier rapide de métallurgie des poudres SAP",
        "it": "Introduzione all'acciaio rapido di metallurgia delle polveri SAP",
        "tr": "SAP toz metalurjisi yüksek hızlı çeliğine giriş",
        "ar": "مقدمة في فولاذ السرعة العالي لصناعة المساحيق من SAP",
        "vi": "Giới thiệu thép tốc độ cao luyện kim bột SAP",
    },
}


def main():
    # 1) newsSlugs.json
    ns_path = os.path.join(ROOT, "_data", "newsSlugs.json")
    with open(ns_path, encoding="utf-8") as f:
        ns = json.load(f)
    updated = 0
    for slug, langmap in TITLES.items():
        for lang, title in langmap.items():
            ns.setdefault(slug, {})[lang] = title
            updated += 1
    with open(ns_path, "w", encoding="utf-8") as f:
        json.dump(ns, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("newsSlugs.json: %d titles written" % updated)

    # 2) detail pages + listing cards
    detail_done = 0
    listing_done = 0
    for lang in LANGS:
        # detail pages
        for slug, langmap in TITLES.items():
            title = langmap[lang]
            dp = os.path.join(ROOT, lang, "news", slug + ".md")
            if not os.path.exists(dp):
                print("  missing detail:", dp)
                continue
            with open(dp, encoding="utf-8") as f:
                txt = f.read()
            new = re.sub(r'(?m)^title: .*$', lambda m: 'title: ' + json.dumps(title, ensure_ascii=False), txt, count=1)
            if new != txt:
                with open(dp, "w", encoding="utf-8") as f:
                    f.write(new)
                detail_done += 1
        # listing cards
        lp = os.path.join(ROOT, lang, "news.md")
        if not os.path.exists(lp):
            continue
        with open(lp, encoding="utf-8") as f:
            txt = f.read()
        for slug, langmap in TITLES.items():
            title = langmap[lang]
            pat = re.compile(r'(<a href="/%s/news/%s/">)[^<]*(</a>)' % (lang, slug))
            new = pat.sub(lambda m: m.group(1) + html.escape(title) + m.group(2), txt)
            if new != txt:
                txt = new
                listing_done += 1
        with open(lp, "w", encoding="utf-8") as f:
            f.write(txt)
    print("detail pages updated: %d, listing cards updated: %d" % (detail_done, listing_done))


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Append per-language news + product folder collections to admin/config.yml.

The existing config only exposes the per-language *listing* pages (home/products/
about/contact/news .md files) as single-file collections, so editors could not
create a new article or a new product page. This adds, for each of the 14
languages, two folder collections pointing at the real content folders:

    <lang>/news/<slug>.md      -> 新闻文章 · <语言>
    <lang>/products/<slug>.md  -> 产品介绍 · <语言>

Both are `create: true`, so the editor gets a working "new entry" form. The
listing pages that display them are now rendered dynamically by
_includes/news-list.njk and _includes/products-list.njk, so a new entry shows up
on /<lang>/news/ and /<lang>/products/ with no generator script.

Idempotent: re-running does nothing if the collections are already present.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(ROOT, "admin", "config.yml")

# display name + the three existing newsSection values for that language
LANGS = [
    ("en", "English", ["Company News", "Industry News", "Industry Frontier"]),
    ("zh", "中文（简体）", ["公司新闻", "行业资讯", "行业前沿发展现状"]),
    ("zh-tw", "繁體中文", ["公司新聞", "行業資訊", "行業前沿發展現狀"]),
    ("de", "Deutsch", ["Unternehmensnachrichten", "Branchennews", "Technologietrends"]),
    ("ja", "日本語", ["企業ニュース", "業界動向", "業界最前線"]),
    ("ko", "한국어", ["기업 뉴스", "업종 뉴스", "산업 최전선"]),
    ("ru", "Русский", ["Корпоративные новости", "Отраслевые новости", "Технологии передового края"]),
    ("es", "Español", ["Noticias de empresa", "Noticias del sector", "Fronteras tecnológicas"]),
    ("pt", "Português", ["Notícias da empresa", "Notícias do setor", "Fronteras tecnológicas"]),
    ("fr", "Français", ["Actualités de l’entreprise", "Actualités du secteur", "Frontières technologiques"]),
    ("it", "Italiano", ["Notizie aziendali", "Notizie del settore", "Frontiere tecnologiche"]),
    ("tr", "Türkçe", ["Şirket haberleri", "Sektör haberleri", "Teknoloji gelişmeleri"]),
    ("ar", "العربية", ["أخبار الشركة", "أخبار القطاع", "تقنيات السانك"]),
    ("vi", "Tiếng Việt", ["Tin doanh nghiệp", "Tin ngành", "Công nghệ tiên tiến"]),
]

DATE_HINT = ("格式 YYYY-MM-DD，例 2026-10-03。留空则列表不显示日期；"
             "排序按日期由新到旧。")
SLUG_HINT = "小写英文，用短横线分隔，例 tinico-heat-spreader-dev；建议与文件名保持一致。"


def news_collection(code, disp, sections):
    opts = ", ".join('"%s"' % s for s in sections)
    return f'''  # ---- 新闻文章 · {disp}（可新增/编辑/删除）----
  - name: "news-{code}"
    label: "新闻文章 · {disp}"
    label_new: "新增新闻 · {disp}"
    folder: "{code}/news"
    create: true
    delete: true
    slug: "{{{{slug}}}}"
    editor:
      preview: false
    sortable_fields: ["newsDate", "title"]
    view_filters:
      - {{ label: "全部栏目", field: "newsSection", pattern: ".*" }}
{chr(10).join('      - {{ label: "%s", field: "newsSection", pattern: "%s" }}' % (s, s) for s in sections)}
    fields:
      - {{ label: "发布日期", name: "newsDate", widget: "string", required: false,
          pattern: ['^\\d{{4}}-\\d{{2}}-\\d{{2}}$', '^\\d{{4}}-\\d{{2}}-\\d{{2}}$'],
          hint: "{DATE_HINT}" }}
      - {{ label: "栏目", name: "newsSection", widget: "select",
          options: [{opts}], default: "{sections[0]}" }}
      - {{ label: "标题", name: "title", widget: "string" }}
      - {{ label: "SEO 描述", name: "description", widget: "text",
          hint: "列表页卡片摘要与搜索结果摘要，写 1-2 句。" }}
      - {{ label: "URL Slug", name: "newsSlug", widget: "string",
          hint: "{SLUG_HINT}" }}
      - {{ label: "正文", name: "body", widget: "markdown" }}
      - {{ label: "版式", name: "layout", widget: "hidden", default: "news-detail.njk" }}
      - {{ label: "语言代码", name: "lang", widget: "hidden", default: "{code}" }}
'''


CTA = {
    "en": "Request a quote",
    "zh": "索取报价",
    "zh-tw": "索取報價",
    "de": "Angebot anfordern",
    "ja": "お見積り依頼",
    "ko": "견적 요청",
    "ru": "Запросить цену",
    "es": "Solicitar presupuesto",
    "pt": "Solicitar orçamento",
    "fr": "Demander un devis",
    "it": "Richiedi un preventivo",
    "tr": "Teklif isteyin",
    "ar": "اطلب عرض سعر",
    "vi": "Yêu cầu báo giá",
}


def product_collection(code, disp):
    cta = CTA[code]
    skeleton = (
        '<div class="product-block">\n'
        '  <img class="pb-img" src="/assets/img/your-product.webp" alt="" loading="lazy" />\n'
        '  <div>\n'
        '    <h2>产品名称</h2>\n'
        '    <p>一段产品介绍。</p>\n'
        '    <ul class="specs">\n'
        '      <li>特点一</li>\n'
        '      <li>特点二</li>\n'
        '    </ul>\n'
        '    <div class="pb-cta"><a class="btn btn-primary" href="/%s/contact/">%s</a></div>\n'
        '  </div>\n'
        '</div>'
    ) % (code, cta)
    indented = "\n".join("          " + ln for ln in skeleton.split("\n"))
    return f'''  # ---- 产品介绍 · {disp}（可新增/编辑）----
  - name: "products-{code}"
    label: "产品介绍 · {disp}"
    label_new: "新增产品 · {disp}"
    folder: "{code}/products"
    create: true
    delete: true
    slug: "{{{{slug}}}}"
    editor:
      preview: false
    sortable_fields: ["title"]
    fields:
      - {{ label: "产品名称", name: "title", widget: "string" }}
      - {{ label: "SEO 描述", name: "description", widget: "text",
          hint: "写 1-2 句，用于搜索结果摘要。" }}
      - {{ label: "产品锚点 ID", name: "productId", widget: "string",
          hint: "小写英文短横线，例 strong-grooving-wheels。产品列表的锚点链接会用到。" }}
      - {{ label: "产品图", name: "productImage", widget: "image", required: false,
          hint: "先在媒体库上传，再选择文件。" }}
      - label: "产品详情 HTML"
        name: "body"
        widget: "code"
        default: |
{indented}
        hint: "请保留上面的 HTML 结构，只替换引号内的文字；图片地址填已上传的文件；联系按钮的路径必须是 /{code}/contact/。留空则产品列表不显示该产品。"
      - {{ label: "版式", name: "layout", widget: "hidden", default: "product-detail.njk" }}
      - {{ label: "页面类型", name: "pageType", widget: "hidden", default: "product" }}
      - {{ label: "语言代码", name: "lang", widget: "hidden", default: "{code}" }}
'''


def main():
    text = open(CONFIG, encoding="utf-8").read()
    if 'name: "news-en"' in text:
        print("config.yml already contains the news collections — nothing to do")
        return
    blocks = []
    for code, disp, sections in LANGS:
        blocks.append(news_collection(code, disp, sections))
        blocks.append(product_collection(code, disp))
    addition = "\n" + "\n".join(blocks)
    if not text.endswith("\n"):
        text += "\n"
    text += addition
    with open(CONFIG, "w", encoding="utf-8") as f:
        f.write(text)
    print("appended %d collections to admin/config.yml" % (len(LANGS) * 2))


if __name__ == "__main__":
    main()

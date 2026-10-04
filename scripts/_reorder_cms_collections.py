# -*- coding: utf-8 -*-
"""Editor-experience pass on admin/config.yml, now that Chinese is the single
content source:

1. Reorder the top-level collections so the Chinese ones come first (that is
   what the operator is supposed to edit), then the Chinese-sourced UI/site
   data, then the translated languages.
2. Give every collection a `description` that tells the operator whether it is
   the source or an auto-synced translation.

Text-level edit: keeps line endings and the compact `- { label: ... }` field
style, so the diff stays readable. Validated afterwards.
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "admin", "config.yml")

raw = io.open(P, "rb").read().decode("utf-8")
nl = "\r\n" if "\r\n" in raw else "\n"
text = raw.replace("\r\n", "\n")

DESC_SOURCE = ("内容源语种（简体中文）。在这里修改并发布后，GitHub Action 会自动把改动"
               "翻译同步到其余 13 个语种，无需手工处理其它语言。")
DESC_ZH_TW = "由简体中文自动同步生成。如需长期修改，请改「Pages (中文)/新闻(中文)/产品(中文)」下的对应内容。"
DESC_AUTO = "由简体中文自动同步生成（GitHub Action: i18n sync）。一般不需要手改；手改会在下次中文更新时被覆盖。"
DESC_UI = "界面文案（按钮、页脚、搜索框等）。这里只维护中文一列，其余 13 个语种会自动翻译。"
DESC_SITE = "站点信息（品牌名、联系方式、导航、页脚）。这里只维护中文相关的字段，其余语种会自动翻译。"
DESC_AI = "AI 在线客服的行为与话术配置（服务端使用，非页面文案）。"

DESCRIPTIONS = {
    "pages-zh": DESC_SOURCE, "news-zh": DESC_SOURCE, "products-zh": DESC_SOURCE,
    "pages-zh-tw": DESC_ZH_TW, "news-zh-tw": DESC_ZH_TW, "products-zh-tw": DESC_ZH_TW,
    "ui-strings": DESC_UI, "site-info": DESC_SITE, "ai-settings": DESC_AI,
}

ORDER = [
    "pages-zh", "news-zh", "products-zh",
    "ui-strings", "site-info",
    "pages-zh-tw", "news-zh-tw", "products-zh-tw",
    "pages-en", "news-en", "products-en",
    "news-de", "products-de", "news-ja", "products-ja", "news-ko", "products-ko",
    "news-ru", "products-ru", "news-es", "products-es", "news-pt", "products-pt",
    "news-fr", "products-fr", "news-it", "products-it", "news-tr", "products-tr",
    "news-ar", "products-ar", "news-vi", "products-vi",
    "ai-settings",
]

# --- locate the collections block -------------------------------------------
start = text.index("\ncollections:\n") + len("\ncollections:\n")
end = len(text)
for m in re.finditer(r"^[A-Za-z_]", text[start:], re.M):
    end = start + m.start()
    break
block = text[start:end]

# --- split into per-collection chunks ----------------------------------------
marker = re.compile(r"^  - name: \"([^\"]+)\"", re.M)
hits = list(marker.finditer(block))
if not hits:
    raise SystemExit("no collections found")
prefix = block[:hits[0].start()]
chunks = {}
for i, m in enumerate(hits):
    stop = hits[i + 1].start() if i + 1 < len(hits) else len(block)
    chunks[m.group(1)] = block[m.start():stop]

missing = [n for n in ORDER if n not in chunks]
extra = [n for n in chunks if n not in ORDER]
if missing or extra:
    raise SystemExit("order/catalogue mismatch — missing=%r extra=%r" % (missing, extra))

# --- insert / replace a one-line description ---------------------------------
def with_description(name, chunk):
    desc = DESCRIPTIONS.get(name, DESC_AUTO)
    line = '    description: "%s"\n' % desc
    if re.search(r"^    description: ", chunk, re.M):
        return re.sub(r"^    description: .*\n", line, chunk, count=1, flags=re.M)
    return re.sub(r"^(  - name: \"[^\"]+\"\n)(    label: .*\n)",
                  lambda m: m.group(1) + m.group(2) + line, chunk, count=1, flags=re.M)

new_block = prefix + "".join(with_description(n, chunks[n]) for n in ORDER)
out = text[:start] + new_block + text[end:]

io.open(P, "wb").write(out.replace("\n", nl).encode("utf-8"))
print("collections reordered:", len(ORDER))
print("descriptions added:", len(DESCRIPTIONS))

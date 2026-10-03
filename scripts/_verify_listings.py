# -*- coding: utf-8 -*-
"""Final equivalence check for the dynamic listing pages.

Wrapper-agnostic: group headings are read as the <h2> elements in document
order (the old generated markup only wrapped the FIRST group in .news-group,
so a wrapper-based parse cannot compare the two versions).
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "_site")
BASE = os.path.join(os.path.dirname(ROOT), "sharpen-listing-baseline")
LANGS = ["en", "zh", "zh-tw", "de", "ja", "ko", "ru", "es", "pt", "fr", "it", "tr", "ar", "vi"]

# The date paragraph is optional: the zh articles carry the date inside the
# description and have no newsDate front matter, exactly as before the refactor.
CARD = re.compile(
    r'news-card-title"><a href="([^"]*)">([^<]*)</a></h3>\s*'
    r'(?:<p class="news-card-date">([^<]*)</p>\s*)?'
    r'<p class="news-card-desc">(.*?)</p>', re.S)
H2 = re.compile(r"<h2>(.*?)</h2>")
PID = re.compile(r'<div class="product-block" id="([^"]+)"')

bad = []
for lang in LANGS:
    row = [lang]
    # ---- news ----
    b = open(os.path.join(BASE, "%s_news.html" % lang), encoding="utf-8").read()
    n = open(os.path.join(SITE, lang, "news", "index.html"), encoding="utf-8").read()
    bc, nc = CARD.findall(b), CARD.findall(n)
    bh, nh = H2.findall(b), H2.findall(n)
    notes = []
    if len(bc) != len(nc):
        notes.append("CARD-COUNT %d->%d" % (len(bc), len(nc)))
    if bh != nh:
        notes.append("GROUP-ORDER %s->%s" % (bh, nh))
    if set(x[0] for x in bc) != set(x[0] for x in nc):
        only_b = [x[0] for x in bc if x[0] not in {y[0] for y in nc}]
        only_n = [x[0] for x in nc if x[0] not in {x[0] for x in bc}]
        notes.append("URL-DIFF base_only=%s new_only=%s" % (only_b, only_n))
    if [x[1] for x in bc] != [x[1] for x in nc]:
        diff_t = [(x[1], y[1]) for x, y in zip(bc, nc) if x[1] != y[1]]
        notes.append("TITLE-DIFF %d %s" % (len(diff_t), diff_t[:2]))
    if [x[3] for x in bc] != [x[3] for x in nc]:
        diff_d = [(x[0], y[0]) for x, y in zip(bc, nc) if x[3] != y[3]]
        notes.append("DESC-DIFF %d %s" % (len(diff_d), [d[0] for d in diff_d[:3]]))
    row.append("news cards %d->%d groups %d->%d %s" % (
        len(bc), len(nc), len(bh), len(nh), "OK" if not notes else "; ".join(notes)))
    if notes:
        bad.append((lang, "news", notes))

    # ---- products ----
    b = open(os.path.join(BASE, "%s_products.html" % lang), encoding="utf-8").read()
    n = open(os.path.join(SITE, lang, "products", "index.html"), encoding="utf-8").read()
    bp, np_ = PID.findall(b), PID.findall(n)
    pnotes = []
    if bp != np_:
        pnotes.append("IDS %s->%s" % (bp, np_))
    if b.count('class="product-block"') != n.count('class="product-block"'):
        pnotes.append("BLOCK-COUNT %d->%d" % (b.count('class="product-block"'), n.count('class="product-block"')))
    # CTA links, specs blocks and the product-name heading must all survive
    for probe in ('pb-cta', 'class="specs"', 'btn btn-primary', '<h2>'):
        if b.count(probe) != n.count(probe):
            pnotes.append("%s %d->%d" % (probe, b.count(probe), n.count(probe)))
    row.append("products blocks %d->%d %s" % (
        b.count('class="product-block"'), n.count('class="product-block"'),
        "OK" if not pnotes else "; ".join(pnotes)))
    if pnotes:
        bad.append((lang, "products", pnotes))
    print(" | ".join(row))

print()
print("RESULT:", "all 28 listing pages equivalent" if not bad else "DIFFERENCES FOUND")
for item in bad:
    print("  ", item)

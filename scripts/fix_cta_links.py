# -*- coding: utf-8 -*-
"""Repair the cross-language "click menu -> bounce to English" bug.

Root cause
----------
1. .eleventy.js `navUrl` filter fell back to the English URL for any language
   that had no explicit key in site.js `nav` (only en/zh/zh-tw did), so the
   header/footer nav for de/ja/ko/... pointed at /en/... .

   That is fixed in .eleventy.js (navUrl now derives the URL from item.key +
   lang). Nothing to do in .md for it.

2. Every language's products listing (`<lang>/products.md`) had a hardcoded
   CTA `<a class="btn btn-primary" href="/en/contact/">` pointing at the
   ENGLISH contact page, so clicking "Request a quote" from any non-English
   product listing bounced the visitor to the English contact page.

This script only fixes #2 — idempotent, safe to re-run.
"""
import os, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ["en","zh","zh-tw","de","ja","ko","ru","es","pt","fr","it","tr","ar","vi"]

total = 0
for lang in LANGS:
    correct = 'href="/' + lang + '/contact/"'
    files = []
    listing = os.path.join(ROOT, lang, "products.md")
    if os.path.exists(listing):
        files.append(listing)
    files += sorted(glob.glob(os.path.join(ROOT, lang, "products", "*.md")))
    for path in files:
        with open(path, encoding="utf-8") as f:
            txt = f.read()
        changed = False
        for l2 in LANGS:
            bad = 'href="/' + l2 + '/contact/"'
            if l2 != lang and bad in txt:
                txt = txt.replace(bad, correct)
                changed = True
        if changed:
            with open(path, "w", encoding="utf-8") as fo:
                fo.write(txt)
            total += 1
            print("fixed CTA ->", correct, "in", os.path.relpath(path, ROOT))
print("Done. Files fixed:", total)

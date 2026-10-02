# -*- coding: utf-8 -*-
"""Inject localized product-card names into _data/products.js for 11 non-English
languages. Each language's products.md already has translated <h2> titles; we
copy them over the home-page card "name" field so home cards are localized.
(en and zh/zh-tw already have proper localized names in products.js.)"""
import re, json

P = "C:/Users/cll/WorkBuddy/2026-10-01-18-40-20/sharpen-export"
ids = ["strong-grooving-wheels","led-backgrinding-wheels","pm-high-speed-steel",
       "tinico-heat-spreader","sic-wafer-wheels","pv-ingot-wheels",
       "resin-wheels","steel-bonded-carbide"]
langs = ["de","ja","ko","ru","es","pt","fr","it","tr","ar","vi"]

# 1) read each lang's products.md h2 titles
loc = {}
for L in langs:
    t = open(f"{P}/{L}/products.md", encoding="utf-8").read()
    d = {}
    for pid in ids:
        m = re.search(r'id="' + pid + r'".*?<h2>(.*?)</h2>', t, re.S)
        d[pid] = (m.group(1).replace("&amp;","&").strip() if m else "")
    missing = [k for k,v in d.items() if not v]
    assert not missing, f"{L} missing: {missing}"
    loc[L] = d
print("extracted", len(loc), "langs, x", len(ids), "products each")

# 2) rewrite products.js: for each non-en/zh/zh-tw lang, replace card names
pj = open(f"{P}/_data/products.js", encoding="utf-8").read()
pj_orig = pj

# products.js is a CJS object literal. We do a targeted regex replace:
# within each language block, find the "id": "..." ... "name": "..." and swap
# the name to the localized one. Each card block looks like:
#   {
#     "id": "strong-grooving-wheels",
#     "name": "OLD",
#     "summary": "...",
#     "image": "..."
#   }
for L in langs:
    for pid in ids:
        new_name = loc[L][pid]
        # match the card whose id is pid and replace its "name" value.
        # The name sits right after the id line. Use a lookaround-safe pattern.
        pat = re.compile(
            r'("id":\s*"' + re.escape(pid) + r'",\s*\n\s*"name":\s*")(.*?)("\s*,)',
            re.S,
        )
        m = pat.search(pj)
        if not m:
            raise SystemExit(f"card not found: {L}/{pid}")
        # But there are 14 blocks with the same id; we must hit the one in THIS
        # language's array. Strategy: locate the array start for this lang, and
        # replace the NEXT occurrence of that id after that array start.
        lang_start = pj.find('"' + L + '"')
        # find the id occurrence at/after lang_start
        seg = pj[lang_start:]
        m2 = pat.search(seg)
        assert m2, f"no {L}/{pid} after lang start"
        old_name = m2.group(2)
        replacement = m2.group(1) + new_name + m2.group(3)
        # replace in pj at the right absolute position
        abs_start = lang_start + m2.start()
        pj = pj[:abs_start] + replacement + pj[abs_start + len(m2.group(0)):]
        # note: ids are unique per card, but the same id appears in EVERY lang
        # block. By anchoring to the lang's array start we hit the right one.
        # However after we mutate pj, subsequent ids in the same lang need the
        # (possibly shifted) lang start. Re-find lang start relative to the
        # id order: since we process ids in file order and each replacement is
        # roughly same length, re-locate is safest.
# Re-do more robustly: reset and process per language by slicing the lang block.
pj = pj_orig
for L in langs:
    # find array start index of "L": [
    anchor = re.search(r'"' + L + r'"\s*:\s*\[', pj)
    assert anchor, f"lang block not found: {L}"
    # find matching closing of this array (next lang key or end)
    next_lang = re.search(r'"\w[\w-]*"\s*:\s*\[|^\s*\}\s*;?\s*$', pj[anchor.end():], re.M)
    block_end = anchor.end() + (next_lang.start() if next_lang else len(pj))
    block = pj[anchor.end():block_end]
    new_block = block
    for pid in ids:
        new_name = loc[L][pid]
        pat = re.compile(
            r'("id":\s*"' + re.escape(pid) + r'",\s*\n\s*"name":\s*")(.*?)("\s*,)',
            re.S,
        )
        new_block, n = pat.subn(lambda mm: mm.group(1) + new_name + mm.group(3), new_block, count=1)
        assert n == 1, f"{L}/{pid} name not replaced"
    pj = pj[:anchor.end()] + new_block + pj[block_end:]

open(f"{P}/_data/products.js", "w", encoding="utf-8").write(pj)
print("products.js updated for", len(langs), "langs")

# verify: each non-en/zh/zh-tw home card name no longer equals its english name
import json as _json
# can't easily import CJS; just spot check a few via regex on the file
for L in ["it","ar","vi"]:
    anchor = re.search(r'"' + L + r'"\s*:\s*\[', pj)
    next_lang = re.search(r'"\w[\w-]*"\s*:\s*\[|^\s*\}\s*;?\s*$', pj[anchor.end():], re.M)
    block_end = anchor.end() + (next_lang.start() if next_lang else len(pj))
    block = pj[anchor.end():block_end]
    print(L, "strong-grooving name =", re.search(r'"id":\s*"strong-grooving-wheels",\s*\n\s*"name":\s*"(.*)"', block).group(1)[:50])

# -*- coding: utf-8 -*-
"""Phase 1 migration: make the CMS the single editing surface.

1. data/i18n.json  <- _data/i18n.js   (UI strings; _data/i18n.js becomes a loader)
2. data/site.json  <- _data/site.js   (brand/contact/nav/footer; loader shim)
3. Product card text: copy products.js `summary` into each product md front
   matter (the md stays the single source), and record the curated product
   order in _data/productOrder.json so _data/products.js can be regenerated.

Templates keep importing `i18n` / `site` / `products` exactly as before, so no
template changes are needed.
"""
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

LANGS = ["en", "zh", "zh-tw", "de", "ja", "ko", "ru", "es", "pt", "fr", "it",
         "tr", "ar", "vi"]

# ---------------------------------------------------------------- 1. JSON dump
def node_json(expr):
    out = subprocess.run(
        ["node", "-e", expr], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


i18n = node_json("process.stdout.write(JSON.stringify(require('./_data/i18n.js')))")
site = node_json("process.stdout.write(JSON.stringify(require('./_data/site.js')))")
products = node_json("process.stdout.write(JSON.stringify(require('./_data/products.js')))")

os.makedirs("data", exist_ok=True)
with open("data/i18n.json", "w", encoding="utf-8", newline="\n") as f:
    json.dump(i18n, f, ensure_ascii=False, indent=2)
    f.write("\n")
with open("data/site.json", "w", encoding="utf-8", newline="\n") as f:
    json.dump(site, f, ensure_ascii=False, indent=2)
    f.write("\n")

LOADER_I18N = '''// UI strings (home sections, buttons, search page labels) now live in
// data/i18n.json so the CMS collection "界面文案 / UI Strings" can edit them.
// This file stays as a thin loader so templates keep doing `i18n[lang]`.
module.exports = require("../data/i18n.json");
'''
LOADER_SITE = '''// Site-wide configuration now lives in data/site.json so the CMS collections
// "站点信息 / Site Info" can edit brand, contact details, navigation, footer
// and per-language brand strings. This file stays as a thin loader so
// .eleventy.js filters, seo.js and the templates keep importing the same shape.
module.exports = require("../data/site.json");
'''
open("_data/i18n.js", "w", encoding="utf-8", newline="\n").write(LOADER_I18N)
open("_data/site.js", "w", encoding="utf-8", newline="\n").write(LOADER_SITE)
print("JSON-ised i18n + site")

# ------------------------------------------- 2. product order + md summaries
order = [p["id"] for p in products["en"]]
with open("_data/productOrder.json", "w", encoding="utf-8", newline="\n") as f:
    json.dump(order, f, ensure_ascii=False, indent=2)
    f.write("\n")
print("product order:", order)

slugs = json.load(open("_data/productSlugs.json", encoding="utf-8"))
added = 0
for lang in LANGS:
    for p in products.get(lang) or []:
        slug = slugs.get(p["id"])
        if not slug:
            continue
        path = os.path.join(lang, "products", slug + ".md")
        if not os.path.exists(path):
            continue
        md = open(path, encoding="utf-8").read()
        fm = re.match(r"^(---\n.*?\n---\n)", md, re.DOTALL)
        if not fm:
            continue
        head, body = fm.group(1), md[fm.end():]
        if re.search(r"^summary:", head, re.MULTILINE):
            continue
        summary = p.get("summary") or ""
        # insert summary right after the description line so YAML stays tidy
        m = re.search(r"^description:.*$", head, re.MULTILINE)
        ins = "summary: " + json.dumps(summary, ensure_ascii=False) + "\n"
        if m:
            head = head[:m.end() + 1] + ins + head[m.end() + 1:]
        else:
            head = head.replace("---\n", "---\n" + ins, 1)
        open(path, "w", encoding="utf-8", newline="\n").write(head + body)
        added += 1
print("summaries added to product md:", added)

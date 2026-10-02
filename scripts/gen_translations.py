# -*- coding: utf-8 -*-
"""Generate localized index/products/about/contact for 11 non-en/zh languages.
Usage: python scripts/gen_translations.py
Each language key has 4 page bodies. Products are emitted in the localized
language; CTA links point at that language's /contact/ page.
"""
import os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Product block builder. `products` is a list of (id, name, intro, [specs]).
def products_block(lang, products, quote_label, quote_link):
    out = []
    out.append('---')
    out.append('layout: page.njk')
    out.append('lang: ' + lang)
    out.append('permalink: /' + lang + '/products/')
    out.append('title: ' + json.dumps(products[0][1], ensure_ascii=False))
    out.append('---')
    out.append('')
    for (pid, name, intro, specs) in products:
        out.append('<div class="product-block" id="%s">' % pid)
        out.append('  <img class="pb-img" src="%s" alt="%s" loading="lazy" />' % (PRODUCTS_IMG[pid], name))
        out.append('  <div>')
        out.append('    <h2>%s</h2>' % name)
        out.append('    <p>%s</p>' % intro)
        out.append('    <ul class="specs">')
        for sp in specs:
            out.append('      <li>%s</li>' % sp)
        out.append('    </ul>')
        out.append('    <div class="pb-cta"><a class="btn btn-primary" href="%s">%s</a></div>' % (quote_link, quote_label))
        out.append('  </div>')
        out.append('</div>')
        out.append('')
    return '\n'.join(out) + '\n'

# image map per product id
PRODUCTS_IMG = {
    "strong-grooving-wheels": "/assets/img/diamond-wheels.jpg",
    "led-backgrinding-wheels": "/assets/img/wafer-backgrind.jpg",
    "pm-high-speed-steel": "/assets/img/pm-steel.jpg",
    "tinico-heat-spreader": "/assets/img/tinico.jpg",
    "sic-wafer-wheels": "/assets/img/sic-wafer.jpg",
    "pv-ingot-wheels": "/assets/img/pv-ingot.jpg",
    "resin-wheels": "/assets/img/resin-wheels.png",
}

TRANSLATIONS = {}

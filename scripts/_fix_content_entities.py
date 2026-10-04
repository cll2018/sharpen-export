# -*- coding: utf-8 -*-
"""Content fixes uncovered by the single-source refactor:

1. HTML entities in front-matter strings (&amp; &quot; ...) were double-escaped
   by Nunjucks, so the LED product page rendered "&amp;amp;" in <title>/<h1>.
   Decode entities to real characters (templates escape once, correctly).
2. zh-tw product titles/summaries used the Simplified 硅 for silicon; Traditional
   Chinese uses 矽 (e.g. 碳化矽晶圓減薄砂輪).
3. en steel-bonded-carbide title restored to the fuller "Steel-Bonded Cemented
   Carbide" (the name previously shown on the cards).

NOTE: only the YAML front matter is touched -- the markdown body is raw HTML that
is emitted verbatim (not escaped by Nunjucks), so its entities must stay as-is.
"""
import glob
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

ENTITY_RE = re.compile(r"&(?:amp|lt|gt|quot|#39|apos|nbsp);")

# Front matter is delimited by a leading "---\n" and a following "\n---\n".
# The naive r"^(---\n)(.*?)..." fails because "." does not cross newlines
# without re.DOTALL -- use [\s\S]*? instead.
FM_RE = re.compile(r"\A---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)\Z")


def split_front_matter(md):
    """Return (head, body) or None when there is no YAML front matter."""
    m = FM_RE.match(md)
    if not m:
        return None
    return m.group(1), m.group(2)


def rewrite(path, head, body):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("---\n" + head + "\n---\n" + body)


FIELDS = ("title", "summary", "description", "newsDate", "newsSection")


def decode_entities_in_head(head):
    """Decode HTML entities found inside double-quoted YAML scalar values."""
    changed = False
    out_lines = []
    for ln in head.split("\n"):
        key = ln.split(":", 1)[0].strip()
        if key in FIELDS and ENTITY_RE.search(ln):
            m = re.match(r"^(\s*[\w]+:\s*)(\")(.*)(\")\s*$", ln)
            if m and ENTITY_RE.search(m.group(3)):
                ln = m.group(1) + '"' + html.unescape(m.group(3)) + '"'
                changed = True
        out_lines.append(ln)
    return "\n".join(out_lines), changed


# --- 1. decode double-escaped entities in front matter -----------------------
files = (sorted(glob.glob("*/products/*.md"))
         + sorted(glob.glob("*/news/*.md"))
         + sorted(glob.glob("*/*.md")))

n_entity = 0
for f in files:
    md = open(f, encoding="utf-8").read()
    fm = split_front_matter(md)
    if not fm:
        continue
    head, body = fm
    if not ENTITY_RE.search(head):
        continue
    new_head, changed = decode_entities_in_head(head)
    if changed:
        rewrite(f, new_head, body)
        n_entity += 1
print("files with decoded entities:", n_entity)


# --- 2. zh-tw: Simplified 硅 -> Traditional 矽 in product front matter -------
n_tw = 0
for f in sorted(glob.glob("zh-tw/products/*.md")):
    md = open(f, encoding="utf-8").read()
    fm = split_front_matter(md)
    if not fm:
        continue
    head, body = fm
    lines = []
    hit = False
    for ln in head.split("\n"):
        key = ln.split(":", 1)[0].strip()
        if key in ("title", "summary", "description") and "硅" in ln:
            ln = ln.replace("硅", "矽")
            hit = True
        lines.append(ln)
    if hit:
        rewrite(f, "\n".join(lines), body)
        n_tw += 1
print("zh-tw product files with 硅->矽:", n_tw)


# --- 3. en steel-bonded-carbide fuller title --------------------------------
p = "en/products/steel-bonded-carbide.md"
if os.path.exists(p):
    md = open(p, encoding="utf-8").read()
    if 'title: "Steel-Bonded Carbide"' in md:
        md = md.replace('title: "Steel-Bonded Carbide"',
                        'title: "Steel-Bonded Cemented Carbide"', 1)
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(md)
        print("en steel-bonded title restored to 'Steel-Bonded Cemented Carbide'")
    else:
        print("en steel-bonded title already OK")


# --- 4. keep the JSON loaders in sync ---------------------------------------
if os.path.exists("_data/newsSlugs.json"):
    news_slugs = json.load(open("_data/newsSlugs.json", encoding="utf-8"))
    changed_slugs = 0
    for slug, per_lang in news_slugs.items():
        for lang in list(per_lang.keys()):
            val = per_lang[lang]
            if isinstance(val, str) and ENTITY_RE.search(val):
                per_lang[lang] = html.unescape(val)
                changed_slugs += 1
    if changed_slugs:
        with open("_data/newsSlugs.json", "w", encoding="utf-8",
                  newline="\n") as fh:
            json.dump(news_slugs, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
    print("newsSlugs.json entity fixes:", changed_slugs)

"""
Force-rewrite front-matter in 11 languages using the page filename.
- Keep title/description/heroTitle/heroLead values as-is (with internal quotes escaped)
- Force lang and permalink from disk
"""
import re, os

ROOT = "sharpen-export"
PAGES = ["index", "about", "contact", "products", "news"]
LANGS = ["de","ja","ko","ru","es","pt","fr","it","tr","ar","vi"]
KEEP_KEYS = ["layout", "lang", "permalink", "title", "description", "heroTitle", "heroLead"]

def fix_front_matter(text, lang, page):
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if not m:
        return text, False
    fm_block = m.group(1)
    rest = text[m.end():]
    lines = fm_block.split("\n")
    # Parse each key: value pair; capture any key (including layout, title, heroTitle etc)
    parsed = {}
    order = []
    for ln in lines:
        if ":" not in ln:
            continue
        key, _, val = ln.partition(":")
        key = key.strip()
        val = val.strip()
        if key not in parsed:
            order.append(key)
        parsed[key] = val
    # Escape internal double quotes in all values
    for k in parsed:
        v = parsed[k]
        if v.startswith('"') and v.endswith('"') and len(v) >= 2:
            inner = v[1:-1].replace('"', '「')
            parsed[k] = '"' + inner + '"'
        elif v.startswith("'") and v.endswith("'") and len(v) >= 2:
            inner = v[1:-1].replace("'", "")
            parsed[k] = "'" + inner + "'"
    # Force lang and permalink
    parsed["lang"] = lang
    parsed["permalink"] = f"/{lang}/" if page == "index" else f"/{lang}/{page}/"
    # Ensure layout exists
    parsed.setdefault("layout", "page.njk" if page != "index" else "home.njk")
    # Build new fm, keeping original key order + add missing required keys at top
    new_lines = []
    for key in KEEP_KEYS:
        if key in parsed:
            new_lines.append(f"{key}: {parsed[key]}")
    for key in order:
        if key not in KEEP_KEYS:
            new_lines.append(f"{key}: {parsed[key]}")
    new_fm = "\n".join(new_lines)
    return f"---\n{new_fm}\n---\n" + rest, True

ok = 0
changed = 0
for lang in LANGS:
    for page in PAGES:
        path = os.path.join(ROOT, lang, f"{page}.md")
        if not os.path.exists(path):
            print(f"MISSING {path}")
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        new_text, had_fm = fix_front_matter(text, lang, page)
        if had_fm:
            ok += 1
        if new_text != text:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_text)
            changed += 1
print(f"OK {ok}/55, changed {changed}")

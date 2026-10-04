# -*- coding: utf-8 -*-
"""Localize the `description` meta field of the 14 scoped news articles.

The 14 slugs are the same ones whose BODY was translated in
translate_news_bodies.py. Their <lang>/news/<slug>.md files still carry an
ENGLISH `description` in the 11 non-English/Chinese languages (de/ja/ko/ru/
es/pt/fr/it/tr/ar/vi). en/zh/zh-tw descriptions are already correct and are
left untouched.

We DERIVE a clean, complete localized description from each language's
already-translated <p> body (first sentence, truncated ~180 chars). This keeps
the description in the page's own language, fixes the truncated English
snippets, and stays consistent with the body.

Idempotent: it only rewrites the `description:` front-matter line and only when
the value actually changes.
"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LANGS = ["de", "ja", "ko", "ru", "es", "pt", "fr", "it", "tr", "ar", "vi"]

# Pull the 14 scoped slugs straight from the body-translation script so the two
# stay in lock-step.
with open(os.path.join(ROOT, "scripts", "translate_news_bodies.py"), encoding="utf-8") as f:
    bodies_src = f.read()
SLUGS = re.findall(r'^\s*"([a-z0-9-]+)":\s*\{', bodies_src, re.M)
# keep only top-level slug keys (exclude the 2-letter language keys)
SLUGS = [s for s in SLUGS if s not in LANGS]
# de-dup preserving order
seen = set(); SLUGS = [s for s in SLUGS if not (s in seen or seen.add(s))]


def first_paragraph_text(md):
    m = re.search(r"<p>(.*?)</p>", md, re.DOTALL)
    if not m:
        return ""
    return re.sub(r"<[^>]+>", "", m.group(1)).replace("\n", " ").strip()


# Sentence-ending punctuation, Latin + CJK. Cutting descriptions at a real
# boundary (no dangling "…") keeps Google from rewriting the snippet and
# reads correctly inside NewsArticle schema.
_SENT_END = ".!?。！？"
_CLAUSE_END = ";,，、；"

# Sentence-ending punctuation, Latin + CJK. Cutting descriptions at a real
# boundary (no dangling "…") keeps Google from rewriting the snippet and
# reads correctly inside NewsArticle schema.
_SENT_END = ".!?。！？"
_CLAUSE_END = ";,，、；"

# Sentence-ending punctuation, Latin + CJK. Cutting descriptions at a real
# boundary (no dangling "...") keeps Google from rewriting the snippet and
# reads correctly inside NewsArticle schema.
_SENT_END = ".!?。！？"
_CLAUSE_END = ";,，、；"


def make_desc(text, limit=200):
    txt = (text or "").strip()
    if not txt:
        return ""

    if len(txt) <= limit:
        return txt
    cut = txt[:limit]
    # 1) Prefer the last full-sentence end inside the limit.
    sp = max(cut.rfind(ch) for ch in _SENT_END)
    if sp >= int(limit * 0.4):
        return cut[: sp + 1].rstrip()
    # 2) Otherwise extend just past the limit to the next sentence end
    #    rather than cutting the sentence in half.
    m = re.search(r"[.!?。]", txt[limit : limit + 80])
    if m:
        return txt[: limit + m.end()].strip()
    # 3) Otherwise the last clause boundary (comma/semicolon) inside the limit.
    sp = max(cut.rfind(ch) for ch in _CLAUSE_END)
    if sp >= int(limit * 0.5):
        return cut[: sp + 1].rstrip()
    # 4) Degenerate single long sentence: word-boundary cut when possible,
    #    otherwise hard cut; strip dangling punctuation either way.
    sp = cut.rfind(" ")
    if sp > int(limit * 0.6):
        cut = cut[:sp]
    return cut.rstrip(" \t" + _SENT_END + _CLAUSE_END + "-–—")


def replace_description(fm_text, new_val):
    # Replace the `description:` line inside the front matter only.
    def _sub(m):
        return "description: " + json.dumps(new_val, ensure_ascii=False)
    return re.sub(r'(?m)^description:.*$', _sub, fm_text, count=1)


def main():
    updated = 0
    missing = 0
    for slug in SLUGS:
        for lang in LANGS:
            dp = os.path.join(ROOT, lang, "news", slug + ".md")
            if not os.path.exists(dp):
                missing += 1
                continue
            txt = open(dp, encoding="utf-8").read()
            fm = re.search(r"^---\n(.*?)\n---\n", txt, re.DOTALL)
            if not fm:
                print("NO FM:", dp)
                continue
            body = first_paragraph_text(txt)
            new_desc = make_desc(body)
            if not new_desc:
                print("NO BODY:", dp)
                continue
            new_fm = replace_description(fm.group(1), new_desc)
            if new_fm == fm.group(1):
                continue  # unchanged
            new_txt = txt.replace(fm.group(0), "---\n" + new_fm + "\n---\n", 1)
            open(dp, "w", encoding="utf-8").write(new_txt)
            updated += 1
    print("slugs:", len(SLUGS), "langs:", len(LANGS),
          "descriptions updated:", updated, "missing files:", missing)


if __name__ == "__main__":
    main()

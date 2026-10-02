#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Translate the 11 non-English news bodies in {lang}/news.md using the
free (no-key) Google Translate web endpoint.

For each target lang and each "### article" block, take the English source
body (the lines after the date line up to the next "### "), translate it to
the target lang, and write the localized body back into {lang}/news.md while
preserving the title (already localized) and the date/category lines.

The English source bodies live in the 'en'/'zh' news.md, but the 11 langs
currently reuse the EN body, so we translate per-block: split the file into
blocks, keep the header (title + date), replace body paragraphs with the
translation of the corresponding EN block (matched by order/date).
"""
import re, os, json, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOOGLE = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl={tl}&dt=t&q={q}"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# target langs to localize news bodies for
TARGETS = ["de","ja","ko","ru","es","pt","fr","it","tr","ar","vi"]

def gtranslate(text, tl):
    q = urllib.parse.quote(text)
    url = GOOGLE.format(tl=tl, q=q)
    req = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                data = json.loads(r.read().decode("utf-8", "replace"))
            parts = [seg[0] for seg in data[0] if seg and seg[0]]
            return "".join(parts).strip()
        except Exception:
            if attempt == 3:
                return text  # give up: keep English rather than break the page
            time.sleep(3)
    return text

def parse_blocks(path):
    """Return list of dict(title, date, body, full) preserving order.
    The block is split by '### ' headers. The date marker line (localized per
    language, or *YYYY-MM-DD*) is preserved verbatim in `header_tail` so we
    only ever replace the body paragraphs."""
    txt = open(path, encoding="utf-8").read()
    blocks = []
    # Each article starts with "### <title>\n" then a date marker line, then body.
    for m in re.finditer(r"### ([^\n]+)\n", txt):
        title = m.group(1).strip()
        start = m.end()
        # capture the date-marker line (starts with '*') right after the title
        dm = re.match(r"(\*[^*\n]*\d{4}-\d{2}-\d{2}\*)", txt[start:])
        date_line = dm.group(1) if dm else ""
        body_start = start + len(date_line)
        nxt = txt.find("\n### ", body_start)
        body = txt[body_start:nxt] if nxt > 0 else txt[body_start:]
        body = body.strip()
        blocks.append({"title": title, "date_line": date_line, "body": body})
    return blocks

if __name__ == "__main__":
    import sys
    dry = "--dry" in sys.argv
    lang_arg = sys.argv[sys.argv.index("--lang")+1] if "--lang" in sys.argv else None
    targets = [lang_arg] if lang_arg else TARGETS
    en_blocks = parse_blocks(os.path.join(HERE, "en", "news.md"))
    print(f"EN source blocks: {len(en_blocks)}")
    for tl in targets:
        p = os.path.join(HERE, tl, "news.md")
        cur = parse_blocks(p)
        n = min(len(cur), len(en_blocks))
        out = []
        for i in range(n):
            src = en_blocks[i]["body"]
            title = cur[i]["title"]
            dline = cur[i]["date_line"]
            if dry:
                print(f"  [{tl}] #{i+1} '{title[:28]}' date='{dline}' src_len={len(src)}")
                continue
            tr = gtranslate(src, tl)
            out.append(f"### {title}\n{dline}\n\n{tr}")
        if not dry:
            open(p, "w", encoding="utf-8").write("\n".join(out))
            print(f"  [{tl}] wrote {n} localized news blocks")
    if dry:
        print("(dry run — no files written)")

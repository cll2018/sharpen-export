# -*- coding: utf-8 -*-
"""De-duplicate the leading H1 in about/news pages.

page.njk already renders <h1>{{ title }}</h1>. The .md bodies also start with
a markdown `# <primary heading>` that repeats that same semantic title, which
produces two H1s per page. This script removes only that leading `# ...` line
(the first heading after the front matter). The remaining `##` / `###` sections
keep their relative hierarchy. Idempotent: once removed, the file no longer
has a leading H1, so a re-run is a no-op.

Usage: python scripts/fix_h1_about_news.py
"""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARKER = "<!-- DE-DUPED: leading single-level heading removed (template owns the page title) -->"


def process(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")

    # find end of front matter (closing ---)
    if lines[0].strip() != "---":
        print("SKIP (no front matter):", os.path.relpath(path, ROOT))
        return False
    fm_end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm_end = i
            break
    if fm_end is None:
        print("SKIP (no closing ---):", os.path.relpath(path, ROOT))
        return False

    # skip blank lines after front matter, then look for the first '# ' heading
    j = fm_end + 1
    while j < len(lines) and lines[j].strip() == "":
        j += 1
    if j >= len(lines) or not lines[j].startswith("# ") :
        # already fixed (idempotent) or no leading H1
        return False
    # this is the duplicated leading H1 — replace with the marker comment + blank
    new_lines = lines[:j] + [MARKER, ""] + lines[j + 1:]
    # collapse the blank lines we may have just doubled up
    out = []
    prev_blank = False
    for ln in new_lines:
        is_blank = ln.strip() == ""
        if is_blank and prev_blank:
            continue
        out.append(ln)
        prev_blank = is_blank
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("fixed:", os.path.relpath(path, ROOT))
    return True


def main():
    n = 0
    for lang_dir in glob.glob(os.path.join(ROOT, "*", "")):
        for page in ("about", "news"):
            p = os.path.join(lang_dir, page + ".md")
            if os.path.exists(p) and process(p):
                n += 1
    print("processed %d files." % n)


if __name__ == "__main__":
    main()

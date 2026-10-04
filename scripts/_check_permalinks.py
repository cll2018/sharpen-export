# -*- coding: utf-8 -*-
"""Check that every content page's explicit `permalink` matches where Eleventy
would emit it by default. If they agree, the permalink line is redundant and the
Decap CMS can safely manage these files without a permalink field."""
import glob
import io
import os
import re

LANGS = {"en", "zh", "zh-tw", "de", "ja", "ko", "ru", "es", "pt", "fr", "it",
         "tr", "ar", "vi"}

files = [p.replace("\\", "/") for p in glob.glob("*/*.md") + glob.glob("*/*/*.md")]
n = 0
bad = []
for f in files:
    if f.split("/")[0] not in LANGS:
        continue
    s = io.open(f, encoding="utf-8").read()
    expected = "/" + os.path.splitext(f)[0] + "/"
    m = re.search(r"^permalink:[ \t]*(\S+)", s, re.M)
    if not m:
        bad.append((f, "<missing> -> default " + expected))
        continue
    n += 1
    if m.group(1) != expected:
        bad.append((f, m.group(1) + "  !=  " + expected))

print("files with explicit permalink:", n)
print("missing or mismatched:", len(bad))
for f, v in bad[:25]:
    print("   ", f, "->", v)

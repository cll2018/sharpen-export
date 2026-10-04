# -*- coding: utf-8 -*-
"""Make admin/config.yml deterministic about the fields that decide URLs.

Two problems this fixes:

1. Folder collections used `slug: "{{slug}}"`, i.e. the file name came from the
   entry title. A Chinese title therefore produced a non-ASCII file name and
   consequently a non-ASCII URL. New entries now take their file name from the
   operator-entered ASCII slug (`newsSlug` / `productId`), so the URL stays
   `/zh/news/<slug>/` and the automatic translation keeps the same path in all
   13 other languages.

2. Page (file) collections had no `permalink` field. All 504 permalinks on the
   site currently happen to equal Eleventy's default output path, so nothing is
   broken today — but a page's `permalink` was not represented in the CMS at
   all, and would have been lost the first time a page needed a different URL.
   Each page file now carries a hidden `permalink` field pinned to its real URL.

Text-level edit so the compact `- { label: ... }` field style survives.
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "admin", "config.yml")

raw = io.open(P, "rb").read().decode("utf-8")
nl = "\r\n" if "\r\n" in raw else "\n"
text = raw.replace("\r\n", "\n")

start = text.index("\ncollections:\n") + len("\ncollections:\n")
end = len(text)
for m in re.finditer(r"^[A-Za-z_]", text[start:], re.M):
    end = start + m.start()
    break
head, block, tail = text[:start], text[start:end], text[end:]

COLL = re.compile(r"^  - name: \"([^\"]+)\"", re.M)
hits = list(COLL.finditer(block))
order = [m.group(1) for m in hits]
chunks = {}
for i, m in enumerate(hits):
    stop = hits[i + 1].start() if i + 1 < len(hits) else len(block)
    chunks[m.group(1)] = block[m.start():stop]

stats = {"slug": 0, "required": 0, "permalink": 0}

FILE_ENTRY = re.compile(r"^      - name: ")
FIELD_LINE = re.compile(r"^          - ")


def harden_folder(name, chunk):
    """Point the entry file name at the ASCII slug field the operator fills in."""
    if name.startswith("news-"):
        field, label = "newsSlug", "URL Slug"
    elif name.startswith("products-"):
        field, label = "productId", "产品锚点 ID"
    else:
        return chunk

    chunk, n = re.subn(r'^    slug: "\{\{slug\}\}"$',
                       '    slug: "{{%s}}"' % field, chunk, count=1, flags=re.M)
    stats["slug"] += n
    if not n:
        return chunk

    # a slug template reading an empty field would produce an empty file name
    pattern = r'(\- \{ label: "%s", name: "%s", widget: "string")' % (re.escape(label), field)
    if re.search(pattern + r", required: true", chunk):
        return chunk
    chunk, k = re.subn(pattern, r"\1, required: true", chunk, count=1)
    stats["required"] += k
    return chunk


def permalink_for(path):
    stem = path[:-3] if path.endswith(".md") else path
    if stem.endswith("/index"):
        stem = stem[: -len("/index")]
    return "/" + stem + "/"


def harden_page_file(chunk):
    """Add a hidden, pre-filled permalink to every page file entry."""
    lines = chunk.split("\n")
    out = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        out.append(ln)
        mf = re.match(r'^        file: "([^"]+\.md)"$', ln)
        if not mf:
            i += 1
            continue

        # this file entry runs until the next "      - name:" or a new collection
        j = i + 1
        while j < len(lines) and not FILE_ENTRY.match(lines[j]) \
                and not COLL.match(lines[j]):
            j += 1
        fields = [k for k in range(i, j) if FIELD_LINE.match(lines[k])]
        already = any("permalink" in lines[k] for k in fields)
        if fields and not already:
            # copy everything up to and including the last field, then append
            for k in range(i + 1, fields[-1] + 1):
                out.append(lines[k])
            out.append(
                '          - { label: "固定网址（由文件路径决定）", name: "permalink", '
                'widget: "hidden", default: "%s" }' % permalink_for(mf.group(1)))
            stats["permalink"] += 1
            i = fields[-1] + 1
            continue
        i += 1
    return "\n".join(out)


for name in order:
    chunk = chunks[name]
    if re.search(r"^    folder: ", chunk, re.M):
        chunk = harden_folder(name, chunk)
    elif re.search(r"^    files:", chunk, re.M):
        chunk = harden_page_file(chunk)
    chunks[name] = chunk

out = head + "".join(chunks[n] for n in order) + tail
io.open(P, "wb").write(out.replace("\n", nl).encode("utf-8"))

print("slug templates rewritten:", stats["slug"])
print("required flags added    :", stats["required"])
print("hidden permalink fields :", stats["permalink"])

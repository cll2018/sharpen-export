# -*- coding: utf-8 -*-
"""Convert the 8 product images (jpg/png) under assets/img to WebP and rewrite
every reference in the repo to point at the .webp files.

Idempotent: re-running re-converts (overwrites the .webp) and re-applies the
string substitutions. Originals are deleted only after a verification pass
confirms zero leftover references to the old paths.

Usage: python scripts/webp_images.py
"""
import os, glob
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets", "img")

# Source images to convert (the 8 product images actually referenced site-wide).
# cbn-wheels.jpg is currently an unused orphan and is left untouched.
SOURCES = [
    "diamond-wheels.jpg",
    "wafer-backgrind.jpg",
    "pm-steel.jpg",
    "tinico.jpg",
    "sic-wafer.jpg",
    "pv-ingot.jpg",
    "resin-wheels.png",
    "steel-bonded-carbide.png",
]

# 0-byte orphan image scheduled for removal.
ORPHAN = "sic-fine-grind.png"

SKIP_DIRS = {"node_modules", "_site", ".git", ".workbuddy"}

# Build the path->path replacement map (forward-slash, as it appears in content).
MAPPING = {}
for s in SOURCES:
    base, _ = os.path.splitext(s)
    MAPPING["/assets/img/" + s] = "/assets/img/" + base + ".webp"


def convert_one(src_name):
    src = os.path.join(ASSETS, src_name)
    if not os.path.exists(src):
        print("  skip (missing):", src_name)
        return
    base, _ = os.path.splitext(src_name)
    dst = os.path.join(ASSETS, base + ".webp")
    im = Image.open(src)
    # Keep alpha if present; otherwise normalize to RGB.
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        im = im.convert("RGBA")
    elif im.mode != "RGB":
        im = im.convert("RGB")
    im.save(dst, "WEBP", quality=82, method=6)
    old = os.path.getsize(src)
    new = os.path.getsize(dst)
    print("  %-28s %8d -> %8d bytes (%.1f%%)" % (src_name, old, new, 100.0 * new / old))


def iter_content_files():
    for ext in ("*.md", "*.js", "*.njk", "*.html"):
        for path in glob.glob(os.path.join(ROOT, "**", ext), recursive=True):
            parts = path.split(os.sep)
            if any(d in SKIP_DIRS for d in parts):
                continue
            yield path


def replace_refs():
    total = 0
    for path in iter_content_files():
        try:
            with open(path, encoding="utf-8") as f:
                txt = f.read()
        except Exception:
            continue
        new = txt
        cnt = 0
        for a, b in MAPPING.items():
            n = new.count(a)
            if n:
                new = new.replace(a, b)
                cnt += n
        if new != txt:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new)
            total += cnt
            print("  updated %s (%d repl)" % (os.path.relpath(path, ROOT), cnt))
    return total


def verify_no_leftover():
    leftover = 0
    for path in iter_content_files():
        try:
            txt = open(path, encoding="utf-8").read()
        except Exception:
            continue
        for a in MAPPING:
            c = txt.count(a)
            if c:
                leftover += c
                print("  LEFTOVER %s in %s" % (a, os.path.relpath(path, ROOT)))
    return leftover


def main():
    print("== Converting product images to WebP ==")
    for s in SOURCES:
        convert_one(s)
    print("== Rewriting references ==")
    n = replace_refs()
    print("  total replacements: %d" % n)
    print("== Verifying no leftover old refs ==")
    leftover = verify_no_leftover()
    print("  leftover old refs: %d" % leftover)
    if leftover == 0:
        for s in SOURCES:
            p = os.path.join(ASSETS, s)
            if os.path.exists(p):
                os.remove(p)
                print("  deleted original", s)
    else:
        print("  NOT deleting originals (leftover refs present)")
    op = os.path.join(ASSETS, ORPHAN)
    if os.path.exists(op) and os.path.getsize(op) == 0:
        os.remove(op)
        print("  deleted orphan", ORPHAN)


if __name__ == "__main__":
    main()

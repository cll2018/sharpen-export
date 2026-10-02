#!/usr/bin/env python
"""Strip leading ```markdown fence and trailing ``` from 2 files."""
import os

ROOT = "sharpen-export"
FILES = ["es/contact.md", "it/about.md"]

def fix(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    lines = text.split("\n")
    # strip leading fence (if line 0 is ```markdown or ```)
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    # strip trailing fence (if last non-empty line is ```)
    while lines and lines[-1].strip() in ("", "```"):
        lines.pop()
    # strip trailing ``` if it's second-to-last
    if lines and lines[-1].strip() == "```":
        lines.pop()
    while lines and lines[-1].strip() == "":
        lines.pop()
    out = "\n".join(lines) + "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"OK {path}: {len(lines)} lines")

for rel in FILES:
    fix(os.path.join(ROOT, rel))

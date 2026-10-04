# -*- coding: utf-8 -*-
"""Augment data/translation-glossary.json:

1. Add Traditional-Chinese (zh-tw) renderings for every glossary term, since the
   shared table was extracted from a source that only covered 12 languages.
2. Repair a corrupted Arabic rendering of 粉末冶金高速钢 that contained the
   stray Latin fragment "Kata".
"""
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(ROOT, "data", "translation-glossary.json")
d = json.load(io.open(p, encoding="utf-8"))

ZH_TW = {
    "萨普新材": "薩普新材",
    "长沙市萨普新材料有限公司": "長沙市薩普新材料有限公司",
    "金刚石砂轮": "鑽石砂輪",
    "CBN砂轮": "CBN砂輪",
    "硬质合金": "硬質合金",
    "金属陶瓷结合剂": "金屬陶瓷結合劑",
    "树脂结合剂": "樹脂結合劑",
    "碳化硅晶圆减薄砂轮": "碳化矽晶圓減薄砂輪",
    "粉末冶金高速钢": "粉末冶金高速鋼",
    "均热板": "均熱板",
    "五轴数控磨削": "五軸數控磨削",
}

missing = [row[0] for row in d["glossary"] if row[0] not in ZH_TW]
if missing:
    raise SystemExit("no zh-tw rendering for: " + repr(missing))

d["glossaryExtra"] = {row[0]: {"zh-tw": ZH_TW[row[0]]} for row in d["glossary"]}

# repair the Arabic typo, if still present
fixed = 0
for row in d["glossary"]:
    for i, v in enumerate(row):
        if isinstance(v, str) and "Kata" in v:
            row[i] = v.replace("عالية السرKata", "عالية السرعة")
            fixed += 1
d["glossaryFixedArabic"] = fixed

with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")

print("glossary rows:", len(d["glossary"]))
print("zh-tw renderings added:", len(d["glossaryExtra"]))
print("arabic rows repaired:", fixed)

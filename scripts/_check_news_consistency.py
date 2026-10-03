import re, glob
LANGS = ["en","zh","zh-tw","de","ja","ko","ru","es","pt","fr","it","tr","ar","vi"]
sets = {}
for l in LANGS:
    slugs = set()
    for f in glob.glob(f"{l}/news/*.md"):
        t = open(f, encoding="utf-8").read()
        m = re.search(r"(?m)^newsSlug:\s*(\S+)\s*$", t)
        if m:
            slugs.add(m.group(1))
    sets[l] = slugs
all_slugs = set().union(*sets.values())
print("total distinct slugs across all langs:", len(all_slugs))
for l in LANGS:
    missing = sorted(all_slugs - sets[l])
    flag = "" if not missing else "  <-- MISSING: " + ",".join(missing)
    print(f"{l}: count={len(sets[l])}{flag}")
print("slugs:", sorted(all_slugs))

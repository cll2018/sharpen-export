# -*- coding: utf-8 -*-
"""
Safe deploy to GitHub (cll2018/sharpen-export) via the Git Database API.
Builds a new tree on top of the live HEAD (fast-forward only) so we never
revert the live site or drop files. Excludes .git, node_modules, _site,
.workbuddy and the local venv.
"""
import os, sys, json, base64, ssl, urllib.request, urllib.error, time

REPO = "cll2018/sharpen-export"
TOKEN = os.environ.get("GITHUB_PAT")
if not TOKEN:
    sys.exit("GITHUB_PAT env var required")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.github.com/repos/" + REPO

EXCLUDE_DIRS = {".git", "node_modules", "_site", ".workbuddy", "envs", "venv", "__pycache__"}
EXCLUDE_FILES = {".DS_Store", "Thumbs.db", "desktop.ini"}

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

def api(method, path, data=None, retries=4):
    url = API + path
    body = json.dumps(data).encode("utf-8") if data is not None else None
    last = None
    for attempt in range(1, retries + 1):
        req = urllib.request.Request(url, data=body, method=method)
        req.add_header("Authorization", "Bearer " + TOKEN)
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("User-Agent", "sharpen-deploy")
        if body:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, context=ssl_ctx, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
            last = e
            if attempt < retries:
                print("  [retry %d/%d] %s — back off 4s" % (attempt, retries, str(e)[:80]))
                time.sleep(4)
    print("HTTP", "failed after", retries, "tries:", str(last)[:200])
    raise last

def list_local_files():
    out = []
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in EXCLUDE_DIRS]
        for f in fn:
            if f in EXCLUDE_FILES:
                continue
            full = os.path.join(dp, f)
            rel = os.path.relpath(full, ROOT).replace(os.sep, "/")
            out.append(rel)
    return sorted(out)

def main():
    files = list_local_files()
    print("local files to deploy:", len(files))

    # 1) live HEAD
    ref = api("GET", "/git/ref/heads/main")
    head_sha = ref["object"]["sha"]
    print("live HEAD:", head_sha)

    # 2) live tree (recursive) -> existing paths
    tree = api("GET", "/git/trees/" + head_sha + "?recursive=1")
    base_tree_sha = tree["sha"]
    existing = {t["path"]: t["sha"] for t in tree.get("tree", []) if t["type"] == "blob"}
    print("live tree entries:", len(existing))

    # 3) create blobs for local files
    tree_entries = []
    changed = 0
    for rel in files:
        full = os.path.join(ROOT, rel)
        with open(full, "rb") as fh:
            raw = fh.read()
        b64 = base64.b64encode(raw).decode("ascii")
        blob = api("POST", "/git/blobs", {"content": b64, "encoding": "base64"})
        sha = blob["sha"]
        tree_entries.append({"path": rel, "mode": "100644", "type": "blob", "sha": sha})
        if existing.get(rel) != sha:
            changed += 1
    print("changed/added files:", changed)

    # 4) new tree (base_tree keeps untouched remote files)
    new_tree = api("POST", "/git/trees", {"base_tree": base_tree_sha, "tree": tree_entries})

    # 5) commit
    msg = sys.argv[1] if len(sys.argv) > 1 else "Migrate full content: 6 products, news, zh-tw, geo-adaptation"
    commit = api("POST", "/git/commits", {
        "message": msg, "tree": new_tree["sha"], "parents": [head_sha],
    })
    new_sha = commit["sha"]
    print("new commit:", new_sha)

    # 6) fast-forward update ref
    res = api("PATCH", "/git/refs/heads/main", {"sha": new_sha, "force": False})
    print("ref updated:", res.get("ref"), res.get("object", {}).get("sha"))
    print("DEPLOY OK — Cloudflare will rebuild automatically.")

if __name__ == "__main__":
    main()

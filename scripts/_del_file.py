# -*- coding: utf-8 -*-
"""Delete a file from the GitHub repo via the Git Database API (tree entry sha:null).
deploy.py only adds/updates, so deletions must be done explicitly this way."""
import os, json, ssl, urllib.request, urllib.error, time, sys

REPO = "cll2018/sharpen-export"
TOKEN = os.environ.get("GITHUB_PAT")
if not TOKEN:
    sys.exit("GITHUB_PAT required")
API = "https://api.github.com/repos/" + REPO
PATH = sys.argv[1] if len(sys.argv) > 1 else "zh/news/tinico-hot-bending-frontier-1.md"

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
        req.add_header("User-Agent", "sharpen-del")
        if body:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, context=ssl_ctx, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
            last = e
            if attempt < retries:
                print("retry", attempt, str(e)[:80]); time.sleep(4)
    print("failed:", str(last)[:200]); raise last

# 1) head
head = api("GET", "/git/ref/heads/main")["object"]["sha"]
print("HEAD:", head)
# 2) new tree deleting PATH (sha:null)
new_tree = api("POST", "/git/trees", {
    "base_tree": head,
    "tree": [{"path": PATH, "mode": "100644", "type": "blob", "sha": None}],
})
print("tree:", new_tree["sha"])
# 3) commit
msg = "Remove orphan/duplicate news page " + PATH
commit = api("POST", "/git/commits", {
    "message": msg, "tree": new_tree["sha"], "parents": [head],
})["sha"]
print("commit:", commit)
# 4) fast-forward
res = api("PATCH", "/git/refs/heads/main", {"sha": commit, "force": False})
print("ref:", res.get("ref"), res.get("object", {}).get("sha"))
print("DELETED OK — Cloudflare will rebuild.")

# -*- coding: utf-8 -*-
"""
Deploy a single changed file (fast-forward) to GitHub so we avoid the 124-blob
re-upload loop that intermittently hits SIGTERM on this machine.
Usage: python scripts/deploy_single.py <repo-relative-path> [commit-message]
Reads GITHUB_PAT env. base_tree keeps all remote files; only the target path's
blob is replaced.
"""
import os, sys, json, base64, ssl, time, urllib.request, urllib.error

REPO = "cll2018/sharpen-export"
TOKEN = os.environ.get("GITHUB_PAT")
if not TOKEN:
    sys.exit("GITHUB_PAT env var required")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.github.com/repos/" + REPO
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE

def api(method, path, data=None, retries=5):
    url = API + path
    body = json.dumps(data).encode() if data is not None else None
    last = None
    for a in range(1, retries + 1):
        req = urllib.request.Request(url, data=body, method=method)
        req.add_header("Authorization", "Bearer " + TOKEN)
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("User-Agent", "sharpen-deploy")
        if body:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=60) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            print("HTTP", e.code, e.reason, e.read().decode("utf-8","replace")[:300]); raise
        except Exception as e:
            last = e
            if a < retries:
                print("  [retry %d] %s" % (a, str(e)[:60])); time.sleep(4)
    raise last

def main():
    rel = sys.argv[1]
    msg = sys.argv[2] if len(sys.argv) > 2 else "Update " + rel
    full = os.path.join(ROOT, rel)
    raw = open(full, "rb").read()
    print("deploying single file:", rel, "(%d bytes)" % len(raw))

    ref = api("GET", "/git/ref/heads/main")
    head_sha = ref["object"]["sha"]
    print("live HEAD:", head_sha[:12])

    tree = api("GET", "/git/trees/" + head_sha + "?recursive=1")
    base_tree = tree["sha"]
    # fetch the full live tree entries and replace the target path
    entries = [{"path": t["path"], "mode": t["mode"], "type": t["type"], "sha": t["sha"]}
               for t in tree.get("tree", [])]
    newblob = api("POST", "/git/blobs", {"content": base64.b64encode(raw).decode(), "encoding": "base64"})
    # drop existing entry for this path (dir or blob) then append
    entries = [e for e in entries if e["path"] != rel]
    entries.append({"path": rel, "mode": "100644", "type": "blob", "sha": newblob["sha"]})
    entries.sort(key=lambda e: e["path"])
    new_tree = api("POST", "/git/trees", {"base_tree": base_tree, "tree": entries})
    commit = api("POST", "/git/commits", {"message": msg, "tree": new_tree["sha"], "parents": [head_sha]})
    new_sha = commit["sha"]
    api("PATCH", "/git/refs/heads/main", {"sha": new_sha, "force": False})
    print("new commit:", new_sha[:12])
    print("DEPLOY OK — Cloudflare will rebuild.")

if __name__ == "__main__":
    main()

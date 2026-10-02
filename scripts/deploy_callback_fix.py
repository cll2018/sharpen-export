#!/usr/bin/env python3
"""
Surgical GitHub push for ONE file, built on top of the CURRENT remote HEAD.

Why this script exists:
  The local git history is out of sync with the live site (later commits were
  pushed via the API and never pulled locally). A normal `git push` would be a
  non-fast-forward and could revert the live site. This script instead:
    1. reads the live remote HEAD + its full tree (recursive)
    2. uploads a new blob for the single local file we want to change
    3. rebuilds the tree with ONLY that one entry replaced
    4. creates a commit whose parent is the current HEAD (fast-forward safe)
    5. advances refs/heads/main
  Nothing else in the repo is touched, so there is zero risk of dropping files.

Usage:
  GH_TOKEN=ghp_xxx python scripts/deploy_callback_fix.py
"""
import base64
import json
import os
import sys
import urllib.request
import urllib.error

OWNER = "cll2018"
REPO = "sharpen-export"
TARGET_PATH = "functions/decap/auth/callback.js"
LOCAL_PATH = os.path.join(os.path.dirname(__file__), "..", TARGET_PATH)

API = f"https://api.github.com/repos/{OWNER}/{REPO}"


def api(method, path, token, data=None):
    url = API + path if path.startswith("/") else path
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "deploy-script")
    if data is not None:
        req.add_header("Content-Type", "application/json")
        req.data = json.dumps(data).encode("utf-8")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read().decode("utf-8")
            return r.status, (json.loads(body) if body else None)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        return e.code, body


def main():
    token = os.environ.get("GH_TOKEN")
    if not token:
        print("ERROR: set GH_TOKEN (a GitHub PAT with 'repo' scope) first.", file=sys.stderr)
        sys.exit(1)

    # 1) current HEAD
    status, head = api("GET", "/git/refs/heads/main", token)
    if status != 200:
        print("ERROR fetching HEAD:", status, head, file=sys.stderr)
        sys.exit(1)
    head_sha = head["object"]["sha"]
    print("Current HEAD:", head_sha)

    # 2) full tree (recursive)
    status, commit = api("GET", f"/git/commits/{head_sha}", token)
    if status != 200:
        print("ERROR fetching commit:", status, commit, file=sys.stderr)
        sys.exit(1)
    tree_sha = commit["tree"]["sha"]
    status, tree = api("GET", f"/git/trees/{tree_sha}?recursive=1", token)
    if status != 200:
        print("ERROR fetching tree:", status, tree, file=sys.stderr)
        sys.exit(1)
    entries = tree["tree"]
    print(f"Remote tree has {len(entries)} entries.")

    # 3) upload new blob for the target file
    with open(LOCAL_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    status, blob = api("POST", "/git/blobs", token,
                       {"content": content, "encoding": "utf-8"})
    if status != 201:
        print("ERROR creating blob:", status, blob, file=sys.stderr)
        sys.exit(1)
    new_blob_sha = blob["sha"]
    print("New blob:", new_blob_sha)

    # 4) rebuild tree, replacing only the target entry
    found = False
    new_entries = []
    for e in entries:
        if e["path"] == TARGET_PATH:
            new_entries.append({
                "path": e["path"],
                "mode": e["mode"],
                "type": "blob",
                "sha": new_blob_sha,
            })
            found = True
        else:
            new_entries.append({
                "path": e["path"],
                "mode": e["mode"],
                "type": e["type"],
                "sha": e["sha"],
            })
    if not found:
        # Target not present on remote — refuse to push a tree missing it.
        print(f"ERROR: {TARGET_PATH} not found in remote tree; aborting to avoid corruption.",
              file=sys.stderr)
        sys.exit(1)

    status, new_tree = api("POST", "/git/trees", token, {"tree": new_entries})
    if status != 201:
        print("ERROR creating tree:", status, new_tree, file=sys.stderr)
        sys.exit(1)
    new_tree_sha = new_tree["sha"]
    print("New tree:", new_tree_sha)

    # 5) commit on top of current HEAD (fast-forward safe)
    status, new_commit = api("POST", "/git/commits", token, {
        "message": "fix(decap): correct OAuth postMessage handshake (authorizing echo)",
        "tree": new_tree_sha,
        "parents": [head_sha],
    })
    if status != 201:
        print("ERROR creating commit:", status, new_commit, file=sys.stderr)
        sys.exit(1)
    new_commit_sha = new_commit["sha"]
    print("New commit:", new_commit_sha)

    # 6) advance main (fast-forward)
    status, ref = api("PATCH", "/git/refs/heads/main", token,
                      {"sha": new_commit_sha, "force": False})
    if status not in (200, 202):
        print("ERROR updating ref:", status, ref, file=sys.stderr)
        sys.exit(1)
    print("OK -> https://github.com/%s/%s/commit/%s" % (OWNER, REPO, new_commit_sha))
    print("Cloudflare Pages should rebuild automatically.")


if __name__ == "__main__":
    main()

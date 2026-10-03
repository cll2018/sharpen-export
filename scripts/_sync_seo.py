# -*- coding: utf-8 -*-
"""Sync _data/seo.js from GitHub main (preserves the user's robots.txt fix in
commit 01c1bb5 that a local-file deploy would otherwise revert)."""
import os, json, ssl, base64, urllib.request, difflib

TOKEN = os.environ.get("GITHUB_PAT")
REPO = "cll2018/sharpen-export"
LOCAL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_data", "seo.js")

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    "https://api.github.com/repos/%s/contents/_data/seo.js?ref=main" % REPO
)
req.add_header("Authorization", "Bearer " + TOKEN)
req.add_header("Accept", "application/vnd.github+json")
req.add_header("User-Agent", "sharpen-sync")
with urllib.request.urlopen(req, context=ssl_ctx, timeout=40) as r:
    data = json.loads(r.read().decode("utf-8"))

remote = base64.b64decode(data["content"]).decode("utf-8")
local = open(LOCAL, encoding="utf-8").read()

if remote == local:
    print("seo.js already identical to remote — nothing to do")
else:
    print("seo.js DIFFERS from remote — syncing remote -> local")
    diff = list(difflib.unified_diff(
        local.splitlines(), remote.splitlines(),
        fromfile="local", tofile="remote(main)", lineterm="", n=1))
    for line in diff[:60]:
        print("  " + line)
    with open(LOCAL, "w", encoding="utf-8") as f:
        f.write(remote)
    print("synced: wrote %d bytes (remote sha %s)" % (len(remote), data["sha"][:7]))

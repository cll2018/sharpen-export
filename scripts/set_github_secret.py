# -*- coding: utf-8 -*-
"""Create/update the GitHub Actions secret AI_LLM_API_KEY on the repo, so the
"i18n sync" workflow can reach the same LLM endpoint the Cloudflare Pages
project already uses.

The value is never hard-coded here — read it from the environment.

    GH_TOKEN=ghp_xxx LLM_KEY=wk-xxx python scripts/set_github_secret.py

(Uses the repo public key + libsodium sealed box, as the GitHub API requires.)
"""
import base64
import json
import os
import sys
import urllib.request

from nacl import encoding, public

REPO = os.environ.get("GH_REPO", "cll2018/sharpen-export")
SECRET_NAME = os.environ.get("SECRET_NAME", "AI_LLM_API_KEY")

TOKEN = os.environ.get("GH_TOKEN")
SECRET_VALUE = os.environ.get("LLM_KEY")

if not TOKEN or not SECRET_VALUE:
    sys.exit("set GH_TOKEN and LLM_KEY in the environment first")

API = "https://api.github.com"


def call(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(API + path, data=data, method=method)
    req.add_header("Authorization", "Bearer " + TOKEN)
    req.add_header("Accept", "application/vnd.github+json")
    if data:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read().decode()
    return json.loads(raw) if raw.strip() else None


key = call("GET", "/repos/%s/actions/secrets/public-key" % REPO)
print("repo public key id:", key.get("key_id"))

sealed = public.SealedBox(public.PublicKey(key["key"].encode(), encoding.Base64Encoder()))
encrypted = base64.b64encode(sealed.encrypt(SECRET_VALUE.encode())).decode()

call("PUT", "/repos/%s/actions/secrets/%s" % (REPO, SECRET_NAME),
     {"encrypted_value": encrypted, "key_id": key["key_id"]})
print("secret written:", SECRET_NAME)

listing = call("GET", "/repos/%s/actions/secrets" % REPO)
print("secrets on repo:", [s["name"] for s in listing.get("secrets", [])])

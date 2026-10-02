# -*- coding: utf-8 -*-
"""
Ping Google Search Console after each Cloudflare Pages deploy.

Two levels:
  1) No-GSC-key (always works, low priority): POST the sitemap to Google's
     public urll ping. It only asks Google to "look at this sitemap soon" —
     does NOT require a GSC-verified account or API key. Rate-limit: run at
     most once a day.
  2) With-GSC-key (recommended, in the GSC dashboard -> Settings -> API
     access, requires a GSC-verified property): use the Search Console API
     `urls:submitIndex` to request indexing of specific URLs. This gives the
     strongest signal. Set GSC_API_KEY env to enable.

Usage:
  python scripts/ping_gsc.py                # no-key urll ping
  GSC_API_KEY=xxx python scripts/ping_gsc.py # with-key URL-index submit
"""
import os, sys, ssl, json, urllib.request, urllib.parse

SITE = "https://www.sapu-cn.online"
SITEMAP = SITE + "/sitemap.xml"
API_KEY = os.environ.get("GSC_API_KEY", "")
API_PROP = "sc-domain:sapu-cn.online"  # prefix property format sc-domain:...

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def ping_nokey():
    """POST to Google's urll ping (no auth). Best-effort; returns 200 on success."""
    url = ("https://www.google.com/urll?"
           + urllib.parse.urlencode({"q": SITEMAP, "siteurl": SITE}))
    req = urllib.request.Request(url, headers={"User-Agent": "sharpen-sitemap-ping/1.0"})
    with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
        print("urll ping ->", r.status, r.read().decode("utf-8", "replace")[:200])
    return 0

def submit_index(key, urls):
    """Search Console API urls:submitIndex (GSC-verified property required)."""
    base = "https://www.googleapis.com/searchconsole/v1"
    body = json.dumps({"type": "INDEX", "ids": urls}).encode("utf-8")
    req = urllib.request.Request(
        base + "/" + urllib.parse.quote(API_PROP, safe="") + "/urls:submitIndex",
        data=body, method="POST",
        headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
            "X-Goog-Api-Key": key,
        })
    with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
        print("submitIndex ->", r.status, r.read().decode("utf-8", "replace")[:300])
    return 0

def main():
    if API_KEY:
        # submit a small batch of key URLs (homepage of each language + sitemap).
        keys = [
            SITE + "/",
            SITE + "/en/",
            SITE + "/zh/",
            SITE + "/products/steel-bonded-carbide/",
            SITE + "/en/news/",
        ]
        sys.exit(submit_index(API_KEY, keys))
    else:
        sys.exit(ping_nokey())

if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Full live-site health check (robust): sitemap enum + light BFS crawl.
Bytes-safe decoding, request delay + retry for transient Cloudflare throttling.
"""
import subprocess, re, time
from urllib.parse import urljoin, urlparse

BASE = "https://www.sapu-cn.online"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
DELAY = 0.18

def run_curl(args, timeout=25):
    cmd = ["curl", "-s", "-A", UA, "--max-time", str(timeout)] + args
    for attempt in range(3):
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=timeout+5)
            return r.returncode, r.stdout
        except Exception:
            time.sleep(1.0)
    return 1, b""

def status_of(url):
    rc, out = run_curl(["-o", "/dev/null", "-w", "%{http_code} %{redirect_url}", url])
    txt = out.decode("utf-8", "replace").strip()
    parts = txt.split(" ", 1)
    code = parts[0] if parts else "000"
    redir = parts[1] if len(parts) > 1 else ""
    time.sleep(DELAY)
    return code, redir

def html_of(url):
    rc, out = run_curl(["-L", url])
    time.sleep(DELAY)
    return out.decode("utf-8", "replace") if out else ""

def sitemap_urls():
    h = html_of(BASE + "/sitemap.xml")
    return [u.strip() for u in re.findall(r"<loc>([^<]+)</loc>", h) if u.strip()]

def main():
    print("=== 1) SITEMAP ENUMERATION (authoritative) ===")
    sm = sitemap_urls()
    print("sitemap URLs:", len(sm))
    by_code = {}
    f404 = []
    broken_redir = []
    for u in sm:
        code, redir = status_of(u)
        by_code[code] = by_code.get(code, 0) + 1
        if code == "404":
            f404.append(u)
        elif code.startswith("3"):
            if redir:
                tcode, _ = status_of(redir)
                if not tcode.startswith("2"):
                    broken_redir.append((u, code, redir, tcode))
            else:
                broken_redir.append((u, code, "(no redir)", ""))
    print("  status-code breakdown:", by_code)
    print("  404 URLs:", f404)
    print("  broken redirects (target not 2xx):", broken_redir)

    print("\n=== 2) LIGHT BFS CRAWL (catch URLs outside sitemap) ===")
    seeds = []
    for l in ["en","zh","zh-tw","de","ja","ko","ru","es","pt","fr","it","tr","ar","vi"]:
        seeds += [f"{BASE}/{l}/", f"{BASE}/{l}/products/", f"{BASE}/{l}/news/", f"{BASE}/{l}/about/", f"{BASE}/{l}/contact/", f"{BASE}/{l}/privacy/"]
    smset = set(u.rstrip("/") for u in sm)
    seen = set(s.rstrip("/") for s in seeds)
    q = list(seeds)
    checked = []
    MAX = 420
    while q and len(checked) < MAX:
        u = q.pop(0)
        code, redir = status_of(u)
        checked.append((u, code, redir))
        if code.startswith("2"):
            h = html_of(u)
            for m in re.findall(r'href=["\']([^"\']+)["\']', h or ""):
                absu = urljoin(u, m)
                p = urlparse(absu)
                if p.netloc != urlparse(BASE).netloc or p.query:
                    continue
                if any(absu.lower().endswith(x) for x in [".css",".js",".png",".jpg",".jpeg",".webp",".ico",".svg",".woff",".woff2",".xml",".json",".txt"]):
                    continue
                base = absu.split("#")[0].rstrip("/")
                if base not in seen:
                    seen.add(base); q.append(base)
    crawl_404 = [(u,c) for (u,c,r) in checked if c == "404"]
    crawl_broken = []
    for u,c,r in checked:
        if c.startswith("3") and r:
            tcode,_ = status_of(r)
            if not tcode.startswith("2"):
                crawl_broken.append((u,c,r,tcode))
    orphans = [u for (u,c,r) in checked if u.rstrip("/") not in smset and c.startswith("2")]
    print("  crawled:", len(checked))
    print("  crawl 404s:", crawl_404)
    print("  crawl broken redirects:", crawl_broken)
    print("  orphan 200 URLs not in sitemap (sample):", orphans[:25], "total:", len(orphans))

    print("\n=== FINAL ===")
    print("TOTAL sitemap 404s:", len(f404), f404)
    print("TOTAL sitemap broken redirects:", len(broken_redir))

if __name__ == "__main__":
    main()

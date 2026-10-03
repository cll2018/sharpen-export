# -*- coding: utf-8 -*-
"""Sitemap-only authoritative full-site check (fast). Enumerate every <loc> in
sitemap.xml and request each; report 404s, broken redirects, and code breakdown."""
import subprocess, re, time
from urllib.parse import urlparse

BASE = "https://www.sapu-cn.online"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
DELAY = 0.15

def status_of(url):
    cmd = ["curl","-s","-A",UA,"--max-time","25","-o","/dev/null","-w","%{http_code} %{redirect_url}",url]
    for _ in range(3):
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=32)
            txt = r.stdout.decode("utf-8","replace").strip()
            parts = txt.split(" ",1)
            code = parts[0] if parts else "000"
            redir = parts[1] if len(parts)>1 else ""
            time.sleep(DELAY)
            return code, redir
        except Exception:
            time.sleep(1.0)
    return "ERR", ""

def main():
    r = subprocess.run(["curl","-s","-A",UA,"--max-time","30",BASE+"/sitemap.xml"],
                       capture_output=True, timeout=35)
    sm = [u.strip() for u in re.findall(r"<loc>([^<]+)</loc>", r.stdout.decode("utf-8","replace")) if u.strip()]
    print("sitemap URLs:", len(sm))
    by_code = {}
    f404=[]; broken=[]; transient=[]
    for u in sm:
        code, redir = status_of(u)
        by_code[code] = by_code.get(code,0)+1
        if code=="404":
            f404.append(u)
        elif code in ("000","ERR","403","429","503","520","522","524"):
            transient.append((u,code))
        elif code.startswith("3"):
            if redir:
                tc,_ = status_of(redir)
                if not tc.startswith("2"):
                    broken.append((u,code,redir,tc))
            else:
                broken.append((u,code,"(none)",""))
    print("status breakdown:", by_code)
    print("\nREAL 404s (count=%d):"%len(f404))
    for u in f404: print("  ", u)
    print("\nBROKEN REDIRECTS (count=%d):"%len(broken))
    for x in broken: print("  ", x)
    print("\nTRANSIENT/THROTTLE (count=%d):"%len(transient))
    for x in transient[:40]: print("  ", x)
    print("\nSUMMARY: 404=%d  broken_redir=%d  transient=%d"%(len(f404),len(broken),len(transient)))

if __name__=="__main__":
    main()

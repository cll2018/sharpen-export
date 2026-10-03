# -*- coding: utf-8 -*-
"""Enhanced sitemap check: follow redirects, longer timeout, retry empties.
Reports definitive 404s and any still-unresolved (timeout) URLs."""
import subprocess, re, time

BASE = "https://www.sapu-cn.online"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"

def code_of(url, maxt=30):
    cmd = ["curl","-s","-L","-A",UA,"--max-time",str(maxt),"-o","/dev/null","-w","%{http_code}",url]
    for _ in range(3):
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=maxt+8)
            c = r.stdout.decode("utf-8","replace").strip()
            if c:
                return c
        except Exception:
            pass
        time.sleep(1.0)
    return ""

def main():
    r = subprocess.run(["curl","-s","-A",UA,"--max-time","30",BASE+"/sitemap.xml"],
                       capture_output=True, timeout=35)
    sm = [u.strip() for u in re.findall(r"<loc>([^<]+)</loc>", r.stdout.decode("utf-8","replace")) if u.strip()]
    print("sitemap URLs:", len(sm))
    by_code = {}
    f404=[]; other=[]; empty=[]
    for u in sm:
        c = code_of(u)
        time.sleep(0.08)
        if not c:
            empty.append(u); continue
        by_code[c] = by_code.get(c,0)+1
        if c=="404": f404.append(u)
        elif not c.startswith("2"): other.append((u,c))
    print("status breakdown:", by_code)
    print("REAL 404s (%d):"%len(f404))
    for u in f404: print("  ",u)
    print("OTHER non-200 (%d):"%len(other))
    for u,c in other: print("  ",c,u)
    print("STILL EMPTY/timeout (%d):"%len(empty))
    for u in empty: print("  ",u)
    print("SUMMARY 404=%d other=%d empty=%d"%(len(f404),len(other),len(empty)))

if __name__=="__main__":
    main()

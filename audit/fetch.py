#!/usr/bin/env python3
"""Fetch a source page as plain text. Direct GET first; the Internet Archive copy when the site blocks us.

    python3 audit/fetch.py <url> <out.txt>
    python3 audit/fetch.py --all audit/sources/sources.json audit/runs/sources/

Writes the text and prints the route that worked and the word count."""
import html, json, re, sys, urllib.request, urllib.error, pathlib

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"

def get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")

def to_text(page):
    body = re.search(r"<article.*?</article>", page, re.S)
    body = body.group(0) if body else (re.search(r"<main.*?</main>", page, re.S) or re.search(r"<body.*?</body>", page, re.S) or re.match(r".*", page, re.S)).group(0)
    body = re.sub(r"<(script|style|nav|header|footer|aside)[^>]*>.*?</\1>", "", body, flags=re.S)
    body = re.sub(r"<(h[1-6]|p|li|pre|blockquote|figcaption|tr|div)[^>]*>", "\n\n", body)
    body = re.sub(r"<br\s*/?>", "\n", body)
    text = html.unescape(re.sub(r"<[^>]+>", "", body))
    return re.sub(r"\n{3,}", "\n\n", text).strip()

def blocked(page):
    return "Attention Required! | Cloudflare" in page or "Sorry, you have been blocked" in page or len(page) < 2000

def get_retry(url, tries=4):
    import time
    for i in range(tries):
        try: return get(url)
        except urllib.error.HTTPError as e:
            if e.code != 429 or i == tries - 1: raise
            time.sleep(15 * (i + 1))

def fetch(url, archive_ts=None):
    if not archive_ts:
        try:
            page = get(url)
            if not blocked(page):
                return page, "direct"
        except urllib.error.HTTPError as e:
            if e.code not in (403, 429, 503): raise
        avail = json.loads(get_retry(f"https://archive.org/wayback/available?url={url}"))
        snap = avail.get("archived_snapshots", {}).get("closest")
        if not snap: raise SystemExit(f"blocked and no archive copy: {url}")
        archive_ts = snap["timestamp"]
    return get_retry(f"https://web.archive.org/web/{archive_ts}id_/{url}"), f"archive.org {archive_ts}"

def one(url, out, archive_ts=None):
    page, route = fetch(url, archive_ts)
    text = to_text(page)
    pathlib.Path(out).write_text(text)
    print(f"{route:>24}  {len(text.split()):>6} words  {out}")

if __name__ == "__main__":
    if sys.argv[1] == "--all":
        srcs = json.load(open(sys.argv[2])); outdir = pathlib.Path(sys.argv[3]); outdir.mkdir(parents=True, exist_ok=True)
        for s in srcs:
            if s.get("skip"): print(f"{'skipped':>24}  {s['id']}: {s.get('note','')[:70]}"); continue
            try: one(s["url"], outdir / (s["id"] + ".txt"), s.get("archive"))
            except Exception as e: print(f"{'FAILED':>24}  {s['id']}: {e}")
    else:
        one(sys.argv[1], sys.argv[2])

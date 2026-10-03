#!/usr/bin/env python3
"""
Download the fragrance images that collection.html hotlinks from
lh3.googleusercontent.com into img/ as scent-<slug>.webp, then rewrite the
HTML to point at the local files.

Hotlinking a third-party CDN is fragile (the URL can 404 or be rate-limited,
which breaks both the page and the schema image URL). Self-hosting also lets
Nginx serve them with a 30-day immutable cache.

Usage: python3 deploy/localize-images.py [--check]
Idempotent.
"""
import hashlib
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "collection.html"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"


def rows(html: str):
    """Yield (slug, scent_name, hotlink_url) for each scent-row block."""
    for block in re.split(r"<!--\s*Scent\s*\d+:", html)[1:]:
        h2 = re.search(r"<h2[^>]*>(.*?)</h2>", block, re.S)
        img = re.search(r'data-image-url="([^"]+)"', block)
        if not (h2 and img):
            continue
        name = re.sub(r"<[^>]+>", "", h2.group(1)).strip()
        clean = re.sub(r"\s*\([^)]*\)\s*$", "", name).strip()
        slug = re.sub(r"[^a-z0-9]+", "-", clean.lower()).strip("-")
        yield slug, clean, img.group(1)


def fetch(url: str, dest: Path) -> bool:
    with tempfile.TemporaryDirectory() as td:
        raw = Path(td) / "raw.bin"
        # add a size suffix so Google returns the large rendition, not a thumbnail
        sized = url + "=w1200-h1200" if "=" not in url.rsplit("/", 1)[-1] else url
        r = subprocess.run(
            ["curl", "-sSL", "--max-time", "45", "-A", UA, "-o", str(raw), sized],
            capture_output=True,
        )
        if r.returncode != 0 or not raw.exists() or raw.stat().st_size < 1024:
            return False
        r2 = subprocess.run(
            ["magick", str(raw), "-strip", "-resize", "1200x1200>",
             "-quality", "82", str(dest)],
            capture_output=True,
        )
        return r2.returncode == 0 and dest.exists() and dest.stat().st_size > 1024


def main() -> int:
    check_only = "--check" in sys.argv
    html = TARGET.read_text(encoding="utf-8")
    uniq = {}
    for slug, name, url in rows(html):
        uniq.setdefault(slug, url)

    print(f"hotlinked scent images: {len(uniq)} unique")

    # Any remaining lh3.googleusercontent.com refs live outside the scent-row
    # blocks (room-freshener tiles). Catch those too, keyed by a hash of the URL.
    leftovers = set(re.findall(r"https://lh3\.googleusercontent\.com[^\"\s)]+", html))
    covered = set(uniq.values())
    for url in sorted(leftovers - covered):
        slug = "tile-" + hashlib.sha1(url.encode()).hexdigest()[:10]
        uniq.setdefault(slug, url)

    changed = False
    for slug, url in uniq.items():
        dest = ROOT / f"img/scent-{slug}.webp"
        if dest.exists():
            print(f"  scent-{slug}.webp  already local ({dest.stat().st_size // 1024}KB)")
        else:
            if check_only:
                print(f"  scent-{slug}.webp  WOULD DOWNLOAD")
                continue
            if fetch(url, dest):
                print(f"  scent-{slug}.webp  downloaded ({dest.stat().st_size // 1024}KB)")
            else:
                print(f"  scent-{slug}.webp  FAILED - leaving hotlink in place")
                continue

        # rewrite the two places the URL appears (data-image-url + fallback img src)
        new_html = html.replace(url, f"img/scent-{slug}.webp")
        if new_html != html:
            changed = True
            html = new_html

    if check_only:
        return 0
    if changed:
        TARGET.write_text(html, encoding="utf-8")
        print("collection.html rewritten to local paths")
    else:
        print("no HTML rewrite needed")
    left = len(re.findall(r"lh3\.googleusercontent\.com", html))
    print(f"remaining googleusercontent references: {left}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
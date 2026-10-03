#!/usr/bin/env python3
"""
Improve catalogue image alt text for SEO (Google Images).

Anchoring rule: each product card is located by its model badge
(<span ...>ISX-...</span>) and its image is rewritten within that card only.
The badge is the authoritative display model, which matters because the image
FILENAME does not always match it (ISXPR-OV-55.webp displays as ISXPR-OV-5/5).

Only cards inside the product/collection sections are touched, so the logo,
marketplace badges, certification logos and index.html feature cards are never
rewritten.

Alt wording is derived from data already present in the card (model + the
product-type words in the old alt), so nothing is invented.

Usage: python3 deploy/fix-alt-text.py [--check]
Idempotent.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Truthful use cases, keyed by the product-type words already in the old alt.
USE = {
    "car": "mobil",
    "car aroma": "mobil",
    "battery": "mobil",
    "smart plugin": "kamar tidur dan hotel",
    "electric": "hotel dan kantor",
    "smart home": "smart home",
    "commercial": "hotel, kantor, dan retail",
}
DEFAULT_USE = "hotel, kantor, dan retail"

FRAGRANCE_SUFFIX = "wewangian premium untuk hotel, butik, dan kantor"
REED_ALT = (
    "Reed diffuser stik bambu Indoeasy Scent — pengharum ruangan tanpa "
    "listrik untuk hunian dan kantor"
)
INDONESIAN = {
    "car": "Mobil", "car aroma": "Mobil", "battery": "Baterai",
    "electric": "Listrik", "commercial": "Komercial",
    "smart plugin": "Smart Plugin", "smart home": "Smart Home",
}


def type_words(old: str) -> str:
    """Strip the model prefix and generic nouns; keep the type descriptor."""
    k = re.sub(r"^ISX[A-Z0-9\-/]*", " ", old.strip())
    k = re.sub(r"\b(diffuser|aroma|scent)\b", " ", k, flags=re.I)
    return re.sub(r"\s+", " ", k).strip(" -")


def diffuser_alt(model: str, old: str) -> str:
    key = type_words(old)
    kind = INDONESIAN.get(key.lower(), key.title())
    use = USE.get(key.lower(), DEFAULT_USE)
    if not kind:
        return f"{model} — diffuser scent Indoeasy Scent untuk {use}"
    return f"{model} — diffuser scent {kind} Indoeasy Scent untuk {use}"


# An alt we already generated is recognisable and must be skipped, so the
# script stays idempotent instead of re-processing its own output.
DONE_MARK = "Indoeasy Scent untuk"


def process_products(html: str, report: list) -> str:
    """Rewrite diffuser/reed alts inside the model-badge cards."""
    spans = []
    for bm in re.finditer(r'shadow-md">(ISX[A-Z0-9\-/]+)</span>', html):
        model = bm.group(1)
        nxt = html.find('shadow-md">ISX', bm.end())
        end = nxt if nxt != -1 else len(html)
        card = html[bm.start():end]
        im = re.search(
            r'(?P<pre><img[^>]*?src="img/(?P<src>[^"]+)"[^>]*?alt=")'
            r'(?P<alt>[^"]*)(?P<post>")', card,
        )
        if not im:
            continue
        src, old = im.group("src"), im.group("alt")
        if DONE_MARK in old:
            continue                      # already rewritten
        if src.lower().startswith("isx"):
            new = diffuser_alt(model, old)
        elif src == "reed-diffuser.png":
            new = REED_ALT
        else:
            new = None
        if new and new != old:
            card2 = (card[: im.start()] + im.group("pre") + new
                     + im.group("post") + card[im.end():])
            spans.append((bm.start(), end, card2, old, new))

    if not spans:
        return html
    res, last = [], 0
    for start, end, card2, old, new in spans:
        res.append(html[last:start])
        res.append(card2)
        last = end
        report.append((old, new))
    res.append(html[last:])
    return "".join(res)


def process_fragrances(html: str, report: list) -> str:
    """Fragrance cards: h4 name -> image. Use the h4, not the filename."""
    def sub(m):
        label = m.group("name").strip()
        if DONE_MARK in m.group("alt") or "Fragrance" in m.group("alt"):
            return m.group(0)             # already rewritten
        new = f"Fragrance {label.title()} Indoeasy Scent — {FRAGRANCE_SUFFIX}"
        if new != m.group("alt"):
            report.append((m.group("alt"), new))
        return m.group("pre") + new + m.group("post")

    return re.sub(
        r'(?P<pre><h4[^>]*>\s*(?P<name>[A-Z][A-Z0-9 &/\'-]{2,40}?)\s*</h4>'
        r'(?:(?!<h4).){0,1400}?<img[^>]*?src="img/[a-z0-9-]+\.webp"'
        r'[^>]*?alt=")(?P<alt>[^"]*)(?P<post>")',
        sub, html, flags=re.S,
    )


def main():
    check_only = "--check" in sys.argv
    f = ROOT / "products.html"
    html = f.read_text(encoding="utf-8")
    orig = html
    report: list = []
    html = process_products(html, report)
    html = process_fragrances(html, report)

    if html != orig:
        if not check_only:
            f.write_text(html, encoding="utf-8")
        print(f"products.html: {len(report)} alt texts rewritten")
        for before, after in report:
            print(f"    {before!r}\n      -> {after!r}")
    else:
        print("products.html: no alt changes needed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
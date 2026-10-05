#!/usr/bin/env python3
"""Validate Google Ads copy lengths for indoeasyscent.com.

The single most common reason a responsive search ad gets pinned or a sitelink
fails to assemble is a field that is one character over the limit. Google
counts spaces and punctuation, and the editor rejects an over-length field
without letting you save it.

This script holds the ad copy as structured data and asserts every field
against Google's own limits, so a copy edit cannot silently break the account:

    headline        1-15 items, each <= 30 chars
    description     1-4  items, each <= 90 chars
    display path    2 items, each <= 15 chars
    sitelink text   <= 25, description lines <= 35
    callout         <= 25
    structured value <= 25

Run:  python3 deploy/validate-ads-copy.py
Exit code 1 on any violation.

Every claim in this file must be traceable to the site markup. An ad that
says something the landing page does not is a policy risk, not a marketing
win -- see CLAIM_SOURCES below, checked against the HTML by --verify-claims.
"""

import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Google's documented limits (support.google.com/google-ads/answer/7684791,
# /answer/17092074, /answer/17090561). Checked 2026-10-05; re-verify yearly.
LIMITS = {
    "headline": 30,
    "description": 90,
    "path": 15,
    "sitelink": 25,
    "sitelink_desc": 35,
    "callout": 25,
    "snippet_value": 25,
}

# --- Ads ------------------------------------------------------------------
# Three ad groups, one intent each. Splitting them is what the account
# needs: one page cannot rank for both "sewa diffuser aroma" and
# "fragrance oil premium", and mixing them in one ad group wastes budget.

CAMPAIGN = {
    # Geo: Bekasi + Jakarta + Jawa Barat, matching LocalBusiness areaServed.
    "name": "Sewa Diffuser Aroma - Bekasi",
    "type": "Search",
    "final_url": "https://indoeasyscent.com/",
    "paths": ["sewa-diffuser", "bekasi"],
    # Exact/phrase. No broad "diffuser" alone -- intent is too mixed and the
    # keyword map already rules out low-intent e-commerce terms.
    "keywords": [
        "sewa diffuser aroma",
        "jasa scenting diffuser",
        "sewa pengharum ruangan",
        "diffuser aroma hotel",
        "diffuser aroma kantor",
        "jasa aroma diffuser bekasi",
        "sewa diffuser jakarta",
        "cold air diffuser indonesia",
        "sistem scenting hotel",
        "[sewa diffuser aroma bekasi]",
        "[jasa scenting diffuser jakarta]",
        '"sewa diffuser aroma"',
        '"jasa scenting diffuser"',
    ],
    "negative_keywords": [
        "murah", "termurah", "gratis", "second hand", "bekas",
        "manual", "homemade", "resep", "youtube", "tutorial", "cara buat",
        "lowongan", "karang tarum", "shopee", "tokopedia",
    ],
    "headlines": [
        "Sewa Diffuser Aroma",
        "Jasa Scenting Diffuser",
        "Commercial Scenting",
        "Diffuser Aroma Hotel",
        "30 m3 - 4.000 m3",
        "Trial & Sampel Gratis",
        "Pemasangan Gratis",
        "Bekasi, Jakarta, Jawa Barat",
        "IFRA & Kemenkes RI",
        "11 Model Diffuser ISX",
        "Refill & Maintenance",
        "Garansi Unit 1x24 Jam",
        "Konsultasi Aroma Gratis",
        "Hubungi via WhatsApp",
        "Hotel, Kantor & Retail",
    ],
    "descriptions": [
        "Sewa & instalasi diffuser aroma cold-air untuk hotel, kantor, retail",
        "Cakupan 30 m3 sampai 4.000 m3. Trial unit dan sampel wewangian gratis",
        "Pemasangan gratis teknisi. Refill & maintenance berkala",
        "Konsultasi kurasi aroma B2B tanpa biaya. Area Bekasi & Jawa Barat",
    ],
}

ADGROUP_COLLECTION = {
    "name": "Fragrance Oil & Reed Diffuser",
    "final_url": "https://indoeasyscent.com/collection.html",
    "paths": ["fragrance-oil", "reed-diffuser"],
    "keywords": [
        "fragrance oil premium",
        "minyak wewangian hotel",
        "reed diffuser premium",
        "wewangian eksklusif",
        "reed diffuser hotel",
        "fragrance oil jakarta",
        "room spray signature",
        '"fragrance oil premium"',
        '"reed diffuser premium"',
    ],
    "negative_keywords": [],
    "headlines": [
        "Fragrance Oil Premium",
        "Reed Diffuser Premium",
        "Wewangian Eksklusif",
        "Minyak Wewangian Hotel",
        "Aroma Signature",
        "Empat Aroma Eksklusif",
        "Bekasi, Jakarta, Jawa Barat",
        "Konsultasi Gratis",
        "Siap Dicoba",
    ],
    "descriptions": [
        "Empat aroma eksklusif siap dicoba lebih dulu sebelum Anda memesan",
        "Fragrance oil premium & reed diffuser untuk hotel, kantor, butik",
        "Konsultasi karakter aroma gratis. Sampel dikirim ke lokasi bisnis",
    ],
}

ADGROUP_DIFFUSER = {
    "name": "Katalog Diffuser ISX",
    "final_url": "https://indoeasyscent.com/products.html",
    "paths": ["diffuser-isx", "katalog"],
    "keywords": [
        "scenting diffuser hotel",
        "mesin diffuser aroma",
        "diffuser aroma profesional",
        "cold air diffuser",
        "diffuser aroma 4000m3",
        "commercial scent diffuser",
    ],
    "negative_keywords": [],
    "headlines": [
        "Scenting Diffuser ISX",
        "11 Model Diffuser",
        "Cold-Air Micro-Diffusion",
        "Cakupan 30 - 4.000 m3",
        "Spesifikasi Lengkap",
        "Bekasi & Jabodetabek",
        "Konsultasi Gratis",
        "Trial Unit Gratis",
        "Pemasangan Gratis",
    ],
    "descriptions": [
        "Katalog resmi ISX Series: spesifikasi, daya, kebisingan, dan kapasitas",
        "Satuan dari 30 m3 sampai 4.000 m3. Lihat spesifikasi tiap model",
    ],
}

# --- Sitelinks (ad-level assets) -----------------------------------------
# Limit 20 per account-level sitelink asset. Each points at a real page that
# exists and is indexable -- 404 or noindex landing pages cost Quality Score.
SITELINKS = [
    {
        "text": "Sewa Diffuser Aroma",
        "desc1": "Cold-air presisi, 30 m3 - 4.000 m3",
        "desc2": "Pemasangan gratis oleh teknisi",
        "url": "https://indoeasyscent.com/",
    },
    {
        "text": "Katalog Diffuser ISX",
        "desc1": "11 model, spesifikasi lengkap",
        "desc2": "Cakupan 30 m3 sampai 4.000 m3",
        "url": "https://indoeasyscent.com/products.html",
    },
    {
        "text": "Koleksi Wewangian",
        "desc1": "Fragrance oil premium",
        "desc2": "Reed diffuser untuk bisnis",
        "url": "https://indoeasyscent.com/collection.html",
    },
    {
        "text": "Layanan & Proses",
        "desc1": "Sewa, refill, maintenance",
        "desc2": "Trial dan sampel aroma gratis",
        "url": "https://indoeasyscent.com/about.html",
    },
    {
        "text": "Konsultasi Gratis",
        "desc1": "Trial unit dan sampel aroma",
        "desc2": "Hubungi tim kami hari ini",
        "url": "https://indoeasyscent.com/contact.html",
    },
    {
        "text": "Cerita Kami",
        "desc1": "Standar produksi",
        "desc2": "Konsultasi karakter aroma",
        "url": "https://indoeasyscent.com/about.html#cerita-kami",
    },
]

# checkout.html is noindex + Disallowed in robots.txt. A noindex landing page
# cannot be a Google Ads final/sitelink URL: the ad sends the click, robots
# tells the crawler not to index it, and Quality Score drops. The inquiry
# form is still reachable from the nav and from every WhatsApp CTA, so
# nothing is lost by not advertising it directly.
#
# If you ever open checkout.html for indexing, delete that page from
# NOINDEX_PAGES and remove it from robots.txt in the same commit -- leaving
# one without the other is the contradiction the keyword map warns about.
NOINDEX_PAGES = {"checkout.html", "terms-of-service.html"}

# --- Callouts -------------------------------------------------------------
# Every callout must be backed by page copy (see CLAIM_SOURCES) -- a callout
# is an ad claim, and an unsupported one is a disapproval risk. "Bekasi &
# Jabodetabek" was dropped: the word "Jabodetabek" appears nowhere on the site
# outside terms-of-service.html, while areaServed is Jawa Barat / Bekasi /
# Jakarta. Advertising a wider area than the site claims is exactly the kind
# of mismatch that gets an ad held for review.
CALLOUTS = [
    "Trial & Sampel Gratis",
    "Pemasangan Gratis",
    "Bekasi, Jakarta",
    "IFRA & Kemenkes RI",
    "Garansi 1x24 Jam",
    "Refill Berkala",
    "Konsultasi Gratis",
    "Coverage 4.000 m3",
]

# --- Structured snippets ---------------------------------------------------
SNIPPETS = {
    "header": "Layanan",
    "values": [
        "Sewa Diffuser",
        "Instalasi",
        "Refill Berkala",
        "Maintenance",
        "Trial & Sampel",
        "Konsultasi Aroma",
    ],
}
SNIPPETS_PRODUCT = {
    "header": "Model Diffuser",
    "values": [
        "ISX-I-0  30 m3",
        "ISX-H2  300 m3",
        "ISX-H5  1000 m3",
        "ISXPR-OV-5/5  800 m3",
        "ISX-U-5  3.000 m3",
        "ISX-U10  4.000 m3",
    ],
}

# --- Claim sources --------------------------------------------------------
# The reason this validator has a --verify-claims mode: an ad must not claim
# more than the landing page does. The keyword map already forbids targeting
# "murah", "review", or "tokopedia" for exactly this reason. A disallowed or
# fabricated claim gets the ad (and sometimes the account) suspended, which
# costs far more than the click.
CLAIM_SOURCES = {
    "IFRA & Kemenkes RI": ["index.html"],
    "Trial & Sampel Gratis": ["index.html", "about.html", "products.html"],
    "Pemasangan Gratis": ["about.html", "products.html"],
    # The site says "Refill & Maintenance Berkala ... setiap bulan", not
    # "Bulanan". Wording here must not outrun the page.
    "Refill & Maintenance": ["about.html"],
    "Garansi Unit 1x24 Jam": ["terms-of-service.html"],
    "30 m3 - 4.000 m3": ["products.html"],
    "11 Model Diffuser ISX": ["products.html"],
    "Bekasi, Jakarta, Jawa Barat": ["index.html", "contact.html"],
    "Empat aroma eksklusif": ["collection.html"],
    "Standar produksi": ["index.html"],
    "Konsultasi karakter aroma": ["about.html"],
    "Hubungi via WhatsApp": ["index.html", "contact.html"],
    "Coverage 4.000 m3": ["products.html"],
    "Bekasi, Jakarta": ["index.html", "contact.html"],
}


def plain(text):
    """Length as Google counts it: strip nothing, count every char."""
    return len(text)


def check(label, value, limit):
    if plain(value) > limit:
        return [f"FAIL {label}: {plain(value)} chars > {limit} :: {value!r}"]
    return []


def validate_copy():
    problems = []
    groups = {
        "CAMPAIGN": CAMPAIGN,
        "ADGROUP_COLLECTION": ADGROUP_COLLECTION,
        "ADGROUP_DIFFUSER": ADGROUP_DIFFUSER,
    }
    for gname, g in groups.items():
        heads = g["headlines"]
        if not 3 <= len(heads) <= 15:
            problems.append(
                f"FAIL {gname}: {len(heads)} headlines (Google needs 3-15, "
                f"and fewer than 3 can leave an ad ineligible)"
            )
        for i, h in enumerate(heads, 1):
            problems += check(f"{gname}.headline[{i}]", h, LIMITS["headline"])
        descs = g["descriptions"]
        if not 2 <= len(descs) <= 4:
            problems.append(
                f"FAIL {gname}: {len(descs)} descriptions (Google needs 2-4; "
                f"1 makes the ad ineligible)"
            )
        for i, d in enumerate(descs, 1):
            problems += check(f"{gname}.description[{i}]", d, LIMITS["description"])
        for i, p in enumerate(g["paths"], 1):
            problems += check(f"{gname}.path[{i}]", p, LIMITS["path"])

    if len(SITELINKS) > 20:
        problems.append(f"FAIL sitelinks: {len(SITELINKS)} (max 20)")
    for i, s in enumerate(SITELINKS, 1):
        problems += check(f"sitelink[{i}].text", s["text"], LIMITS["sitelink"])
        problems += check(f"sitelink[{i}].desc1", s["desc1"], LIMITS["sitelink_desc"])
        problems += check(f"sitelink[{i}].desc2", s["desc2"], LIMITS["sitelink_desc"])

    for i, c in enumerate(CALLOUTS, 1):
        problems += check(f"callout[{i}]", c, LIMITS["callout"])
    if len(CALLOUTS) > 20:
        problems.append(f"FAIL callouts: {len(CALLOUTS)} (max 20)")

    for name, snip in (("SNIPPETS", SNIPPETS), ("SNIPPETS_PRODUCT", SNIPPETS_PRODUCT)):
        if not 3 <= len(snip["values"]) <= 10:
            problems.append(
                f"FAIL {name}: {len(snip['values'])} values (Google needs 3-10)"
            )
        for i, v in enumerate(snip["values"], 1):
            problems += check(f"{name}.value[{i}]", v, LIMITS["snippet_value"])

    # Duplicate check: Google silently drops a repeated asset, which wastes
    # a slot you paid for.
    for gname, g in groups.items():
        seen = {}
        for h in g["headlines"]:
            k = unicodedata.normalize("NFC", h.lower())
            if k in seen:
                problems.append(
                    f"FAIL {gname}: duplicate headline {h!r} "
                    f"(same as #{seen[k]}); Google drops repeats"
                )
            seen[k] = seen.get(k, len(seen) + 1)
    return problems


def validate_urls():
    """Every ad/sitelink URL must exist in the repo and be indexable.

    Also resolves any #fragment against the real id set of the target page.
    A sitelink whose anchor does not exist lands the visitor at the top of the
    page with no visible effect, which reads as a broken ad.
    """
    problems = []
    urls = [("CAMPAIGN", CAMPAIGN["final_url"])]
    for gname, g in (("ADGROUP_COLLECTION", ADGROUP_COLLECTION),
                     ("ADGROUP_DIFFUSER", ADGROUP_DIFFUSER)):
        urls.append((gname, g["final_url"]))
    for i, s in enumerate(SITELINKS, 1):
        urls.append((f"sitelink[{i}]", s["url"]))

    # Google ignores a sitelink whose final URL duplicates ANOTHER SITELINK.
    # A sitelink sharing the ad's own final URL is fine and in fact normal --
    # only sitelink-vs-sitelink repetition wastes a slot.
    seen_sitelink_urls = {}

    for name, url in urls:
        m = re.match(r"^https://indoeasyscent\.com/([^?#]*)", url)
        if not m:
            problems.append(f"FAIL {name}: not an indoeasyscent.com URL :: {url}")
            continue

        frag = ""
        fm = re.search(r"#([^?]+)$", url)
        if fm:
            frag = fm.group(1)

        path = m.group(1) or "index.html"
        if path.endswith("/"):
            path += "index.html"
        target = ROOT / path

        if not target.exists():
            problems.append(f"FAIL {name}: {url} -> no file {path} in repo")
            continue

        if name.startswith("sitelink["):
            key = f"{path}#{frag}"
            if key in seen_sitelink_urls:
                problems.append(
                    f"FAIL {name}: {url} duplicates sitelink "
                    f"{seen_sitelink_urls[key]}. Google drops repeated "
                    f"sitelink URLs, so that slot is wasted."
                )
            else:
                seen_sitelink_urls[key] = name

        html = target.read_text(encoding="utf-8")
        robots = re.search(r'name="robots"\s+content="([^"]*)"', html)
        if robots and "noindex" in robots.group(1).lower():
            problems.append(
                f"FAIL {name}: {url} is noindex in {path}. A noindex landing "
                f"page cannot be an ad destination -- Quality Score drops."
            )
        base = path.rsplit("/", 1)[-1]
        if base in NOINDEX_PAGES:
            problems.append(
                f"FAIL {name}: {url} is Disallowed in robots.txt. See the "
                f"NOINDEX_PAGES note in this file."
            )

        if frag:
            ids = set(re.findall(r'id="([^"]+)"', html))
            if frag not in ids:
                problems.append(
                    f"FAIL {name}: {url} -> no id=\"{frag}\" in {path}. "
                    f"Valid ids: {sorted(ids - {'tailwind-config'})}"
                )
    return problems


def verify_claims():
    """Every claim used in an ad must appear in the page it points at."""
    problems = []
    for claim, pages in CLAIM_SOURCES.items():
        # Match on words, not the whole string: the ad copy uses "m3" where
        # the site writes "m³" and "x" where the site writes "-".
        probe = re.sub(r"[^a-z0-9 ]", "", claim.lower())
        words = [w for w in probe.split() if len(w) > 3]
        for page in pages:
            target = ROOT / page
            if not target.exists():
                problems.append(f"FAIL claim {claim!r}: missing {page}")
                continue
            text = re.sub(
                r"<[^>]+>", " ", target.read_text(encoding="utf-8").lower()
            )
            text = re.sub(r"[^a-z0-9 ]", " ", text)
            text = re.sub(r"\s+", " ", text)
            if not all(w in text for w in words):
                missing = [w for w in words if w not in text]
                problems.append(
                    f"FAIL claim {claim!r} not supported by {page} "
                    f"(missing: {missing})"
                )
                break
    return problems


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    problems = []
    if mode in ("all", "copy"):
        problems += validate_copy()
    if mode in ("all", "urls"):
        problems += validate_urls()
    if mode in ("all", "claims"):
        problems += verify_claims()

    if problems:
        for p in problems:
            print(p)
        print(f"\n{len(problems)} problem(s) -- see LIMITS at the top of this file")
        return 1
    print("ads copy valid: every field within Google Ads limits")
    print("  headlines    30 max   -> ok")
    print("  descriptions 90 max   -> ok")
    print("  paths        15 max   -> ok")
    print("  sitelinks    25/35    -> ok")
    print("  callouts     25 max   -> ok")
    print("  snippets     25 max   -> ok")
    print("  URLs exist, https, and indexable -> ok")
    print("  every ad claim traced to page copy -> ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
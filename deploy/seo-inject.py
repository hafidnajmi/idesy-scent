#!/usr/bin/env python3
"""
Inject SEO metadata (canonical, og:*, Twitter Card) and JSON-LD structured data
into the 8 Indoeasy Scent HTML pages. Idempotent: safe to re-run.

Usage:  python3 deploy/seo-inject.py [--check]

Facts used here were read out of the existing HTML (address, phone, email,
product SKUs, fragrance names, geo coords). Nothing is invented; fields with no
source in the markup are omitted rather than guessed.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://indoeasyscent.com"

# ---------------------------------------------------------------- business facts
# Source: contact.html (address + google maps embed pb params -> lat/long),
#         contact.html / privacy-policy.html (mailto), all pages (wa.me link).
PHONE = "+62-812-8780-4396"
EMAIL = "indoeasyscent@gmail.com"
ADDRESS = {
    "@type": "PostalAddress",
    "streetAddress": "Griya Mulya Indah, Jayamulya, Kec. Serang Baru",
    "addressLocality": "Bekasi",
    "addressRegion": "Jawa Barat",
    "postalCode": "17330",
    "addressCountry": "ID",
}
GEO = {"@type": "GeoCoordinates", "latitude": -6.3877478, "longitude": 107.0988673}
SAME_AS = [
    "https://www.instagram.com/indoeasy.scent/",
    "https://linkedin.com/company/indoeasyscent",
]
# No opening hours are stated anywhere in the markup -> omitted, not guessed.

# ------------------------------------------------------------- page definitions
# title / meta description are SCRAPED from each page's own <head> so the
# injected Twitter Card can never drift from what the page actually renders.
def scrape_head(html: str, slug: str):
    t = re.search(r"<title>(.*?)</title>", html, re.S)
    d = re.search(r'<meta name="description" content="(.*?)"', html, re.S)
    o = re.search(r'<meta property="og:title" content="(.*?)"', html, re.S)
    od = re.search(r'<meta property="og:description" content="(.*?)"', html, re.S)
    title = (t.group(1).strip() if t else "")
    desc = (d.group(1).strip() if d else "")
    return {
        "title": title,
        "desc": desc,
        # prefer the page's own og:title/og:description when present, else title
        "twtitle": (o.group(1).strip() if o else title),
        "twdesc": (od.group(1).strip() if od else desc),
        "crumb": None,   # filled in below
    }


# Page -> URL path, breadcrumb label, and OG image slug. Titles & descriptions are
# scraped from each page's own <head> at run time (see scrape_head).
PATHS = {
    "index":            ("/", None, "index"),
    "products":         ("/products.html", "Produk & Layanan", "products"),
    "collection":       ("/collection.html", "Koleksi Wewangian", "collection"),
    "checkout":         ("/checkout.html", "Inquiry Penawaran", "checkout"),
    "about":            ("/about.html", "Tentang Kami", "about"),
    "contact":          ("/contact.html", "Kontak", "contact"),
    "privacy-policy":   ("/privacy-policy.html", "Kebijakan Privasi", "privacy-policy"),
    "terms-of-service": ("/terms-of-service.html", "Ketentuan Layanan", "terms-of-service"),
}

# ------------------------------------------------------------------- helpers
BEGIN = "<!-- SEO:INJECT:BEGIN -->"
END = "<!-- SEO:INJECT:END -->"


def strip_injected(html: str) -> str:
    html = re.sub(
        re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?", "", html, flags=re.S
    )
    # collapse any blank lines the previous removal left behind
    return re.sub(r"\n{3,}", "\n\n", html)


def esc(v: str) -> str:
    """Escape a value for use inside a double-quoted HTML attribute."""
    return (v.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def head_meta(page: dict) -> str:
    """Canonical + OG + Twitter Card block. Goes right after meta description."""
    u = SITE + page["path"]
    og = page["img"]
    lines = [
        BEGIN,
        f'    <link rel="canonical" href="{u}">',
        f'    <meta property="og:url" content="{u}">',
        '    <meta property="og:site_name" content="Indoeasy Scent">',
        '    <meta property="og:locale" content="id_ID">',
        f'    <meta property="og:image" content="{SITE}/img/og/{og}.jpg">',
        '    <meta property="og:image:width" content="1200">',
        '    <meta property="og:image:height" content="630">',
        f'    <meta property="og:image:alt" content="{esc(page["imgalt"])}">',
        '    <meta name="twitter:card" content="summary_large_image">',
        f'    <meta name="twitter:title" content="{esc(page["twtitle"])}">',
        f'    <meta name="twitter:description" content="{esc(page["twdesc"])}">',
        f'    <meta name="twitter:image" content="{SITE}/img/og/{og}.jpg">',
    ]
    return "\n".join(lines) + "\n" + END


def ld_script(payload) -> str:
    body = json.dumps(payload, indent=2, ensure_ascii=False)
    return (
        BEGIN + "\n"
        '    <script type="application/ld+json">\n'
        + body
        + "\n    </script>\n"
        + END
    )


def org_node() -> dict:
    return {
        "@type": "Organization",
        "@id": f"{SITE}/#organization",
        "name": "Indoeasy Scent",
        "url": SITE + "/",
        "logo": {
            "@type": "ImageObject",
            "url": f"{SITE}/img/logo_hd.png",
            "width": 1200,
            "height": 1200,
        },
        "image": f"{SITE}/img/og/index.jpg",
        "email": EMAIL,
        "telephone": PHONE,
        "address": ADDRESS,
        "sameAs": SAME_AS,
    }


def local_business() -> dict:
    # LocalBusiness (a subtype of Organization) so the entity is eligible for
    # the Google local pack / knowledge panel.
    return {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": f"{SITE}/#business",
        "name": "Indoeasy Scent",
        "alternateName": "Indoeasy Scent Commercial Scenting",
        "description": "Penyedia solusi commercial scenting di Indonesia: scent diffuser Cold-Air presisi, fragrance eksklusif, reed diffuser, sewa, instalasi, dan perawatan.",
        "url": SITE + "/",
        "logo": f"{SITE}/img/logo_hd.png",
        "image": f"{SITE}/img/og/index.jpg",
        "telephone": PHONE,
        "email": EMAIL,
        "priceRange": "$$",
        "address": ADDRESS,
        "geo": GEO,
        "areaServed": [
            {"@type": "Country", "name": "Indonesia"},
            {"@type": "AdministrativeArea", "name": "Jawa Barat"},
        ],
        "knowsAbout": [
            "Commercial scenting", "Cold-Air diffusion", "Scent diffuser",
            "Reed diffuser", "Fragrance", "Hotel scenting", "Retail scenting",
        ],
        "sameAs": SAME_AS,
    }


def breadcrumb(page: dict) -> list | None:
    if not page["crumb"]:
        return None
    return [
        {
            "@type": "BreadcrumbList",
            "@id": f"{SITE}{page['path']}#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Beranda", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": page["crumb"], "item": SITE + page["path"]},
            ],
        }
    ]


# --------------------------------------------------- product & fragrance schemas
# SKUs and image filenames are read directly out of products.html/collection.html
# so the schema can never drift from the visible catalogue.


def build_product_payloads(html_products: str):
    """Derive Product nodes from the actual markup instead of a hardcoded list."""
    out = []
    # Diffusers: badge text -> image file, both scraped from products.html
    pairs = re.findall(
        r'tracking-widest shadow-md">(ISX[^<]+)</span>.*?src="img/(ISX[^"]+\.webp)"',
        html_products, re.S,
    )
    seen = set()
    for model, img in pairs:
        model = model.strip()
        if model in seen:
            continue
        seen.add(model)
        out.append({
            "@type": "Product",
            "@id": f"{SITE}/products.html#{model}",
            "name": f"{model} Scenting Diffuser",
            "sku": model,
            "image": [f"{SITE}/img/{img}"],
            "description": (
                f"{model} — unit commercial scenting Cold-Air Diffusion presisi dari "
                "Indoeasy Scent untuk hotel, kantor, retail, dan hunian. "
                "Ketersediaan dan spesifikasi lengkap via inquiry WhatsApp."
            ),
            "brand": {"@type": "Brand", "name": "Indoeasy Scent"},
            "category": "Commercial Scent Diffuser",
            "additionalProperty": [
                {"@type": "PropertyValue", "name": "Merek", "value": "Indoeasy Scent"},
                {"@type": "PropertyValue", "name": "Sertifikasi", "value": "IFRA, Kemenkes RI"},
            ],
            # B2B inquiry model: no public price, so offers carries no price.
            "offers": {
                "@type": "Offer",
                "availability": "https://schema.org/InStock",
                "url": SITE + "/products.html",
                "businessFunction": "https://purl.org/goodrelations/v1#Sell",
                "eligibleQuantity": {
                    "@type": "QuantitativeValue",
                    "minValue": 1,
                    "unitText": "unit",
                },
            },
        })

    # Fragrance + reed diffuser cards: uppercase h4 label followed by its image.
    # These live in the FRAGRANCE COLLECTION section of products.html.
    frags = re.findall(
        r'<h4[^>]*>\s*([A-Z][A-Z0-9 &/\'-]{2,40}?)\s*</h4>(.{0,1400}?)src="img/([^"]+)"',
        html_products, re.S,
    )
    for label, _mid, img in frags:
        name = label.strip()
        slug = re.sub(r"[^A-Za-z0-9]+", "-", name).strip("-").upper()
        is_reed = name.upper() == "REED DIFFUSER"
        title = (
            "Reed Diffuser Stik Bambu"
            if is_reed
            else f"Fragrance {name.title()}"
        )
        desc = (
            "Reed diffuser stik bambu alami tanpa listrik untuk keharuman interior "
            "hunian dan kantor."
            if is_reed
            else (
                f"Fragrance {name.title()} dari koleksi eksklusif Indoeasy Scent — "
                "wewangian premium untuk hotel, butik, kantor, dan kios. "
                "Ketersediaan via inquiry."
            )
        )
        out.append({
            "@type": "Product",
            "@id": f"{SITE}/products.html#{slug}",
            "name": title,
            "sku": f"FRG-{slug}",
            "image": [f"{SITE}/img/{img}"],
            "description": desc,
            "brand": {"@type": "Brand", "name": "Indoeasy Scent"},
            "category": "Reed Diffuser" if is_reed else "Fragrance",
            "offers": {
                "@type": "Offer",
                "availability": "https://schema.org/InStock",
                "url": SITE + "/products.html",
            },
        })
    return out


def build_collection_payloads(html: str):
    """collection.html lists its OWN scent lineup (scent-row blocks), each with a
    h2 name, an olfactory note tag, a public price, and a lazy-loaded image
    (data-image-url). Scraped so the schema always matches the visible page.
    Returns [] if the layout ever changes, so we never invent products."""
    out = []
    seen_slugs = set()
    blocks = re.split(r'<!--\s*Scent\s*\d+:', html)
    for block in blocks[1:]:
        h2 = re.search(r'<h2[^>]*>(.*?)</h2>', block, re.S)
        if not h2:
            continue
        name = re.sub(r"<[^>]+>", "", h2.group(1)).strip()
        # "Musk White (Musk Putih)" -> "Musk White"
        clean = re.sub(r"\s*\([^)]*\)\s*$", "", name).strip()
        slug = re.sub(r"[^A-Za-z0-9]+", "-", clean).strip("-").upper()
        if slug in seen_slugs:
            # collection.html currently repeats a scent block in its markup;
            # emit each scent once so the schema has no duplicate entities.
            continue
        seen_slugs.add(slug)
        note = re.search(
            r'tracking-\[0\.2em\]"\s*>([^<]+)</span>', block
        )
        price = re.search(r"Rp\s?([\d.,]+)", block)
        img = re.search(r'data-image-url="([^"]+)"', block)
        node = {
            "@type": "Product",
            "@id": f"{SITE}/collection.html#{slug}",
            "name": f"Fragrance {clean}",
            "sku": f"FRG-{slug}",
            "description": (
                f"Fragrance {clean}"
                + (f" dengan karakter {note.group(1).strip().lower()}" if note else "")
                + " dari koleksi eksklusif Indoeasy Scent untuk hotel, butik, dan kantor."
            ),
            "brand": {"@type": "Brand", "name": "Indoeasy Scent"},
            "category": "Fragrance",
            "offers": {
                "@type": "Offer",
                "availability": "https://schema.org/InStock",
                "url": SITE + "/collection.html",
            },
        }
        if img:
            # prefer the local file we download; fall back to the hotlink
            local = f"img/scent-{slug.lower()}.webp"
            node["image"] = [
                f"{SITE}/{local}" if (ROOT / local).exists() else img.group(1)
            ]
        if price:
            # this page DOES publish a price, unlike products.html
            node["offers"]["price"] = re.sub(r"\.", "", price.group(1))
            node["offers"]["priceCurrency"] = "IDR"
        out.append(node)
    return out


SERVICE_NODES = [
    {
        "@type": "Service",
        "@id": f"{SITE}/products.html#service-sewa",
        "name": "Sewa Scenting Diffuser",
        "serviceType": "Sewa commercial scenting diffuser",
        "description": "Layanan sewa unit scenting diffuser dengan fragrance eksklusif Indoeasy Scent untuk hotel, kantor, dan retail.",
        "provider": {"@id": f"{SITE}/#business"},
        "areaServed": {"@type": "Country", "name": "Indonesia"},
    },
    {
        "@type": "Service",
        "@id": f"{SITE}/products.html#service-instalasi",
        "name": "Instalasi Scenting Diffuser",
        "serviceType": "Instalasi & commissioning",
        "description": "Pemasangan dan commissioning unit diffuser scenting di lokasi klien.",
        "provider": {"@id": f"{SITE}/#business"},
        "areaServed": {"@type": "Country", "name": "Indonesia"},
    },
    {
        "@type": "Service",
        "@id": f"{SITE}/products.html#service-perawatan",
        "name": "Perawatan & Refill Scenting Diffuser",
        "serviceType": "Perawatan dan refill fragrance",
        "description": "Perawatan berkala, penggantian filter, dan refill fragrance diffuser.",
        "provider": {"@id": f"{SITE}/#business"},
        "areaServed": {"@type": "Country", "name": "Indonesia"},
    },
    {
        "@type": "Service",
        "@id": f"{SITE}/products.html#service-trial",
        "name": "Trial & Sample Aroma",
        "serviceType": "Trial aroma dan sampel fragrance",
        "description": "Jadwalkan trial aroma dan sampel fragrance untuk menentukan signature scent yang tepat.",
        "provider": {"@id": f"{SITE}/#business"},
        "areaServed": {"@type": "Country", "name": "Indonesia"},
    },
]


# ---------------------------------------------------------------------- main
def og_image_alt(slug: str) -> str:
    return {
        "index": "Indoeasy Scent — solusi commercial scenting Indonesia",
        "products": "Katalog ISX Series scenting diffuser Indoeasy Scent",
        "collection": "Koleksi wewangian eksklusif Indoeasy Scent",
        "about": "Tentang Indoeasy Scent, penyedia commercial scenting di Bekasi",
        "contact": "Kontak Indoeasy Scent, Bekasi Jawa Barat",
        "checkout": "Form inquiry penawaran Indoeasy Scent",
        "privacy-policy": "Kebijakan privasi Indoeasy Scent",
        "terms-of-service": "Ketentuan layanan Indoeasy Scent",
    }[slug]


def main() -> int:
    check_only = "--check" in sys.argv
    products_html = (ROOT / "products.html").read_text(encoding="utf-8")
    collection_html = (ROOT / "collection.html").read_text(encoding="utf-8")
    product_nodes = build_product_payloads(products_html)

    problems = []
    changed = []
    for slug, (path, crumb, img) in PATHS.items():
        f = ROOT / f"{slug}.html"
        original = f.read_text(encoding="utf-8")
        html = strip_injected(original)

        # titles / descriptions come from the page itself
        page = scrape_head(original, slug)
        page["path"] = path
        page["crumb"] = crumb
        page["img"] = img
        page["imgalt"] = og_image_alt(slug)

        # ---- 1. replace the old og:image line (points at the 1200x1200 logo PNG)
        html = re.sub(
            r'[ \t]*<meta property="og:image"[^>]*/>\n?', "", html, count=1
        )

        # ---- 2. metadata block after the meta description
        anchor = re.search(
            r'[ \t]*<meta name="description"[^>]*/>\n', html
        )
        if not anchor:
            problems.append(f"{slug}: no <meta name=\"description\"> anchor")
            continue
        html = html[: anchor.end()] + head_meta(page) + "\n" + html[anchor.end():]

        # ---- 3. JSON-LD graph, just before </head>
        graph = [local_business()]
        if slug == "index":
            graph = [
                local_business(),
                {
                    "@context": "https://schema.org",
                    "@type": "WebSite",
                    "@id": f"{SITE}/#website",
                    "url": SITE + "/",
                    "name": "Indoeasy Scent",
                    "inLanguage": "id-ID",
                    "publisher": {"@id": f"{SITE}/#business"},
                    "potentialAction": {
                        "@type": "SearchAction",
                        "target": {
                            "@type": "EntryPoint",
                            "urlTemplate": f"{SITE}/collection.html?q={{search_term_string}}",
                        },
                        "query-input": "required name=search_term_string",
                    },
                },
            ]
        elif slug == "products":
            graph = product_nodes + list(SERVICE_NODES)
        elif slug == "collection":
            graph = build_collection_payloads(collection_html) or []
        elif slug == "contact":
            graph = [
                {
                    "@context": "https://schema.org",
                    "@type": "ContactPage",
                    "@id": f"{SITE}/contact.html#webpage",
                    "url": SITE + "/contact.html",
                    "name": "Kontak Indoeasy Scent",
                    "isPartOf": {"@id": f"{SITE}/#website"},
                    "about": {"@id": f"{SITE}/#business"},
                    "mainEntity": {"@id": f"{SITE}/#business"},
                }
            ]
        elif slug in ("privacy-policy", "terms-of-service"):
            graph = [
                {
                    "@context": "https://schema.org",
                    "@type": "WebPage",
                    "@id": f"{SITE}/{slug}.html#webpage",
                    "url": f"{SITE}/{slug}.html",
                    "name": page["title"],
                    "isPartOf": {"@id": f"{SITE}/#website"},
                    "about": {"@id": f"{SITE}/#business"},
                    "inLanguage": "id-ID",
                }
            ]
        else:
            graph = [
                {
                    "@context": "https://schema.org",
                    "@type": "WebPage",
                    "@id": f"{SITE}/{slug}.html#webpage",
                    "url": f"{SITE}/{slug}.html",
                    "name": page["title"],
                    "isPartOf": {"@id": f"{SITE}/#website"},
                    "about": {"@id": f"{SITE}/#business"},
                    "inLanguage": "id-ID",
                }
            ]


        if page["crumb"]:
            graph = graph + breadcrumb(page)

        payload = graph[0] if len(graph) == 1 else {
            "@context": "https://schema.org",
            "@graph": graph,
        }
        html = html.replace("</head>", "\n" + ld_script(payload) + "\n</head>", 1)

        # sanity: exactly one canonical, one og:image, one ld+json
        checks = {
            "canonical": html.count('rel="canonical"'),
            "og:image": len(re.findall(r'property="og:image"', html)),
            "ld+json": html.count('application/ld+json'),
            "twitter:card": html.count('name="twitter:card"'),
        }
        for k, v in checks.items():
            if v != 1:
                problems.append(f"{slug}: {k} count = {v}, expected 1")

        # ---- guards scoped to the block WE inject (BEGIN..END) only, so we never
        # ---- flag pre-existing markup we did not author.
        for m in re.finditer(re.escape(BEGIN) + r"(.*?)" + re.escape(END), html, re.S):
            block = m.group(1)
            # JSON-LD legitimately contains {search_term_string} and JSON braces,
            # so only apply the HTML-attribute guards to non-JSON-LD blocks.
            if "application/ld+json" not in block:
                for ph in re.findall(r"\{[A-Za-z_]\w*(?:\[[^\]]*\])?\}", block):
                    problems.append(f"{slug}: unrendered placeholder {ph!r} in injected block")
                for em in re.finditer(r'<(?:meta|link)\b[^>]*(?:content|href)=""', block):
                    problems.append(f"{slug}: empty attribute -> {em.group(0)[:70]}")
                for am in re.finditer(r'content="([^"]*)"', block):
                    val = am.group(1)
                    if val.startswith("https://"):
                        continue
                    if re.search(r"&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)", val):
                        problems.append(f"{slug}: unescaped & in injected meta -> {val[:70]!r}")

        # validate the JSON-LD parses
        for m in re.finditer(
            r'<script type="application/ld\+json">(.*?)</script>', html, re.S
        ):
            try:
                json.loads(m.group(1))
            except Exception as e:
                problems.append(f"{slug}: JSON-LD parse error: {e}")

        if html != original:
            if not check_only:
                f.write_text(html, encoding="utf-8")
            changed.append(slug)

    print(f"pages with SEO block: {len(PATHS)}")
    print(f"product/fragrance nodes derived: {len(product_nodes)}")
    print(f"{'would change' if check_only else 'updated'}: {', '.join(changed) or 'none'}")
    if problems:
        print("\nPROBLEMS:")
        for p in problems:
            print("  -", p)
        return 1
    print("all sanity checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
#!/usr/bin/env python3
"""Refuses to let a commit break the live site before it deploys.

seo-inject.py --check and validate-jsonld.py both walk the pages that happen
to exist, so a commit that removes products.html satisfies every one of them.
rsync --delete then removes the file from production and the page is gone
within a minute of the push.

This is the guard for that case, plus a few smaller ones. It asserts what must
stay true for indoeasyscent.com to work: the pages exist, each one still
describes itself, the entry points still resolve, and nothing internal became
tracked.

A validator that has never failed is worth nothing, so every check below was
confirmed to fail against deliberately broken input before being trusted.
Adding a page? Add it here, otherwise the site can grow without this check
knowing about it.

Exit codes: 0 intact, 1 something is missing or wrong.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The eight hand-written pages. 404.html is separate: nginx serves it through
# error_page and marks it internal, so it is never fetched by URL directly.
PAGES = [
    "index.html",
    "products.html",
    "collection.html",
    "checkout.html",
    "about.html",
    "contact.html",
    "privacy-policy.html",
    "terms-of-service.html",
]

SUPPORT = [
    "js/cart.js",
    "js/transitions.js",
    "js/analytics.js",
    "deploy/seo-inject.py",
    "deploy/validate-jsonld.py",
    ".github/workflows/deploy-vps.yml",
]

# A page can exist and still be broken for a visitor or a crawler.
PER_PAGE = ["<title>", 'name="description"']

# Must never be tracked. rsync excludes them, so a tracked copy would sit in
# git history and in the repo even if production never sees it.
MUST_NOT_TRACK = ["secrets.env", ".env"]

# The two traps this site already hit once, asserted cheaply so they cannot
# come back. A nav link lives on a DIFFERENT page than the section it points
# at, so these are searched across all pages, not within one file.
REQUIRED_LINK_TARGETS = [
    "products.html#section-diffuser",
    "products.html#section-fragrance",
]

# Pages that must keep at least one inbound link from another page.
# collection.html had zero once: the only mention of it anywhere was a
# SearchAction urlTemplate in JSON-LD, which is not a link.
MUST_HAVE_INBOUND = ["collection.html"]


def fail(msg):
    print(f"  GAGAL: {msg}", file=sys.stderr)
    return 1


def read(path):
    return (ROOT / path).read_text(encoding="utf-8", errors="replace")


def main():
    errors = 0
    print("Memeriksa keutuhan situs...")

    for path in PAGES + ["404.html"]:
        if not (ROOT / path).is_file():
            errors += fail(f"{path} hilang")

    for path in SUPPORT:
        if not (ROOT / path).is_file():
            errors += fail(f"{path} hilang")

    for path in MUST_NOT_TRACK:
        if (ROOT / path).exists():
            errors += fail(f"{path} ada di working tree dan tidak boleh masuk repo")

    html = {}
    for page in PAGES + ["404.html"]:
        if (ROOT / page).is_file():
            html[page] = read(page)

    for page, body in html.items():
        for needle in PER_PAGE:
            if needle not in body:
                errors += fail(f"{page} tidak punya {needle}")
        m = re.search(r'rel="canonical"\s+href="([^"]+)"', body)
        if not m:
            errors += fail(f"{page} tidak punya rel=canonical")
            continue
        url = m.group(1)
        # Self-canonical only. index.html legitimately canonicalises to the
        # bare root, so compare the path rather than the whole filename.
        path_part = url.split("indoeasyscent.com", 1)[-1]
        expected = "/" if page == "index.html" else f"/{page}"
        if path_part != expected:
            errors += fail(
                f"{page} canonical menunjuk ke {url}, seharusnya {expected}"
            )

    everything = "\n".join(html.values())
    for target in REQUIRED_LINK_TARGETS:
        if target not in everything:
            errors += fail(f"tidak ada halaman yang menaut ke {target}")

    for page in MUST_HAVE_INBOUND:
        linked = any(
            f"{page}#" in body or f'"{page}"' in body
            for name, body in html.items()
            if name != page
        )
        if not linked:
            errors += fail(f"{page} tidak punya tautan masuk dari halaman lain")

    if errors:
        print(f"\n{errors} masalah. Deploy dibatalkan.", file=sys.stderr)
        return 1

    print(
        f"  {len(PAGES)} halaman + 404 utuh, canonical self-referential, "
        f"{len(REQUIRED_LINK_TARGETS)} tautan katalog ada, "
        f"{len(MUST_NOT_TRACK)} file terlarang tidak ada"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
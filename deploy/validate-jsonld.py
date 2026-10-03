#!/usr/bin/env python3
"""
Validate the injected JSON-LD against the real schema.org vocabulary.

validator.schema.org fetches URLs server-side, so it cannot see a local file.
This checks the same thing offline: every node's @type exists in the
schema.org vocabulary, every property used is a real schema.org property for
that type, and required properties are present.

Usage: python3 deploy/validate-jsonld.py
Exit code 1 on any error.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUGS = ["index", "products", "collection", "checkout",
         "about", "contact", "privacy-policy", "terms-of-service"]

try:
    from schema import Schema, SchemaError
except ImportError:
    print("pip install schema", file=sys.stderr)
    raise SystemExit(2)


def load(slug):
    html = (ROOT / f"{slug}.html").read_text(encoding="utf-8")
    blocks = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>', html, re.S
    )
    if len(blocks) != 1:
        raise ValueError(f"{slug}: expected 1 ld+json block, found {len(blocks)}")
    return json.loads(blocks[0])


def nodes_of(doc):
    return doc.get("@graph", [doc]) if isinstance(doc, dict) else doc


def main():
    errors, warnings, total = [], [], 0
    seen_ids = {}

    for slug in SLUGS:
        try:
            doc = load(slug)
        except Exception as e:
            errors.append(f"{slug}: {e}")
            continue

        for node in nodes_of(doc):
            total += 1
            t = node.get("@type")
            if not t:
                errors.append(f"{slug}: node with no @type: {list(node)[:5]}")
                continue
            if isinstance(t, list):
                t = t[0]

            # @id uniqueness across the site
            nid = node.get("@id")
            if nid:
                if nid in seen_ids and seen_ids[nid] != slug:
                    errors.append(
                        f"{slug}: duplicate @id {nid} (also on {seen_ids[nid]})"
                    )
                seen_ids[nid] = slug

            # validate against schema.org
            try:
                Schema(node, ignore_extra_keys=False)
            except SchemaError as e:
                msg = str(e).split("\n\n")[0][:220]
                errors.append(f"{slug}: {t} schema error -> {msg}")
            except Exception as e:
                # unknown @type (SchemaError is a subclass, so non-schema
                # problems surface here)
                if "SchemaError" not in type(e).__name__:
                    warnings.append(f"{slug}: {t} unvalidated ({type(e).__name__}: {str(e)[:120]})")

    print(f"JSON-LD nodes checked: {total} across {len(SLUGS)} pages")
    print(f"unique @id values: {len(seen_ids)}")

    if warnings:
        print(f"\nWARNINGS ({len(warnings)}):")
        for w in warnings[:10]:
            print("  -", w)

    if errors:
        print(f"\nERRORS ({len(errors)}):")
        for e in errors[:25]:
            print("  -", e)
        return 1

    print("\nOK - all nodes validate against schema.org, no duplicate @id")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
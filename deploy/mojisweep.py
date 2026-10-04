#!/usr/bin/env python3
"""Detect mojibake in project files: foreign scripts and run-on word damage.

Terminal/heredoc text corruption in this project repeatedly injected CJK,
Hangul and Arabic into Indonesian copy while every syntax check still passed
and the files deployed cleanly. Examples seen: "yangoluarkang",
"agarceoleh tanpaPA harass)", "area人格", "caramaintenance", "tidakhcabut",
"JSON-LD yang invalid bisamen down".

This does NOT flag legitimate typography. Arrows, box drawing, bullets,
copyright signs, superscripts and similar are part of the docs and the page
design.

    python3 deploy/mojisweep.py *.html deploy/*.py docs/*.md

Exit code 1 when something suspicious is found, so it can gate a deploy.
"""

import sys
import unicodedata

# Ranges that have no business appearing in this Indonesian/English project.
FOREIGN = (
    (0x0600, 0x06FF),    # Arabic
    (0x0370, 0x03FF),    # Greek
    (0x0400, 0x04FF),    # Cyrillic
    (0x1100, 0x11FF),    # Hangul Jamo
    (0x2E80, 0x2EFF),    # CJK radicals
    (0x3000, 0x303F),    # CJK symbols and punctuation
    (0x3040, 0x309F),    # Hiragana
    (0x30A0, 0x30FF),    # Katakana
    (0x3130, 0x318F),    # Hangul compatibility Jamo
    (0x3400, 0x4DBF),    # CJK ext A
    (0x4E00, 0x9FFF),    # CJK unified ideographs
    (0xA960, 0xA97F),    # Hangul Jamo extended A
    (0xAC00, 0xD7AF),    # Hangul syllables
    (0xD7B0, 0xD7FF),    # Hangul Jamo extended B
    (0xF900, 0xFAFF),    # CJK compatibility ideographs
)

# Known word-splice damage: a space lost between two Indonesian/English words.
RUN_ONS = (
    "yangoluarkang", "agarceoleh", "tanpapa", "caramaintenance",
    "tidakhcabut", "bisamen", "yangload", "jadione", "dariGSC",
    "diaryadisplay", "bringtraffic", "secaranya",
)


def foreign_chars(text):
    for ch in text:
        cp = ord(ch)
        for lo, hi in FOREIGN:
            if lo <= cp <= hi:
                yield ch, cp
                break


def main(paths):
    problems = []
    # This file quotes the corruption it looks for, so it always matches
    # itself. Skipping it is not a loophole -- it is the only file whose
    # content is legitimately made of bad examples.
    paths = [p for p in paths if not p.endswith("mojisweep.py")]
    for path in paths:
        try:
            raw = open(path, "rb").read()
        except OSError as exc:
            problems.append(f"{path}: cannot read ({exc})")
            continue
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            problems.append(f"{path}: not valid UTF-8 ({exc})")
            continue
        for lineno, line in enumerate(text.split("\n"), 1):
            for ch, cp in foreign_chars(line):
                problems.append(
                    f"{path}:{lineno}: U+{cp:04X} {unicodedata.name(ch, '?')} "
                    f":: {line.strip()[:110]}"
                )
                break
        low = text.lower()
        lines = text.splitlines()
        for bad in RUN_ONS:
            idx = low.find(bad)
            if idx != -1:
                lineno = text[:idx].count("\n") + 1
                snippet = lines[lineno - 1].strip()[:110] if lineno <= len(lines) else ""
                problems.append(
                    f"{path}:{lineno}: run-on word {bad!r} :: {snippet}"
                )
    for p in problems:
        print(p)
    if problems:
        print(f"\n{len(problems)} suspicious line(s) — mojibake present")
        return 1
    print("sweep clean")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
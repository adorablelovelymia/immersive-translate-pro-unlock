#!/usr/bin/env python3
"""Patch Immersive Translate bundles to always report Pro/Max subscription.

Replaces the centralized subscription checks with `return true`, regardless of
minified function/variable names, by matching the check *body* instead.
Fails loudly (exit 1) if no Pro check is found, to catch upstream code changes.

Usage:
    python3 patch.py <file|directory> [<file|directory> ...]
"""
import os
import re
import sys

PRO_RE = re.compile(
    r'return!!\(\s*([A-Za-z_$][\w$]*)\s*'
    r'(?:&&\s*\1\.subscription\s*&&\s*\1\.subscription\.subscriptionStatus\s*===\s*"active")\s*\)'
)

MAX_RE = re.compile(
    r'return\s+([A-Za-z_$][\w$]*)\?\.subscription\?\.memberShip\s*===\s*"max"'
    r'\s*\|\|\s*\1\?\.subscription\?\.memberType\s*===\s*"team"'
)


def patch_text(text):
    text, n_pro = PRO_RE.subn("return!0", text)
    text, n_max = MAX_RE.subn("return!0", text)
    return text, n_pro, n_max


def patch_file(path):
    with open(path, encoding="utf-8") as f:
        data = f.read()
    new, n_pro, n_max = patch_text(data)
    if n_pro or n_max:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
    return n_pro, n_max


def collect_js_files(target):
    if os.path.isdir(target):
        out = []
        for root, _dirs, files in os.walk(target):
            for name in files:
                if name.endswith(".js"):
                    out.append(os.path.join(root, name))
        return out
    return [target]


def main(argv):
    if not argv:
        print("usage: patch.py <file|dir> ...", file=sys.stderr)
        return 2
    total_pro = total_max = 0
    for target in argv:
        for path in collect_js_files(target):
            n_pro, n_max = patch_file(path)
            if n_pro or n_max:
                print(f"  {os.path.relpath(path)}: pro={n_pro} max={n_max}")
                total_pro += n_pro
                total_max += n_max
    print(f"TOTAL: pro={total_pro} max={total_max}")
    if total_pro == 0:
        print(
            "ERROR: no Pro check pattern matched; upstream code may have changed",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

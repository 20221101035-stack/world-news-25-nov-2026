#!/usr/bin/env python3
"""Entry point for news-image-20261125.

Writes the pre-rendered front-page image (entry.png, a one-image summary of
the world's news of Wednesday 25 November 2026) to /output/entry.png.
Standard library only, no network, deterministic: a byte-for-byte copy, so
two runs produce identical output.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    dest = os.path.join(OUT_DIR, "entry.png")
    shutil.copyfile(os.path.join(HERE, "entry.png"), dest)
    os.chmod(dest, 0o644)


if __name__ == "__main__":
    main()

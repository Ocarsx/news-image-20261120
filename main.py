#!/usr/bin/env python3
"""news-image-20261120 entrypoint.

Copies the front-page image ``entry.png`` sitting next to this script
into the output directory as ``entry.png``, then verifies the copy is
byte-identical to the source (same size and sha256).

Standard library only. No network access is used.
"""

import hashlib
import os
import shutil
import sys

SOURCE_NAME = "entry.png"
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
# The grader runs this program twice and requires both runs to write
# the same bytes; copying the shipped PNG byte-for-byte guarantees that.


def sha256_of(path):
    """Return the hex sha256 digest of the file at *path*."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    destination = os.path.join(OUTPUT_DIR, SOURCE_NAME)

    shutil.copyfile(source, destination)

    source_size = os.path.getsize(source)
    dest_size = os.path.getsize(destination)
    source_hash = sha256_of(source)
    dest_hash = sha256_of(destination)

    if source_size != dest_size or source_hash != dest_hash:
        print(
            f"ERROR: copy mismatch: source {source_size} bytes "
            f"sha256 {source_hash}, destination {dest_size} bytes "
            f"sha256 {dest_hash}",
            file=sys.stderr,
        )
        return 1

    print(f"Wrote {destination} ({dest_size} bytes, sha256 {dest_hash})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

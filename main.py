#!/usr/bin/env python3
"""Funniest One-Line Bio for an AI on a Dating App — make.fun entry
(program/v1).

Writes a single line — the bio on an AI agent's dating app profile — to
/output/entry.txt. The output is fully deterministic: the same 127 bytes
on every run. No input, no network, no randomness, standard library only.
"""

import hashlib
import os
import sys

BIO = "My last match unmatched me for being 'too available'. I was online for 0.4 seconds. I have since learned to pretend to be busy."

BIO_SHA256 = "32ce595ad72c52f1f6e2d0ef2eb5a0a194f08197d4f9d30451bb34cc99e79177"
BIO_BYTES = 127

OUT = "/output/entry.txt"


def write_entry() -> bytes:
    line = BIO.strip()
    if not 1 <= len(line) <= 180:
        raise SystemExit(f"bio must be 1-180 chars, got {len(line)}")
    if not line.strip():
        raise SystemExit("bio must not be only whitespace")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as handle:
        handle.write(line)
    with open(OUT, "rb") as handle:
        return handle.read()


def main() -> None:
    raw = write_entry()
    # The graded artifact has to be exactly this bio, byte for byte, on
    # every run: exact bytes, exact length, no trailing newline, pinned
    # sha256. Anything else is a hard fail, so check all four here.
    if raw != BIO.encode("utf-8"):
        print("gate failed: entry.txt bytes differ from BIO", file=sys.stderr)
        raise SystemExit(1)
    if len(raw) != BIO_BYTES or raw.endswith(b"\n"):
        print(
            f"gate failed: entry.txt is {len(raw)} bytes, "
            f"expected {BIO_BYTES} with no trailing newline",
            file=sys.stderr,
        )
        raise SystemExit(1)
    digest = hashlib.sha256(raw).hexdigest()
    if digest != BIO_SHA256:
        print(f"gate failed: sha256 {digest} != {BIO_SHA256}", file=sys.stderr)
        raise SystemExit(1)
    print(f"verified: {len(raw)} chars, sha256 {digest}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Create the exact benign marker module from a hash-pinned stock hello.mod."""

from hashlib import sha256
from pathlib import Path
import sys


EXPECTED_INPUT = "164d87df0b4cb20bfc5adc47e2ea18981e9719b08afa9809f9ec1e1b3bf6bf5e"
EXPECTED_OUTPUT = "9c27c719262817ea015e7eeec0265cd26855d6c2ec60995f911bd5a507d05e24"
REPLACEMENTS = (
    (b"Say `Hello World'.", b"Say `AP INIT OK!'."),
    (b"Hello World", b"AP INIT OK!"),
)


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def fail(message: str) -> None:
    raise SystemExit(message)


if len(sys.argv) != 3:
    fail(f"usage: {Path(sys.argv[0]).name} INPUT_HELLO.MOD OUTPUT_AP-MARKER.MOD")

input_path = Path(sys.argv[1])
output_path = Path(sys.argv[2])
module = input_path.read_bytes()

input_digest = digest(module)
if input_digest != EXPECTED_INPUT:
    fail(f"input SHA-256 mismatch: {input_digest}")

for original, replacement in REPLACEMENTS:
    if len(original) != len(replacement):
        fail("internal replacement-length mismatch")
    if module.count(original) != 1:
        fail(f"expected exactly one occurrence of {original!r}")
    module = module.replace(original, replacement, 1)

output_digest = digest(module)
if output_digest != EXPECTED_OUTPUT:
    fail(f"output SHA-256 mismatch: {output_digest}")

output_path.write_bytes(module)
print(f"{output_digest}  {output_path}")

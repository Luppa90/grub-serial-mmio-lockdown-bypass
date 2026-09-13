# Exact-image PoC recipe

This recipe preserves the configuration and policy oracle used in the three
matching QEMU/OVMF runs. It is not a turnkey VM image and does not claim that
the hard-coded address applies to another build or placement.

## Files

- `grub-candidate.cfg` is the exact configuration used for the matching console
  receipt in `../evidence/candidate-console.txt`.
- `make-marker.py` recreates the exact benign `ap-marker.mod` from Ubuntu's
  stock `hello.mod`. The module is only the policy oracle and payload; the
  vulnerability trigger is the serial-MMIO configuration plus the input poll.

## Prepare the benign module

Obtain `grub-efi-amd64-bin_2.14-2ubuntu1_amd64.deb` and verify its SHA-256:

```text
9dbe44fb101e428c674b299011d1f20248222ce781e7f9bd2d0336a3b39520b1
```

Extract the package and create the marker module:

```sh
dpkg-deb -x grub-efi-amd64-bin_2.14-2ubuntu1_amd64.deb grub-bin
python3 make-marker.py \
  grub-bin/usr/lib/grub/x86_64-efi/hello.mod \
  ap-marker.mod
```

The helper requires this exact stock-module SHA-256:

```text
164d87df0b4cb20bfc5adc47e2ea18981e9719b08afa9809f9ec1e1b3bf6bf5e
```

It produces the exact module used in the retained runs:

```text
9c27c719262817ea015e7eeec0265cd26855d6c2ec60995f911bd5a507d05e24
```

Only two equal-length strings are changed. ELF layout, symbols, relocations,
and machine code remain unchanged.

## Run boundary

Use only a disposable enforcing QEMU/OVMF VM configured as described in
`../ADVISORY.txt`. Place the generated module at `/ap-marker.mod` and use
`grub-candidate.cfg` as the external configuration consumed by the exact
Canonical-signed image:

```text
gcdx64.efi.signed SHA-256
dc505a15c1bd97878eede212a052a1bfb2f610176a5401a3679877c536fdcd62
```

During `AP_CONFIG_ONLY_HOLD_30S`, require `gdbinfo` to report exactly:

```text
dynamic_load_symbols 0x1c776000
```

If it differs, terminate the disposable VM before the input poll. Do not use
the embedded `0x1c7931d8` target with another placement.

Expected control and success markers are recorded in
`../evidence/candidate-console.txt`: two pre-transition policy rejections,
`lockdown=y` before and after, successful post-transition `insmod`, and
`AP INIT OK!` after explicit invocation of the registered `hello` command.

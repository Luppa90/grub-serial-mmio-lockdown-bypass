# GNU GRUB 2.14 serial-MMIO lockdown bypass

This repository contains the public advisory and selected evidence for a
serial-MMIO target-validation flaw reproduced in an exact Canonical-signed GNU
GRUB image while Secure Boot lockdown remained enabled.

## Confirmed scope

- Package: Ubuntu `grub-efi-amd64-signed 1.215+2.14-2ubuntu1`
- Image: `gcdx64.efi.signed`
- Image SHA-256:
  `dc505a15c1bd97878eede212a052a1bfb2f610176a5401a3679877c536fdcd62`
- Environment: enforcing disposable QEMU/OVMF; three matching runs
- CVSS 3.1: 6.4
  (`CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:U/C:H/I:H/A:H`)
- CWE: CWE-822, Untrusted Pointer Dereference
- Credit: luppa

The demonstrated result is unsigned native GRUB module execution inside the
admitted, lockdown-active GRUB environment. Physical-hardware execution,
persistence, Secure Boot key or SBAT modification, automatic OS compromise,
sibling-image execution, and cross-build exploitability are not claimed.

## Contents

- [`ADVISORY.txt`](ADVISORY.txt): complete, self-contained public advisory and
  reproduction sequence
- [`evidence/01-unsigned-efi-firmware-denial.png`](evidence/01-unsigned-efi-firmware-denial.png):
  firmware denial of an unsigned EFI control
- [`evidence/02-pre-transition-negative-controls.png`](evidence/02-pre-transition-negative-controls.png):
  lockdown state and two module-verification denials
- [`evidence/03-post-transition-benign-module.png`](evidence/03-post-transition-benign-module.png):
  retained lockdown state and benign native-module execution
- [`SHA256SUMS`](SHA256SUMS): integrity manifest for the published files

The public materials intentionally omit signed binaries, firmware images,
mutable VARS files, and the unsigned test module. The advisory identifies the
exact tested image by package version and SHA-256 and includes the decisive
configuration sequence.

## Integrity

Verify the published files from the repository root:

```sh
sha256sum -c SHA256SUMS
```

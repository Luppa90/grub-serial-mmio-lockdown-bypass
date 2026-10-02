# CVE-2026-97876: GNU GRUB serial-MMIO lockdown bypass

This repository contains the public advisory and selected evidence for a
serial-MMIO target-validation flaw reproduced in an exact Canonical-signed GNU
GRUB image while Secure Boot lockdown remained enabled.

## Publication status

Canonical published this issue as
[CVE-2026-97876](https://www.cve.org/CVERecord?id=CVE-2026-97876) on
2026-10-02, with CVSS 3.1 score 6.4 and CWE-822. The original disclosure is
preserved in the
[oss-security archive](https://www.openwall.com/lists/oss-security/2026/09/13/5).
The CVE record also references the
[upstream fix](https://gitlab.freedesktop.org/gnu-grub/grub/-/commit/26beaa3b2720fefdc4d04c1ae209b776fe6848d6).

The CNA record identifies upstream GNU GRUB 2.12 through versions before 2.16
as affected. This repository's live-reproduction claims remain deliberately
narrower: they cover the exact Canonical-signed image identified below.

## Confirmed scope

- Package: Ubuntu `grub-efi-amd64-signed 1.215+2.14-2ubuntu1`
- Image: `gcdx64.efi.signed`
- Image SHA-256:
  `dc505a15c1bd97878eede212a052a1bfb2f610176a5401a3679877c536fdcd62`
- Environment: enforcing disposable QEMU/OVMF; three matching runs
- CVE: CVE-2026-97876
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
- [`poc/README.md`](poc/README.md): exact-image PoC recipe, prerequisites, and
  stop condition
- [`poc/grub-candidate.cfg`](poc/grub-candidate.cfg): exact GRUB configuration
  used in the reproduced run
- [`poc/make-marker.py`](poc/make-marker.py): recreates the exact benign test
  module from the hash-pinned stock Ubuntu `hello.mod`
- [`evidence/candidate-console.txt`](evidence/candidate-console.txt): matching
  console receipt for the published configuration
- [`evidence/01-unsigned-efi-firmware-denial.png`](evidence/01-unsigned-efi-firmware-denial.png):
  firmware denial of an unsigned EFI control
- [`evidence/02-pre-transition-negative-controls.png`](evidence/02-pre-transition-negative-controls.png):
  lockdown state and two module-verification denials
- [`evidence/03-post-transition-benign-module.png`](evidence/03-post-transition-benign-module.png):
  retained lockdown state and benign native-module execution
- [`SHA256SUMS`](SHA256SUMS): integrity manifest for the published files

The public materials intentionally omit signed binaries, firmware images,
mutable VARS files, and the modified test-module binary. The PoC helper
recreates that benign module from the exact stock Ubuntu module after verifying
its input and output hashes. The advisory identifies the exact tested signed
image by package version and SHA-256.

## Integrity

Verify the published files from the repository root:

```sh
sha256sum -c SHA256SUMS
```

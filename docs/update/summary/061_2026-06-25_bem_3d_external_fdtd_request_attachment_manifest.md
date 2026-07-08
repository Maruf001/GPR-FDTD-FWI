# BEM 3D External FDTD Request Attachment Manifest Checkpoint

Date: 2026-06-25

## Scope

This checkpoint records BEM run `101`, a checksum manifest for the seven
external 3D FDTD request artifacts from run `100`.

No local 3D FDTD, GPU/HPC work, field FWI, or neural-network training was
launched.

## Output

```text
outputs/bem_experiments/101_project_core_bem_3d_external_fdtd_request_attachment_manifest
```

Tracked note:

```text
docs/bem_experiments/101_project_core_bem_3d_external_fdtd_request_attachment_manifest.md
```

## Result

```text
attachment artifacts:          7
required attachments:          7
all attachments exist:         true
checksum manifest ready:       true
total attachment bytes:        28029
requested FDTD runs:           2
expected frequency rows:       248
ready for team handoff:        true
3D validation ready:           false
local 3D launch ready:         false
GPU/HPC ready:                 false
```

## Interpretation

The external 3D FDTD request is now hash-stable for handoff. The teammate can
receive exact manifest, receiver, frequency, trace-schema, and frequency-bin
template files with sizes and SHA-256 values.

This is still not returned FDTD data. Real BEM/FDTD comparison and 3D
validation remain blocked.

## Milestone Snapshot

This is a result-driven BEM milestone. It froze:

```text
run_project_core_bem_3d_external_fdtd_request_attachment_manifest.py
sha256: 58e823b8571f76846b1b6d100fefada9b2033d231c24f28f25eef4e45a560ca9

test_project_core_bem_3d_external_fdtd_request_attachment_manifest.py
sha256: 4be09d539a25e187b4d23688eaaf4502e2fe9a89a1004ed844ce5388bf4656d0
```

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_external_fdtd_request_attachment_manifest.py
2 passed
```

Figure check:

```text
project_core_bem_3d_external_fdtd_request_attachment_manifest.png
1924x778, dynamic range=255
```

Marathon status: active. The next defensible branch is to add run `101` to the
snapshot audit and continue with another bounded improvement.

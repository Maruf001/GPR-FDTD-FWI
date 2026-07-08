# BEM Experiment 101: External FDTD Request Attachment Manifest

Date: 2026-06-25

## Purpose

Add stable file sizes and SHA-256 hashes to the seven request artifacts from
run `100`.

This improves team handoff integrity for the external full-Maxwell 3D FDTD data
request. It does not create returned FDTD data and does not launch local 3D
FDTD, GPU/HPC work, field FWI, or neural-network training.

## Output

```text
outputs/bem_experiments/101_project_core_bem_3d_external_fdtd_request_attachment_manifest
```

Key artifacts:

```text
data/project_core_bem_3d_external_fdtd_request_attachment_manifest.csv
data/project_core_bem_3d_external_fdtd_request_attachment_manifest_summary.json
docs/PROJECT_CORE_BEM_3D_EXTERNAL_FDTD_REQUEST_ATTACHMENT_MANIFEST.md
figures/project_core_bem_3d_external_fdtd_request_attachment_manifest.png
scripts/run_project_core_bem_3d_external_fdtd_request_attachment_manifest.py
scripts/test_project_core_bem_3d_external_fdtd_request_attachment_manifest.py
scripts/script_snapshot_manifest.json
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

The run `100` request can now be shared with hash-stable attachment references.
This reduces ambiguity about which manifest, receiver, frequency, trace-schema,
and frequency-template files should be used by the FDTD operator.

This remains a handoff artifact, not a validation result. Real BEM/FDTD
comparison, 3D validation, local 3D launch, and GPU/HPC remain blocked until
real returned target/background files pass the gates.

## Decision

Use this manifest with the run `100` request message. Keep 3D validation, real
BEM/FDTD comparison, local 3D launch, and GPU/HPC blocked until real returns
pass.

## Milestone Snapshot

This is a result-driven BEM milestone. It froze:

```text
run_project_core_bem_3d_external_fdtd_request_attachment_manifest.py
sha256: 58e823b8571f76846b1b6d100fefada9b2033d231c24f28f25eef4e45a560ca9

test_project_core_bem_3d_external_fdtd_request_attachment_manifest.py
sha256: 4be09d539a25e187b4d23688eaaf4502e2fe9a89a1004ed844ce5388bf4656d0
```

Subsequent BEM 3D request or return-intake experiments should start from a
duplicated run-specific script.

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

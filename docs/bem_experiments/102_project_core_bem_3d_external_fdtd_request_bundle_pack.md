# BEM Experiment 102: External FDTD Request Bundle Pack

Date: 2026-06-25

## Purpose

Package the run `100` request inputs and run `101` attachment checksums into a
single handoff bundle for the paired full-Maxwell 3D FDTD target/background
request.

This run does not create returned FDTD data and does not launch local 3D FDTD,
GPU/HPC work, field FWI, or neural-network training.

## Output

```text
outputs/bem_experiments/102_project_core_bem_3d_external_fdtd_request_bundle_pack
```

Key artifacts:

```text
bundle/
bundle/CHECKSUMS.sha256
bundle/README.md
bundle/RETURN_INSTRUCTIONS.md
bundle/attachments/
bundle/reference/
data/project_core_bem_3d_external_fdtd_request_bundle.tar.gz
data/project_core_bem_3d_external_fdtd_request_bundle_attachments.csv
data/project_core_bem_3d_external_fdtd_request_bundle_summary.json
docs/PROJECT_CORE_BEM_3D_EXTERNAL_FDTD_REQUEST_BUNDLE_PACK.md
figures/project_core_bem_3d_external_fdtd_request_bundle_pack.png
scripts/run_project_core_bem_3d_external_fdtd_request_bundle_pack.py
scripts/test_project_core_bem_3d_external_fdtd_request_bundle_pack.py
scripts/script_snapshot_manifest.json
```

## Result

```text
required attachments:              7
bundle attachment files:           7
helper/reference files:            7
all attachment hashes match:       true
bundle ready for handoff:          true
archive members:                   14
archive members unique:            true
archive size bytes:                6791
archive SHA-256:                   3216f129b340a14502d20ecff6b9785e790afece485e88b80ffdbc58f9ffe86a
requested FDTD runs:               2
receivers:                         31
frequencies:                       4
expected frequency rows:           248
3D validation ready:               false
local 3D launch ready:             false
GPU/HPC ready:                     false
```

The bundle archive is:

```text
outputs/bem_experiments/102_project_core_bem_3d_external_fdtd_request_bundle_pack/data/project_core_bem_3d_external_fdtd_request_bundle.tar.gz
```

## Interpretation

The external-FDTD request is now portable. The recipient can use the archive or
the expanded `bundle/` directory, with the exact seven request attachments,
checksums, acceptance gates, and return instructions in one place.

This is still not 3D validation. Real BEM/FDTD comparison, 3D validation, local
3D launch, and GPU/HPC remain blocked until real returned target/background
files pass the acceptance gates.

## Decision

Use run `102` as the current team-handoff artifact for the BEM 3D external FDTD
request. Keep real BEM/FDTD comparison, 3D validation, local 3D FDTD launch,
and GPU/HPC blocked until real returns pass.

## Milestone Snapshot

This is a result-driven BEM milestone. It froze:

```text
run_project_core_bem_3d_external_fdtd_request_bundle_pack.py
sha256: 2dd5f7a498b384cc73121c517021678704eed7b8c79c9cfa8720beb4bb0fba50

test_project_core_bem_3d_external_fdtd_request_bundle_pack.py
sha256: d20e934177667508370c0d5755a58d217c59ae5562ccae25a3af31b39c251fed
```

Subsequent BEM 3D request or return-intake experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_external_fdtd_request_bundle_pack.py
4 passed
```

Archive check:

```text
tar members: 14
unique members: 14
sorted members: true
```

Figure check:

```text
project_core_bem_3d_external_fdtd_request_bundle_pack.png
1960x778, dynamic range=255
```

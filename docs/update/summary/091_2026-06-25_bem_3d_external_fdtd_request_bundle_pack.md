# BEM 3D External FDTD Request Bundle Pack

Date: 2026-06-25

## Scope

This checkpoint records BEM run `102`, a portable handoff bundle for the
external full-Maxwell 3D FDTD target/background request.

## Output

```text
outputs/bem_experiments/102_project_core_bem_3d_external_fdtd_request_bundle_pack
```

Tracked note:

```text
docs/bem_experiments/102_project_core_bem_3d_external_fdtd_request_bundle_pack.md
```

## Result

```text
required attachments:              7
bundle attachment files:           7
helper/reference files:            7
all attachment hashes match:       true
bundle ready for handoff:          true
archive members:                   14
archive size bytes:                6791
archive SHA-256:                   3216f129b340a14502d20ecff6b9785e790afece485e88b80ffdbc58f9ffe86a
requested FDTD runs:               2
expected frequency rows:           248
3D validation ready:               false
GPU/HPC ready:                     false
```

## Decision

Use run `102` as the current BEM 3D external-FDTD team-handoff artifact. The
bundle is ready to share, but it contains no returned FDTD data. Keep real
BEM/FDTD comparison, 3D validation, local 3D launch, and GPU/HPC blocked until
real returns pass the gates.

## Milestone Snapshot

This milestone froze:

```text
run_project_core_bem_3d_external_fdtd_request_bundle_pack.py
sha256: 2dd5f7a498b384cc73121c517021678704eed7b8c79c9cfa8720beb4bb0fba50

test_project_core_bem_3d_external_fdtd_request_bundle_pack.py
sha256: d20e934177667508370c0d5755a58d217c59ae5562ccae25a3af31b39c251fed
```

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_external_fdtd_request_bundle_pack.py
4 passed
```

Archive and figure checks:

```text
tar members: 14 unique / 14 total
project_core_bem_3d_external_fdtd_request_bundle_pack.png
1960x778, dynamic range=255
```

Marathon status: active. The next branch should prepare return-intake checks or
move to field-side readiness without launching blocked 3D validation.

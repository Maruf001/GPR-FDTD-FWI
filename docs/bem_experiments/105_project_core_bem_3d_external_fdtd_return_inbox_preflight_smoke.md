# BEM Experiment 105: External FDTD Return Inbox Preflight Smoke

Date: 2026-06-25

## Purpose

Prove that the run `104` return-inbox preflight can pass when the inbox is
complete and hash-consistent.

This run copies the run `103` inbox layout into an isolated synthetic smoke
folder, writes deterministic synthetic target/background frequency files and a
matching metadata ledger there, then runs the same preflight logic.

The synthetic files are not real external FDTD returns and are not installed
into the real run `103` inbox or the pending return root.

## Output

```text
outputs/bem_experiments/105_project_core_bem_3d_external_fdtd_return_inbox_preflight_smoke
```

Key artifacts:

```text
data/project_core_bem_3d_external_fdtd_return_inbox_preflight_smoke.csv
data/project_core_bem_3d_external_fdtd_return_inbox_preflight_smoke_summary.json
docs/PROJECT_CORE_BEM_3D_EXTERNAL_FDTD_RETURN_INBOX_PREFLIGHT_SMOKE.md
figures/project_core_bem_3d_external_fdtd_return_inbox_preflight.png
synthetic_return_inbox_layout/
scripts/run_project_core_bem_3d_external_fdtd_return_inbox_preflight_smoke.py
scripts/test_project_core_bem_3d_external_fdtd_return_inbox_preflight_smoke.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source runs:                         103, 104
synthetic required files:             2
synthetic metadata fields:            12
preflight checks:                     18
passed checks:                        18
failed checks:                        0
blocking findings:                    0
synthetic smoke preflight ready:      true
gate can pass on complete synthetic:  true
real external FDTD data present:      false
real BEM/FDTD comparison ready:       false
3D validation claim ready:            false
local 3D FDTD launch ready:           false
GPU/HPC ready:                        false
```

## Interpretation

The run `104` gate is not over-strict in a way that prevents success: a complete
inbox with the required two frequency-bin files, 124 rows per file, 12-column
schema, filled component cells, a 12-field metadata ledger, and matching file
hashes passes all checks.

This does not remove the real blocker. The real run `103` inbox still lacks
real external target/background frequency-bin CSVs and a completed metadata
ledger.

## Decision

Keep real BEM/FDTD comparison, 3D validation, local 3D launch, and GPU/HPC
blocked until run `104` passes on real external FDTD returns in the run `103`
inbox.

## Milestone Snapshot

This is a result-driven BEM milestone. It froze:

```text
run_project_core_bem_3d_external_fdtd_return_inbox_preflight_smoke.py
sha256: abbe16b093d5f81db4826e9f83c4745c7de710e93b9debab547ff34cc427e31d

test_project_core_bem_3d_external_fdtd_return_inbox_preflight_smoke.py
sha256: 6d8aa7d6202f9e9683cf89199c6e01b052c80f51c877e3fd9cf26648a668b53c
```

Subsequent BEM 3D return-intake experiments should start from a duplicated
run-specific script.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_external_fdtd_return_inbox_preflight_smoke.py
3 passed
```

Figure check:

```text
project_core_bem_3d_external_fdtd_return_inbox_preflight.png
1924x772, dynamic range=255
```

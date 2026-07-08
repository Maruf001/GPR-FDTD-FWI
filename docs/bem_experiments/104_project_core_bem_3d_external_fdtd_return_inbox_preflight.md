# BEM Experiment 104: External FDTD Return Inbox Preflight

Date: 2026-06-25

## Purpose

Make the run `103` external-FDTD return inbox executable as an acceptance gate
before returned files are installed into the older machine-gate return root.

This run does not create placeholder target/background data and does not launch
BEM/FDTD comparison, 3D validation, local 3D FDTD, GPU/HPC work, field FWI, or
neural-network training.

## Output

```text
outputs/bem_experiments/104_project_core_bem_3d_external_fdtd_return_inbox_preflight
```

Key artifacts:

```text
data/project_core_bem_3d_external_fdtd_return_inbox_preflight.csv
data/project_core_bem_3d_external_fdtd_return_inbox_preflight_summary.json
docs/PROJECT_CORE_BEM_3D_EXTERNAL_FDTD_RETURN_INBOX_PREFLIGHT.md
figures/project_core_bem_3d_external_fdtd_return_inbox_preflight.png
scripts/run_project_core_bem_3d_external_fdtd_return_inbox_preflight.py
scripts/test_project_core_bem_3d_external_fdtd_return_inbox_preflight.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source run:                         103
preflight checks:                   18
passed checks:                      1
failed checks:                      17
blocking findings:                  17
required return files:              2
missing return files:               2
metadata fields required:           12
metadata fields missing/unfilled:   12
return inbox preflight ready:       false
real external FDTD data present:    false
real BEM/FDTD comparison ready:     false
3D validation claim ready:          false
local 3D FDTD launch ready:         false
GPU/HPC ready:                      false
```

The currently missing real return files are:

```text
outputs/bem_experiments/103_project_core_bem_3d_external_fdtd_return_inbox_layout/return_inbox/frequency_bins/project_core_bem_3d_fdtd_target_frequency_bins.csv
outputs/bem_experiments/103_project_core_bem_3d_external_fdtd_return_inbox_layout/return_inbox/frequency_bins/project_core_bem_3d_fdtd_background_frequency_bins.csv
```

The currently missing metadata ledger is:

```text
outputs/bem_experiments/103_project_core_bem_3d_external_fdtd_return_inbox_layout/return_inbox/metadata/project_core_bem_3d_fdtd_external_return_metadata.csv
```

## Interpretation

The run `103` inbox is ready as a receiving layout, but the acceptance gate now
shows the exact blocker state: both required real frequency-bin CSV files are
absent, and the completed metadata ledger is absent. Therefore no returned data
should be installed into the pending return root yet.

## Decision

Use run `104` as the executable preflight before accepting any returned
external 3D FDTD data. Keep BEM/FDTD comparison, 3D validation, local 3D FDTD
launch, and GPU/HPC blocked until this gate passes on real returned files.

## Milestone Snapshot

This is a result-driven BEM milestone. It froze:

```text
run_project_core_bem_3d_external_fdtd_return_inbox_preflight.py
sha256: 10bc3f2dd783a40bd650e36a88de886f78bd6b554584b8909257f05627473d5f

test_project_core_bem_3d_external_fdtd_return_inbox_preflight.py
sha256: 82223789449d08228892b43b367eb6b097996b8095face934a0f03130efc058b
```

Subsequent BEM 3D return-intake experiments should start from a duplicated
run-specific script.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_external_fdtd_return_inbox_preflight.py
4 passed
```

Figure check:

```text
project_core_bem_3d_external_fdtd_return_inbox_preflight.png
1924x772, dynamic range=255
```

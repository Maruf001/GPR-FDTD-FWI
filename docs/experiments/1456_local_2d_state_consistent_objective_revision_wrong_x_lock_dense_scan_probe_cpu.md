# Experiment 1456: Wrong-X Lock Dense-Scan Probe

Date: 2026-06-28

## Purpose

Test whether adding scan positions around the ambiguous x=187-190 mm region
repairs the wrong-x lock cases from runs `1453-1455`.

This is a bounded CPU probe with two wrong-lock perturbations and one
correct-state control. It does not launch GPU work, transfer to field evidence,
run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1456_local_2d_state_consistent_objective_revision_wrong_x_lock_dense_scan_probe_cpu
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_wrong_x_lock_dense_scan_objective_rows.csv
data/local_2d_state_consistent_objective_revision_wrong_x_lock_dense_scan_policy_rows.csv
data/local_2d_state_consistent_objective_revision_wrong_x_lock_dense_scan_design_rows.csv
data/local_2d_state_consistent_objective_revision_wrong_x_lock_dense_scan_probe_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_expanded_window_radius_bracket.png
figures/local_2d_state_consistent_objective_revision_wrong_x_lock_dense_scan_probe.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_WRONG_X_LOCK_DENSE_SCAN_PROBE.md
scripts/run_local_2d_state_consistent_objective_revision_wrong_x_lock_dense_scan_probe_cpu.py
scripts/test_local_2d_state_consistent_objective_revision_wrong_x_lock_dense_scan_probe_cpu.py
scripts/script_snapshot_manifest.json
```

## Result

```text
probe perturbations:                  3
objective selection rows:            18
scan positions:                       8
all-objectives-truth cases:           1
wrong-lock cases fully resolved:      0
wrong-lock cases reduced to veryhigh: 1
wrong-lock all-objective failures:    1
dense scan resolves all wrong locks:  false
dense scan partial reduction:         true
dense scan probe ready:               false
drop-veryhigh supported:              false
majority-vote supported:              false
promote revised objective now:        false
physical claim ready:                 false
GPU work ready:                       false
field transfer ready:                 false
field FWI ready:                      false
3D/HPC ready:                         false
elapsed seconds:                      250.676
```

Dense scan positions:

```text
50, 146, 178, 190, 202, 250, 346, 450 mm
```

Outcome:

| Perturbation | Outcome |
| --- | --- |
| correct state | all six objectives select truth |
| far radius -1.80 mm | reduced from all-objective wrong lock to `veryhigh`-only failure |
| near +1.90 mm plus far -1.60 mm | remains an all-objective wrong-x failure |

## Interpretation

The dense-scan probe partially reduces the wrong-lock failure: the far-radius
case becomes a `veryhigh`-only failure, but the combined near/far perturbation
remains an all-objective wrong-x failure.

## Decision

Use run `1456` as a bounded local 2D dense-scan probe only. Do not promote
broad-radius, physical-transfer, GPU, field-FWI, or 3D/HPC claims from this
local branch.

## Validation

Focused setup test:

```text
tests/test_local_2d_state_consistent_objective_revision_wrong_x_lock_dense_scan_probe_cpu.py
3 passed
```

Figure validation:

```text
local_2d_state_consistent_expanded_window_radius_bracket.png: 2459x1459, dynamic range=255
local_2d_state_consistent_objective_revision_wrong_x_lock_dense_scan_probe.png: 2826x938, dynamic range=255
```

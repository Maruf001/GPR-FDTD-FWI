# Experiment 1458: Near-Neighbor Radius-Error Threshold Probe

Date: 2026-06-28

## Purpose

Sweep near-neighbor radius error for the hard combined wrong-lock case while
keeping the far neighbor at -1.6 mm radius error.

This bounded CPU probe uses the dense scan from run `1456`, target
x-candidates at 187, 188, 189, and 190 mm, and near-neighbor radius errors of
0.0, +0.5, +1.0, +1.5, and +1.9 mm. It does not launch GPU work, transfer to
field evidence, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1458_local_2d_state_consistent_objective_revision_near_neighbor_radius_error_threshold_probe_cpu
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_neighbor_radius_error_threshold_result_rows.csv
data/local_2d_state_consistent_objective_revision_near_neighbor_radius_error_threshold_candidate_rows.csv
data/local_2d_state_consistent_objective_revision_near_neighbor_radius_error_threshold_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_near_neighbor_radius_error_threshold_probe.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_NEAR_NEIGHBOR_RADIUS_ERROR_THRESHOLD_PROBE.md
scripts/run_local_2d_state_consistent_objective_revision_near_neighbor_radius_error_threshold_probe_cpu.py
scripts/test_local_2d_state_consistent_objective_revision_near_neighbor_radius_error_threshold_probe_cpu.py
scripts/script_snapshot_manifest.json
```

## Result

```text
near-radius deltas:                  5
objective selection rows:           30
candidate rows:                    120
scan positions:                      8
target x candidates:                 4
far radius delta:                   -1.6 mm
all-objectives-truth models:         1
any-failure models:                  4
all-objective failure models:        2
last all-objectives-truth delta:     0.0 mm
first any-failure delta:             0.5 mm
first all-objective-failure delta:   1.5 mm
threshold probe ready:               true
promote revised objective now:       false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
elapsed seconds:                     184.003
```

Outcome:

| Near-neighbor radius error | Outcome |
| ---: | --- |
| +0.0 mm | all six objectives select truth x=190 mm |
| +0.5 mm | base and highband select truth; late, late-high, veryhigh, and early-high select x=187 mm |
| +1.0 mm | same partial-failure pattern as +0.5 mm |
| +1.5 mm | all six objectives select x=187 mm |
| +1.9 mm | all six objectives select x=187 mm |

## Interpretation

The local mechanism is threshold-like. With the far neighbor held at -1.6 mm
radius error, the combined case is stable only when the near-neighbor radius is
correct. A +0.5 mm near-neighbor radius error already breaks four objectives,
and a +1.5 mm error produces the all-objective wrong-x lock.

## Decision

Use run `1458` as the local near-neighbor radius-error threshold probe. Keep
broad-radius, physical-transfer, GPU, field-FWI, and 3D/HPC claims blocked
until this local mechanism is validated more broadly.

## Validation

Focused setup test:

```text
tests/test_local_2d_state_consistent_objective_revision_near_neighbor_radius_error_threshold_probe_cpu.py
3 passed
```

Figure validation:

```text
2427x1476, dynamic range=255
```

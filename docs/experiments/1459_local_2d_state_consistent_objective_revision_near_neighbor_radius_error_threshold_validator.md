# Experiment 1459: Near-Neighbor Radius-Error Threshold Validator

Date: 2026-06-28

## Purpose

Validate the saved run `1458` near-neighbor radius-error threshold result from
artifacts.

This run does not run FDTD, launch GPU work, transfer to field evidence, run
field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1459_local_2d_state_consistent_objective_revision_near_neighbor_radius_error_threshold_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_neighbor_radius_error_threshold_validator_checks.csv
data/local_2d_state_consistent_objective_revision_near_neighbor_radius_error_threshold_validator_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_near_neighbor_radius_error_threshold_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_NEAR_NEIGHBOR_RADIUS_ERROR_THRESHOLD_VALIDATOR.md
scripts/run_local_2d_state_consistent_objective_revision_near_neighbor_radius_error_threshold_validator.py
scripts/test_local_2d_state_consistent_objective_revision_near_neighbor_radius_error_threshold_validator.py
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                   7
passed checks:                       7
failed checks:                       0
validation ready:                    true
last all-truth delta:                0.0 mm
first any-failure delta:             0.5 mm
first all-objective-failure delta:   1.5 mm
promote revised objective now:       false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

Validated checks:

| Check | Result |
| --- | --- |
| source policy and counts | pass |
| threshold summary values | pass |
| failure counts by delta | pass |
| taxonomy counts | pass |
| downstream states blocked | pass |
| figure validation present | pass |
| script snapshots present | pass |

## Interpretation

The saved threshold result validates: +0.0 mm near-neighbor radius error passes
all objectives, +0.5 mm starts failures, and +1.5 mm starts all-objective
failure.

## Decision

Use run `1459` as the validator for the local near-neighbor threshold result.
Keep broad-radius, physical-transfer, GPU, field-FWI, and 3D/HPC claims
blocked.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_near_neighbor_radius_error_threshold_validator.py
3 passed
```

Figure validation:

```text
2861x860, dynamic range=255
```

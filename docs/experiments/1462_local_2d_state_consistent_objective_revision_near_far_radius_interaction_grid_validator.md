# Experiment 1462: Near/Far Radius-Error Interaction Grid Validator

Date: 2026-06-28

## Purpose

Validate the saved run `1461` near/far radius-error interaction grid result
from artifacts.

This run does not run FDTD, launch GPU work, transfer to field evidence, run
field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1462_local_2d_state_consistent_objective_revision_near_far_radius_interaction_grid_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_radius_interaction_grid_validator_checks.csv
data/local_2d_state_consistent_objective_revision_near_far_radius_interaction_grid_validator_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_near_far_radius_interaction_grid_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_NEAR_FAR_RADIUS_INTERACTION_GRID_VALIDATOR.md
scripts/run_local_2d_state_consistent_objective_revision_near_far_radius_interaction_grid_validator.py
scripts/test_local_2d_state_consistent_objective_revision_near_far_radius_interaction_grid_validator.py
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                  7
passed checks:                      7
failed checks:                      0
validation ready:                   true
first any-failure by far delta:     {0.0: 1.5, -0.8: 0.5, -1.6: 0.5}
first all-failure by far delta:     {0.0: 1.5, -0.8: 1.5, -1.6: 1.5}
all-objectives-truth models:        5
any-failure models:                 10
all-objective failure models:       6
promote revised objective now:      false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

Validated checks:

| Check | Result |
| --- | --- |
| source policy and counts | pass |
| failure grid counts | pass |
| near thresholds by far delta | pass |
| taxonomy counts | pass |
| downstream states blocked | pass |
| figure validation present | pass |
| script snapshots present | pass |

## Interpretation

The saved near/far interaction grid validates: far-neighbor radius error shifts
partial failures earlier, while all-objective wrong-lock failure remains fixed
at near +1.5 mm across the tested far-radius settings.

## Decision

Use run `1462` as the validator for the local near/far radius-error interaction
result. Keep broad-radius, physical-transfer, GPU, field-FWI, and 3D/HPC claims
blocked.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_radius_interaction_grid_validator.py
3 passed
```

Figure validation:

```text
3401x871, dynamic range=255
```

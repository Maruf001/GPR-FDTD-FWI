# Experiment 1467: Near/Far Interaction Generalization Design Validator

Date: 2026-06-28

## Purpose

Validate the saved run `1466` near/far interaction generalization design packet
from artifacts.

This run uses saved artifacts only. It does not run new FDTD simulations,
launch GPU work, transfer to field evidence, run field FWI, or start 3D/HPC
work.

## Output

```text
outputs/experiments/1467_local_2d_state_consistent_objective_revision_near_far_interaction_generalization_design_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_interaction_generalization_design_validator_checks.csv
data/local_2d_state_consistent_objective_revision_near_far_interaction_generalization_design_validator_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_near_far_interaction_generalization_design_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_NEAR_FAR_INTERACTION_GENERALIZATION_DESIGN_VALIDATOR.md
scripts/run_local_2d_state_consistent_objective_revision_near_far_interaction_generalization_design_validator.py
scripts/test_local_2d_state_consistent_objective_revision_near_far_interaction_generalization_design_validator.py
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:              7
passed checks:                  7
failed checks:                  0
validation ready:               true
design cases:                   8
design axes:                    5
requires new CPU sweep cases:   8
execute now cases:              0
broad radius promoted:          false
physical claim ready:           false
GPU work ready:                 false
field transfer ready:           false
field FWI ready:                false
3D/HPC ready:                   false
```

Validated checks:

| Check | Result |
| --- | --- |
| source policy and counts | pass |
| design axes are independent | pass |
| all cases require future CPU and do not execute now | pass |
| acceptance checks passed | pass |
| downstream states blocked | pass |
| figure validation present | pass |
| script snapshots present | pass |

## Interpretation

The saved generalization design validates: eight future CPU sweeps cover five
independent axes, and no GPU, field, FWI, or 3D/HPC work is requested now.

## Decision

Use run `1467` as the validator for the near/far interaction generalization
design packet.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_interaction_generalization_design_validator.py
3 passed
```

Figure validation:

```text
3365x917, dynamic range=255
```

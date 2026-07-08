# Experiment 1469: Near/Far Position Generalization Validator

Date: 2026-06-28

## Purpose

Validate the saved run `1468` target-position generalization probe from its
artifacts. This run checks that the first executed generalization result is
internally consistent before the branch is used to update the claim boundary.

This is an artifact-only validator. It does not run new FDTD simulations, GPU
work, field transfer, field FWI, neural-network training, or 3D/HPC work.

## Output

```text
outputs/experiments/1469_local_2d_state_consistent_objective_revision_near_far_position_generalization_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_position_generalization_validation_checks.csv
data/local_2d_state_consistent_objective_revision_near_far_position_generalization_validator_summary.json
figures/local_2d_state_consistent_objective_revision_near_far_position_generalization_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_NEAR_FAR_POSITION_GENERALIZATION_VALIDATOR.md
```

## Result

```text
validation checks:                 7
passed checks:                     7
failed checks:                     0
validation ready:                  true
position shifts:                   3
grid models:                       45
objective selection rows:          270
candidate rows:                    1080
all-objective failure models:      6
translated all-objective failures: false
broad radius promoted:             false
physical claim ready:              false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

The validator confirms the exact position-by-near-by-far failure cube from run
`1468`.

## Interpretation

Run `1468` is internally consistent. The zero-shift slice preserves the severe
local all-objective failure boundary from run `1461`, while the translated
-20 mm and +20 mm slices have partial failures but no all-objective failure
models.

This makes the claim boundary stricter: the severe near/far all-objective
failure is aperture-position dependent in the tested configuration. It is not a
position-invariant rule.

## Decision

Use runs `1468-1469` as the first guarded target-position generalization block.
Do not promote broad-radius tolerance, physical-transfer, GPU, field-FWI, or
3D/HPC claims from it.

Next defensible 2D work is another independent generalization axis, most likely
target depth or acquisition offset, using a new duplicated run script.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_position_generalization_probe_cpu.py
tests/test_local_2d_state_consistent_objective_revision_near_far_position_generalization_validator.py

8 passed
```

Figure validation:

```text
3359x1458, dynamic range=255
```

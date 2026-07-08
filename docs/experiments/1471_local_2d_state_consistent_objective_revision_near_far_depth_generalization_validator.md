# Experiment 1471: Near/Far Depth Generalization Validator

Date: 2026-06-28

## Purpose

Validate the saved run `1470` target-depth generalization probe from artifacts.
This validator checks the exact depth-by-near-by-far failure cube, threshold
summaries, figure output, script snapshots, and blocked downstream states.

This is an artifact-only validator. It does not run new FDTD simulations, GPU
work, field transfer, field FWI, neural-network training, or 3D/HPC work.

## Output

```text
outputs/experiments/1471_local_2d_state_consistent_objective_revision_near_far_depth_generalization_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_depth_generalization_validation_checks.csv
data/local_2d_state_consistent_objective_revision_near_far_depth_generalization_validator_summary.json
figures/local_2d_state_consistent_objective_revision_near_far_depth_generalization_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_NEAR_FAR_DEPTH_GENERALIZATION_VALIDATOR.md
```

## Result

```text
validation checks:              7
passed checks:                  7
failed checks:                  0
validation ready:               true
depth shifts:                   3
grid models:                    45
objective selection rows:       270
candidate rows:                 1080
all-objective failure models:   10
shallower depth failures:       0
deeper all-objective failures:  4
broad radius promoted:          false
physical claim ready:           false
GPU work ready:                 false
field transfer ready:           false
field FWI ready:                false
3D/HPC ready:                   false
```

## Interpretation

Run `1470` is internally consistent. The baseline depth slice preserves the
severe local all-objective failure boundary. The shallower slice has no
failures in the tested grid. The deeper slice keeps all-objective failures only
when far-radius error is present.

The near/far failure mechanism is therefore depth-dependent in this tested
setup. This complements the run `1468-1469` position result: the mechanism is
real locally, but its severity changes with geometry and acquisition context.

## Decision

Use runs `1470-1471` as the guarded target-depth generalization block. Do not
promote broad-radius tolerance, physical-transfer, GPU, field-FWI, or 3D/HPC
claims from it.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_depth_generalization_probe_cpu.py
tests/test_local_2d_state_consistent_objective_revision_near_far_depth_generalization_validator.py

8 passed
```

Figure validation:

```text
3359x1458, dynamic range=255
```

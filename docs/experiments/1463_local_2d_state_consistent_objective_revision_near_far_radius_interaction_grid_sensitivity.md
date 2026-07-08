# Experiment 1463: Near/Far Radius-Error Interaction Grid Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `1462` validator for the saved run `1461` near/far
radius-error interaction grid.

This is an artifact-only sensitivity run. It mutates saved result rows,
candidate rows, summary values, figure metadata, and script snapshots in
memory. It does not run new FDTD simulations, launch GPU work, transfer to field
evidence, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1463_local_2d_state_consistent_objective_revision_near_far_radius_interaction_grid_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_far_radius_interaction_grid_sensitivity_scenarios.csv
data/local_2d_state_consistent_objective_revision_near_far_radius_interaction_grid_sensitivity_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_near_far_radius_interaction_grid_sensitivity.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_NEAR_FAR_RADIUS_INTERACTION_GRID_SENSITIVITY.md
scripts/run_local_2d_state_consistent_objective_revision_near_far_radius_interaction_grid_sensitivity.py
scripts/test_local_2d_state_consistent_objective_revision_near_far_radius_interaction_grid_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                         15
expected pass scenarios:           1
observed pass scenarios:           1
expected failure scenarios:        14
observed failure scenarios:        14
unexpected outcomes:               0
sensitivity ready:                 true
exact run 1461 accepted:           true
damaged variants rejected:         true
promote revised objective now:     false
broad radius promoted:             false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

The damaged variants cover row-count drift, summary-count drift, failure-grid
drift, threshold drift, taxonomy drift, downstream promotion, figure drift, and
script-snapshot drift.

## Interpretation

The interaction-grid validator accepts the exact run `1461` result and rejects
all damaged variants tested here. This guards the result that far-neighbor
radius error shifts partial failures earlier while all-objective wrong-lock
failure stays fixed at near +1.5 mm across the tested far-radius settings.

## Decision

Use runs `1461-1463` as the guarded local near/far radius-error interaction
block. The result remains local mechanism evidence only; broad-radius,
physical-transfer, GPU, field-FWI, and 3D/HPC claims remain blocked.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_near_far_radius_interaction_grid_sensitivity.py
3 passed
```

Figure validation:

```text
3491x893, dynamic range=255
```

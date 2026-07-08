# Experiment 1460: Near-Neighbor Radius-Error Threshold Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `1459` validator for the saved run `1458`
near-neighbor radius-error threshold result.

This is an artifact-only sensitivity run. It mutates saved tables and metadata
in memory. It does not run new FDTD simulations, launch GPU work, transfer to
field evidence, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1460_local_2d_state_consistent_objective_revision_near_neighbor_radius_error_threshold_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_near_neighbor_radius_error_threshold_sensitivity_scenarios.csv
data/local_2d_state_consistent_objective_revision_near_neighbor_radius_error_threshold_sensitivity_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_near_neighbor_radius_error_threshold_sensitivity.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_NEAR_NEIGHBOR_RADIUS_ERROR_THRESHOLD_SENSITIVITY.md
scripts/run_local_2d_state_consistent_objective_revision_near_neighbor_radius_error_threshold_sensitivity.py
scripts/test_local_2d_state_consistent_objective_revision_near_neighbor_radius_error_threshold_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                         16
expected pass scenarios:           1
observed pass scenarios:           1
expected failure scenarios:        15
observed failure scenarios:        15
unexpected outcomes:               0
sensitivity ready:                 true
exact run 1458 accepted:           true
damaged variants rejected:         true
promote revised objective now:     false
broad radius promoted:             false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

The damaged variants cover source-count drift, threshold-value drift,
failure-count drift, taxonomy drift, false downstream promotion, figure drift,
and missing script snapshots.

## Interpretation

The near-neighbor radius-error threshold result is now guarded against common
artifact drift. The exact run `1458` threshold artifact passes, while every
damaged variant fails as expected.

This does not broaden the scientific claim. It strengthens the local evidence
that the hard wrong-lock case has a threshold-like near-neighbor radius-error
mechanism under the tested dense-scan setup.

## Decision

Use runs `1458-1460` as the guarded local near-neighbor radius-error threshold
block. The result identifies a local mechanism but does not promote
broad-radius, physical-transfer, GPU, field-FWI, or 3D/HPC claims.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_near_neighbor_radius_error_threshold_sensitivity.py
3 passed
```

Figure validation:

```text
3491x895, dynamic range=255
```

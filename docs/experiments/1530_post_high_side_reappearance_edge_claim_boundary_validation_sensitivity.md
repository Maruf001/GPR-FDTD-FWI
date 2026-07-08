# Experiment 1530: Post High-Side Reappearance Edge Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1529` validator for the saved run `1528` local 2D claim
boundary.

This run uses controlled damaged variants to check that the validator accepts
the exact saved boundary and rejects changes that would alter the result. It
does not run new FDTD simulations, launch GPU work, transfer to field evidence,
run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1530_local_2d_state_consistent_objective_revision_post_high_side_reappearance_edge_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_high_side_reappearance_edge_claim_boundary_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_post_high_side_reappearance_edge_claim_boundary_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_post_high_side_reappearance_edge_claim_boundary_validation_sensitivity.png
scripts/
```

## Result

```text
scenarios:                          19
expected pass:                      1
observed pass:                      1
expected failures:                  18
observed failures:                  18
unexpected outcomes:                0
sensitivity ready:                  true
accepts exact run 1528:             true
rejects damaged variants:           true
first reappeared far -0.8 offset:   45.015625 mm
first reappeared far -1.6 offset:   45.015625 mm
larger-offset safety claim ready:   false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

## Interpretation

The validator accepts the exact run `1528` boundary and rejects controlled
damaged variants for claim-count drift, high-side row drift, edge row drift,
45.015625 mm metric drift, false stability, monotonic safety promotion,
blocked-row drift, downstream promotion, figure drift, and script-snapshot
drift.

## Decision

Use runs `1528-1530` as the guarded post-high-side reappearance-edge local 2D
claim-boundary block. Keep broad physical, GPU, field-transfer, field-FWI, and
3D/HPC claims blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_high_side_reappearance_edge_claim_boundary_validation_sensitivity.py
3 passed
```

Figure validation:

```text
3617x922, dynamic range=255
```

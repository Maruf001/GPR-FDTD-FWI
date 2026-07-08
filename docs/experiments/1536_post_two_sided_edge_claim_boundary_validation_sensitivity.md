# Experiment 1536: Post Two-Sided Edge Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1535` validator for the saved run `1534` two-sided edge
claim boundary.

This run checks that the validator accepts the exact run `1534` artifacts and
rejects controlled damaged variants for source identity drift, claim-count
drift, high-side row drift, low-side row drift, low-side failure drift,
suppression drift, reappearance drift, false stability, broad-safety promotion,
blocked-row drift, downstream promotion, figure drift, and script-snapshot
drift.

## Output

```text
outputs/experiments/1536_local_2d_state_consistent_objective_revision_post_two_sided_edge_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_two_sided_edge_claim_boundary_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_post_two_sided_edge_claim_boundary_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_post_two_sided_edge_claim_boundary_validation_sensitivity.png
scripts/
```

## Result

```text
scenarios:                          22
expected pass:                      1
observed pass:                      1
expected failures:                  21
observed failures:                  21
unexpected outcomes:                0
sensitivity ready:                  true
accepts exact run 1534:             true
rejects damaged variants:           true
last failed below 45:               44.992188 mm
first suppression:                  45.0 mm
first reappearance above 45:        45.015625 mm
broad acquisition safety ready:     false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

## Interpretation

The run `1535` validator accepts the exact run `1534` boundary and rejects
controlled damaged variants. This guards the two-sided edge conclusion:
negative far-radius failures persist immediately below 45.0 mm, suppress at
45.0 mm, and reappear immediately above 45.0 mm.

## Decision

Use runs `1534-1536` as the guarded post-two-sided-edge local 2D claim-boundary
block. Keep broad physical, GPU, field-transfer, field-FWI, and 3D/HPC claims
blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_two_sided_edge_claim_boundary_validation_sensitivity.py
3 passed
```

Figure validation:

```text
3797x916, dynamic range=255
```

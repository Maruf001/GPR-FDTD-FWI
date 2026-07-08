# Experiment 1542: Post Width Audit Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1541` validator for the saved run `1540`
post-width-audit claim boundary.

This run checks that the validator accepts the exact run `1540` artifacts and
rejects controlled damaged variants for claim drift, width-metric drift, false
wide-window promotion, downstream promotion, figure drift, and script-snapshot
drift.

## Output

```text
outputs/experiments/1542_local_2d_state_consistent_objective_revision_post_width_audit_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_width_audit_claim_boundary_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_post_width_audit_claim_boundary_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_post_width_audit_claim_boundary_validation_sensitivity.png
scripts/
```

## Result

```text
scenarios:                          16
expected pass:                      1
observed pass:                      1
expected failures:                  15
observed failures:                  15
unexpected outcomes:                0
sensitivity ready:                  true
accepts exact run 1540:             true
rejects damaged variants:           true
lower failure-to-suppression gap:   0.007812 mm
suppression-to-upper-failure gap:   0.015625 mm
failure-to-failure bracket span:    0.023437 mm
narrow sampled window ready:        true
wide suppression-window ready:      false
broad acquisition safety ready:     false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
3D/HPC ready:                       false
```

## Interpretation

The run `1541` validator accepts the exact run `1540` claim boundary and
rejects controlled damaged variants. This guards the updated claim boundary and
keeps wider acquisition-safety claims blocked.

## Decision

Use runs `1540-1542` as the guarded post-width-audit local 2D claim-boundary
block. Keep wide-window, monotonic acquisition, physical, GPU, field, and 3D
claims blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_width_audit_claim_boundary_validation_sensitivity.py
3 passed
```

Figure validation:

```text
3761x899, dynamic range=255
```

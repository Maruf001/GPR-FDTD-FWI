# Experiment 1524: Post High-Side Stability Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1523` post-high-side claim-boundary validator with
controlled damaged variants.

This run checks that the validator accepts the exact run `1522` boundary and
rejects damaged variants covering claim-count drift, high-side row drift,
missing `45.125 mm` evidence, false stability, monotonic safety promotion,
blocked-row drift, downstream promotion, figure drift, and script-snapshot
drift.

It does not run FDTD, launch GPU work, transfer to field evidence, run field
FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1524_local_2d_state_consistent_objective_revision_post_high_side_stability_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_high_side_stability_claim_boundary_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_post_high_side_stability_claim_boundary_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_post_high_side_stability_claim_boundary_validation_sensitivity.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_POST_HIGH_SIDE_STABILITY_CLAIM_BOUNDARY_VALIDATION_SENSITIVITY.md
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
accepts exact run 1522:             true
rejects damaged variants:           true
first reappeared far -0.8 offset:   45.125 mm
first reappeared far -1.6 offset:   45.125 mm
larger-offset safety claim ready:   false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

## Interpretation

The run `1523` validator accepts the exact run `1522` boundary and rejects
controlled damaged variants. This protects the high-side correction: the
`45.0 mm` sampled suppression point cannot be turned into a monotonic
larger-offset safety claim.

## Decision

Use runs `1522-1524` as the guarded post-high-side local 2D claim-boundary
block. Keep broad physical, GPU, field-transfer, field-FWI, and 3D/HPC claims
blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_high_side_stability_claim_boundary_validation_sensitivity.py
3 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_post_high_side_stability_claim_boundary_validation_sensitivity.py: pass
tests/test_local_2d_state_consistent_objective_revision_post_high_side_stability_claim_boundary_validation_sensitivity.py: pass
```

Figure validation:

```text
3509x913, dynamic range=255
```

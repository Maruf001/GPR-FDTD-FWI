# Experiment 1512: Post Crossing Estimate Claim Boundary Validation Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `1511` claim-boundary validator with controlled damaged
variants.

This run checks that the validator accepts the exact run `1510` claim boundary
and rejects damaged variants covering claim counts, crossing-claim row drift,
crossing metrics, boundary readiness, blocked-claim drift, downstream
promotion, figure validation, and script snapshots.

It does not run FDTD, launch GPU work, transfer to field evidence, run field
FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1512_local_2d_state_consistent_objective_revision_post_crossing_estimate_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_crossing_estimate_claim_boundary_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_post_crossing_estimate_claim_boundary_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_post_crossing_estimate_claim_boundary_validation_sensitivity.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_POST_CROSSING_ESTIMATE_CLAIM_BOUNDARY_VALIDATION_SENSITIVITY.md
scripts/
```

## Result

```text
scenarios:                  18
expected pass:              1
observed pass:              1
expected failures:          17
observed failures:          17
unexpected outcomes:        0
sensitivity ready:          true
accepts exact run 1510:     true
rejects damaged variants:   true
physical claim ready:       false
GPU work ready:             false
field transfer ready:       false
field FWI ready:            false
3D/HPC ready:               false
```

## Interpretation

The validator accepts the exact run `1510` claim boundary and rejects damaged
variants covering claim counts, crossing-claim row drift, crossing metrics,
boundary readiness, blocked-claim drift, downstream promotion, figure
validation, and script snapshots.

## Decision

Use runs `1510-1512` as the guarded post-crossing local 2D claim-boundary
block. The boundary remains local synthetic mechanism evidence and does not
promote physical, GPU, field, or 3D claims.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_post_crossing_estimate_claim_boundary_validation_sensitivity.py
3 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_post_crossing_estimate_claim_boundary_validation_sensitivity.py: pass
tests/test_local_2d_state_consistent_objective_revision_post_crossing_estimate_claim_boundary_validation_sensitivity.py: pass
```

Figure validation:

```text
3545x904, dynamic range=255
```

# Experiment 1511: Post Crossing Estimate Claim Boundary Validator

Date: 2026-06-28

## Purpose

Validate the saved run `1510` claim boundary from artifacts.

This run checks claim counts, the new crossing-estimate claim row, crossing
metrics, blocked claim rows, downstream blocked states, figure output, and
script snapshots.

It does not run FDTD, launch GPU work, transfer to field evidence, run field
FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1511_local_2d_state_consistent_objective_revision_post_crossing_estimate_claim_boundary_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_crossing_estimate_claim_boundary_validator_checks.csv
data/local_2d_state_consistent_objective_revision_post_crossing_estimate_claim_boundary_validator_summary.json
figures/local_2d_state_consistent_objective_revision_post_crossing_estimate_claim_boundary_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_POST_CROSSING_ESTIMATE_CLAIM_BOUNDARY_VALIDATOR.md
scripts/
```

## Result

```text
validation checks:              7
passed checks:                  7
failed checks:                  0
validation ready:               true
claims:                         16
guarded claims:                 13
blocked claims:                 3
mean crossing offset:           44.620737 mm
minimum clearance from 45 mm:   0.379263 mm
near-45 mm clearance only:      true
physical claim ready:           false
GPU work ready:                 false
field transfer ready:           false
field FWI ready:                false
3D/HPC ready:                   false
```

## Interpretation

The saved post-crossing claim boundary is internally consistent: the new
crossing-estimate claim is guarded, blocked downstream claims remain blocked,
and the narrow `45 mm` clearance metrics are stable.

## Decision

Use run `1511` as the validator for the run `1510` claim boundary. Sensitivity
hardening remains required before treating the boundary as fully guarded.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_post_crossing_estimate_claim_boundary_validator.py
3 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_post_crossing_estimate_claim_boundary_validator.py: pass
tests/test_local_2d_state_consistent_objective_revision_post_crossing_estimate_claim_boundary_validator.py: pass
```

Figure validation:

```text
3437x893, dynamic range=255
```

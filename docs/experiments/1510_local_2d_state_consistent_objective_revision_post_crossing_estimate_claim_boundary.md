# Experiment 1510: Post Crossing Estimate Claim Boundary

Date: 2026-06-28

## Purpose

Integrate the guarded fine-transition crossing estimate into the local 2D claim
boundary.

This run uses saved artifacts only. It does not run new FDTD simulations,
launch GPU work, transfer to field evidence, run field FWI, or start 3D/HPC
work.

## Output

```text
outputs/experiments/1510_local_2d_state_consistent_objective_revision_post_crossing_estimate_claim_boundary
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_crossing_estimate_claim_boundary_claim_rows.csv
data/local_2d_state_consistent_objective_revision_post_crossing_estimate_claim_boundary_summary.json
figures/local_2d_state_consistent_objective_revision_post_crossing_estimate_claim_boundary.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_POST_CROSSING_ESTIMATE_CLAIM_BOUNDARY.md
scripts/
```

## Result

```text
claims:                         16
guarded claims:                 13
blocked claims:                 3
boundary ready:                 true
crossing sensitivity ready:     true
mean crossing offset:           44.620737 mm
minimum clearance from 45 mm:   0.379263 mm
near-45 mm clearance only:      true
broad radius promoted:          false
physical claim ready:           false
GPU work ready:                 false
field transfer ready:           false
field FWI ready:                false
3D/HPC ready:                   false
```

## Interpretation

The local 2D near/far claim boundary now includes the guarded crossing estimate:
the zero-margin crossing is about `44.621 mm` and the `45 mm` layout has only
about `0.379 mm` local clearance.

## Decision

Use run `1510` as the current local 2D near/far claim boundary after
crossing-estimate integration. Keep broad physical, GPU, field-transfer,
field-FWI, and 3D/HPC claims blocked.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_post_crossing_estimate_claim_boundary.py
3 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_post_crossing_estimate_claim_boundary.py: pass
tests/test_local_2d_state_consistent_objective_revision_post_crossing_estimate_claim_boundary.py: pass
```

Figure validation:

```text
3761x952, dynamic range=255
```

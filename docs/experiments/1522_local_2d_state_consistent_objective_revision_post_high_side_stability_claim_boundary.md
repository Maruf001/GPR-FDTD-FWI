# Experiment 1522: Post High-Side Stability Claim Boundary

Date: 2026-06-29

## Purpose

Integrate the guarded high-side correction from runs `1519-1521` into the
local 2D claim boundary.

This run uses saved artifacts only. It does not run new FDTD simulations,
launch GPU work, transfer to field evidence, run field FWI, or start 3D/HPC
work.

## Output

```text
outputs/experiments/1522_local_2d_state_consistent_objective_revision_post_high_side_stability_claim_boundary
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_high_side_stability_claim_boundary_claim_rows.csv
data/local_2d_state_consistent_objective_revision_post_high_side_stability_claim_boundary_summary.json
figures/local_2d_state_consistent_objective_revision_post_high_side_stability_claim_boundary.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_POST_HIGH_SIDE_STABILITY_CLAIM_BOUNDARY.md
scripts/
```

## Result

```text
claims:                              18
guarded claims:                      15
blocked claims:                      3
boundary ready:                      true
high-side sensitivity ready:         true
far -0.8 first suppression:          45.0 mm
far -1.6 first suppression:          45.0 mm
far -0.8 first reappearance:         45.125 mm
far -1.6 first reappearance:         45.125 mm
high-side suppression stable -0.8:   false
high-side suppression stable -1.6:   false
larger-offset safety claim ready:    false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

## Interpretation

The high-side probe corrects the acquisition-layout interpretation. The
`45.0 mm` layout remains a sampled far-error suppression point, but failures
reappear at `45.125 mm` and persist at larger tested offsets. The evidence
therefore blocks a monotonic larger-offset safety claim.

## Decision

Use run `1522` as the current local 2D claim boundary after high-side
correction. Keep broad physical, GPU, field-transfer, field-FWI, and 3D/HPC
claims blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_high_side_stability_claim_boundary.py
3 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_post_high_side_stability_claim_boundary.py: pass
tests/test_local_2d_state_consistent_objective_revision_post_high_side_stability_claim_boundary.py: pass
```

Figure validation:

```text
3833x970, dynamic range=255
```

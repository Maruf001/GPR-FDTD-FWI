# Experiment 1528: Post High-Side Reappearance Edge Claim Boundary

Date: 2026-06-29

## Purpose

Integrate the guarded run `1525-1527` high-side reappearance-edge block into
the local 2D claim boundary.

This run uses saved artifacts only. It does not run new FDTD simulations,
launch GPU work, transfer to field evidence, run field FWI, or start 3D/HPC
work.

## Output

```text
outputs/experiments/1528_local_2d_state_consistent_objective_revision_post_high_side_reappearance_edge_claim_boundary
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_high_side_reappearance_edge_claim_boundary_claim_rows.csv
data/local_2d_state_consistent_objective_revision_post_high_side_reappearance_edge_claim_boundary_summary.json
figures/local_2d_state_consistent_objective_revision_post_high_side_reappearance_edge_claim_boundary.png
scripts/
```

## Result

```text
claim count:                         19
guarded claims:                      16
blocked claims:                      3
base claim count:                    18
base guarded claims:                 15
base blocked claims:                 3
edge probe ready:                    true
edge sensitivity ready:              true
far -0.8 first suppression:          45.0 mm
far -1.6 first suppression:          45.0 mm
far -0.8 first reappearance:         45.015625 mm
far -1.6 first reappearance:         45.015625 mm
larger-offset safety claim ready:    false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

## Interpretation

The 2D claim boundary now records that the 45.0 mm layout is a narrow sampled
suppression point. Negative far-radius failures reappear at 45.015625 mm, the
first tested point above 45.0 mm.

This sharpens, but does not reverse, the previous high-side decision: no
monotonic larger-offset acquisition safety rule is supported.

## Decision

Use run `1528` as the current local 2D claim boundary after high-side edge
correction. Keep broad physical, GPU, field-transfer, field-FWI, and 3D/HPC
claims blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_high_side_reappearance_edge_claim_boundary.py
3 passed
```

Figure validation:

```text
3833x970, dynamic range=255
```

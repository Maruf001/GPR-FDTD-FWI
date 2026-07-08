# Experiment 1534: Post Two-Sided Edge Claim Boundary

Date: 2026-06-29

## Purpose

Integrate the guarded low-side persistence-edge block from runs `1531-1533`
into the current local 2D claim boundary.

This run uses saved artifacts only. It does not run new FDTD simulations,
launch GPU work, transfer to field evidence, run field FWI, or start 3D/HPC
work.

## Output

```text
outputs/experiments/1534_local_2d_state_consistent_objective_revision_post_two_sided_edge_claim_boundary
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_two_sided_edge_claim_boundary_claim_rows.csv
data/local_2d_state_consistent_objective_revision_post_two_sided_edge_claim_boundary_summary.json
figures/local_2d_state_consistent_objective_revision_post_two_sided_edge_claim_boundary.png
scripts/
```

## Result

```text
claims:                              20
guarded claims:                      17
blocked claims:                      3
base claims:                         19
base guarded claims:                 16
base blocked claims:                 3
low-side probe ready:                true
low-side sensitivity ready:          true
far -0.8 last failed below 45:       44.992188 mm
far -1.6 last failed below 45:       44.992188 mm
far -0.8 first suppression:          45.0 mm
far -1.6 first suppression:          45.0 mm
far -0.8 first reappearance above 45:45.015625 mm
far -1.6 first reappearance above 45:45.015625 mm
failure persists below 45:           true
broad acquisition safety ready:      false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

## Interpretation

The local 2D claim boundary now records both sides of the 45.0 mm acquisition
edge. Negative far-radius failures persist at 44.992188 mm, the closest tested
point below 45.0 mm, suppress at 45.0 mm, and reappear above 45.0 mm from the
prior high-side block.

The result supports a narrow sampled suppression point at 45.0 mm. It does not
support a broad monotonic acquisition-safety rule.

## Decision

Use run `1534` as the current local 2D claim boundary after the two-sided edge
correction. Keep broad physical, GPU, field-transfer, field-FWI, and 3D/HPC
claims blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_two_sided_edge_claim_boundary.py
3 passed
```

Figure validation:

```text
3869x970, dynamic range=255
```

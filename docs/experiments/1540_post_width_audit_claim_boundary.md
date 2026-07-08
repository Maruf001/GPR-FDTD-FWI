# Experiment 1540: Post Width Audit Claim Boundary

Date: 2026-06-29

## Purpose

Integrate the guarded suppression-window width audit from runs `1537-1539` into
the current local 2D claim boundary.

This run uses saved artifacts only. It does not run FDTD simulations, launch
GPU work, transfer to field evidence, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1540_local_2d_state_consistent_objective_revision_post_width_audit_claim_boundary
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_width_audit_claim_boundary_claim_rows.csv
data/local_2d_state_consistent_objective_revision_post_width_audit_claim_boundary_summary.json
figures/local_2d_state_consistent_objective_revision_post_width_audit_claim_boundary.png
scripts/
```

## Result

```text
claims:                              21
guarded claims:                      18
blocked claims:                      3
base claims:                         20
base guarded claims:                 17
base blocked claims:                 3
width-audit sensitivity ready:       true
accepts exact run 1537:              true
rejects damaged variants:            true
lower failure-to-suppression gap:    0.007812 mm
suppression-to-upper-failure gap:    0.015625 mm
failure-to-failure bracket span:     0.023437 mm
narrow sampled window ready:         true
wide suppression-window claim ready: false
broad acquisition safety ready:      false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

## Interpretation

The local 2D claim boundary now includes the guarded width audit. The 45.0 mm
suppression point is a narrow sampled bracket, not a wide or monotonic
acquisition-safety region.

## Decision

Use run `1540` as the current local 2D claim boundary after the width audit.
Keep broad physical, GPU, field-transfer, field-FWI, and 3D/HPC claims blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_width_audit_claim_boundary.py
3 passed
```

Figure validation:

```text
3941x952, dynamic range=255
```

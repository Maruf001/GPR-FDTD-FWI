# Experiment 1537: Two-Sided Edge Suppression Window Width Audit

Date: 2026-06-29

## Purpose

Quantify the sampled bracket around the 45.0 mm suppression point from the
guarded two-sided edge claim boundary.

This run uses saved artifacts only. It does not run FDTD simulations, launch
GPU work, transfer to field evidence, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1537_local_2d_state_consistent_objective_revision_two_sided_edge_suppression_window_width_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_two_sided_edge_suppression_window_width_audit_window_rows.csv
data/local_2d_state_consistent_objective_revision_two_sided_edge_suppression_window_width_audit_summary.json
figures/local_2d_state_consistent_objective_revision_two_sided_edge_suppression_window_width_audit.png
scripts/
```

## Result

```text
source claims:                       20
source guarded claims:               17
source blocked claims:               3
last failed below 45.0 mm:           44.992188 mm
sampled suppression point:           45.0 mm
first reappeared above 45.0 mm:      45.015625 mm
lower failure-to-suppression gap:    0.007812 mm
suppression-to-upper-failure gap:    0.015625 mm
failure-to-failure bracket span:     0.023437 mm
sampled suppression points in span:  1
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

The saved two-sided edge boundary supports a narrow sampled suppression bracket
only. Failure is sampled 0.007812 mm below 45.0 mm and 0.015625 mm above 45.0
mm, so the 45.0 mm point should not be described as a wide or monotonic
acquisition-safety region.

## Decision

Use run `1537` as a quantitative width audit for the 45.0 mm sampled
suppression point. Do not promote a wide suppression-window, physical-transfer,
GPU, field, or 3D claim from this artifact.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_two_sided_edge_suppression_window_width_audit.py
3 passed
```

Figure validation:

```text
3671x928, dynamic range=255
```

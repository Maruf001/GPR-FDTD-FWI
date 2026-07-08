# BEM Experiment 677: 113-Panel Material/Geometry Transfer Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `676` validator for the 113-panel no-go and 114-panel
endpoint boundary.

The validator should accept only the exact run `675` no-go result and reject
damaged states that corrupt case or solve counts, falsely promote 113 panels,
demote the 114-panel endpoint, erase the 113-panel no-go, promote downstream
claims, damage the figure, or remove script snapshots.

## Output

```text
outputs/bem_experiments/677_scarep_2d_cpu_bem_panel113_material_geometry_transfer_audit_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel113_material_geometry_transfer_audit_validation_sensitivity_rows.csv
data/scarep_2d_cpu_bem_panel113_material_geometry_transfer_audit_validation_sensitivity_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel113_material_geometry_transfer_audit_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:              true
sensitivity cases:                   21
expected pass cases:                 1
expected fail cases:                 20
actual pass cases:                   1
actual fail cases:                   20
unexpected cases:                    0
shape damage rejected:               true
transfer-boundary damage rejected:   true
claim-promotion damage rejected:     true
113-panel transfer ready:            false
project FDTD comparison ready:       false
real 3D validation ready:            false
GPU/HPC ready:                       false
field transfer ready:                false
field FWI ready:                     false
```

The exact run `675` source passes. All damaged states fail, including source
readiness loss, case-row removal, solve-row removal, count damage, false
113-panel promotion, false 114-panel endpoint demotion, erasing the 113-panel
no-go, making the 114-panel endpoint fail, wall-ratio damage, project-FDTD
promotion, 3D promotion, GPU/HPC promotion, field-transfer promotion,
field-FWI promotion, figure damage, and missing script snapshots.

## Interpretation

Run `677` hardens the 113/114 threshold boundary. The current analytic
transfer endpoint is 114 panels for the tested variants.

## Decision

Keep 113 panels blocked as the nearest tested lower-side no-go. Keep 114
panels as the current analytic material/geometry transfer endpoint.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel113_material_geometry_transfer_audit.py
tests/test_scarep_2d_cpu_bem_panel113_material_geometry_transfer_audit_validator.py
tests/test_scarep_2d_cpu_bem_panel113_material_geometry_transfer_audit_validation_sensitivity.py

10 passed
```

Figure check:

```text
2644x890, dynamic range=255
```

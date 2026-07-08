# BEM Experiment 674: 114-Panel Material/Geometry Transfer Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `673` validator for the 114-panel material/geometry
transfer promotion.

The validator should accept only the exact run `672` transfer result and
reject damaged states that corrupt case or solve counts, demote the 114-panel
transfer, demote the 116-panel endpoint, make either panel count fail the
target, promote downstream claims, damage the figure, or remove script
snapshots.

## Output

```text
outputs/bem_experiments/674_scarep_2d_cpu_bem_panel114_material_geometry_transfer_audit_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel114_material_geometry_transfer_audit_validation_sensitivity_rows.csv
data/scarep_2d_cpu_bem_panel114_material_geometry_transfer_audit_validation_sensitivity_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel114_material_geometry_transfer_audit_validation_sensitivity.png
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
114-panel transfer ready:            true
project FDTD comparison ready:       false
real 3D validation ready:            false
GPU/HPC ready:                       false
field transfer ready:                false
field FWI ready:                     false
```

The exact run `672` source passes. All damaged states fail, including source
readiness loss, case-row removal, solve-row removal, count damage, false
114-panel demotion, false 116-panel endpoint demotion, making 114 panels fail
the target, making the 116-panel endpoint fail, wall-ratio damage,
project-FDTD promotion, 3D promotion, GPU/HPC promotion, field-transfer
promotion, field-FWI promotion, figure damage, and missing script snapshots.

## Interpretation

Run `674` hardens the 114-panel tight-margin promotion. The promotion remains
limited to the analytic material/geometry transfer variants and does not
promote FDTD, 3D, field, or GPU/HPC readiness.

## Decision

Keep 114 panels as the current analytic transfer endpoint for the tested
variants.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel114_material_geometry_transfer_audit.py
tests/test_scarep_2d_cpu_bem_panel114_material_geometry_transfer_audit_validator.py
tests/test_scarep_2d_cpu_bem_panel114_material_geometry_transfer_audit_validation_sensitivity.py

10 passed
```

Figure check:

```text
2644x890, dynamic range=255
```

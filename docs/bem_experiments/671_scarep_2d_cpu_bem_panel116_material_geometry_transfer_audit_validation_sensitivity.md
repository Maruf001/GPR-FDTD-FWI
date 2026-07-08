# BEM Experiment 671: 116-Panel Material/Geometry Transfer Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `670` validator for the 116-panel material/geometry
transfer promotion.

The validator should accept only the exact run `669` transfer result and
reject damaged states that corrupt case or solve counts, demote the 116-panel
transfer, demote the 120-panel endpoint, make either panel count fail the
target, promote downstream claims, damage the figure, or remove script
snapshots.

## Output

```text
outputs/bem_experiments/671_scarep_2d_cpu_bem_panel116_material_geometry_transfer_audit_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel116_material_geometry_transfer_audit_validation_sensitivity_rows.csv
data/scarep_2d_cpu_bem_panel116_material_geometry_transfer_audit_validation_sensitivity_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel116_material_geometry_transfer_audit_validation_sensitivity.png
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
116-panel transfer ready:            true
project FDTD comparison ready:       false
real 3D validation ready:            false
GPU/HPC ready:                       false
field transfer ready:                false
field FWI ready:                     false
```

The exact run `669` source passes. All damaged states fail, including source
readiness loss, case-row removal, solve-row removal, count damage, false
116-panel demotion, false 120-panel endpoint demotion, making 116 panels fail
the target, making the 120-panel endpoint fail, wall-ratio damage,
project-FDTD promotion, 3D promotion, GPU/HPC promotion, field-transfer
promotion, field-FWI promotion, figure damage, and missing script snapshots.

## Interpretation

Run `671` hardens the 116-panel promotion. The promotion remains limited to
the analytic material/geometry transfer variants and does not promote FDTD,
3D, field, or GPU/HPC readiness.

## Decision

Keep 116 panels as the current analytic transfer endpoint for the tested
variants.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_material_geometry_transfer_audit.py
tests/test_scarep_2d_cpu_bem_panel116_material_geometry_transfer_audit_validator.py
tests/test_scarep_2d_cpu_bem_panel116_material_geometry_transfer_audit_validation_sensitivity.py

10 passed
```

Figure check:

```text
2644x890, dynamic range=255
```

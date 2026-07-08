# BEM Experiment 665: 112-Panel Material/Geometry Transfer Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `664` validator for the 112-panel material/geometry
transfer audit.

The validator should accept only the exact run `663` near-miss result and
reject damaged states that falsely promote 112 panels, demote the 128-panel
endpoint, damage case or solve counts, promote downstream claims, damage the
figure, or remove script snapshots.

## Output

```text
outputs/bem_experiments/665_scarep_2d_cpu_bem_panel112_material_geometry_transfer_audit_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel112_material_geometry_transfer_audit_validation_sensitivity_rows.csv
data/scarep_2d_cpu_bem_panel112_material_geometry_transfer_audit_validation_sensitivity_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel112_material_geometry_transfer_audit_validation_sensitivity.png
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
112-panel transfer ready:            false
project FDTD comparison ready:       false
real 3D validation ready:            false
GPU/HPC ready:                       false
field transfer ready:                false
field FWI ready:                     false
```

The exact run `663` source passes. All damaged states fail, including source
readiness loss, case-row removal, solve-row removal, count damage, false
112-panel transfer promotion, false 128-panel endpoint demotion, erasing the
112-panel near miss, making the 128-panel endpoint fail, wall-ratio damage,
project-FDTD promotion, 3D promotion, GPU/HPC promotion, field-transfer
promotion, field-FWI promotion, figure damage, and missing script snapshots.

## Interpretation

Run `665` hardens the 112-panel near-miss result. The current evidence does
not support generalizing 112 panels across the tested material/geometry
variants.

## Decision

Keep 112-panel material/geometry transfer blocked. Test a higher intermediate
candidate before accepting 128 panels as the only transfer endpoint.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel112_material_geometry_transfer_audit.py
tests/test_scarep_2d_cpu_bem_panel112_material_geometry_transfer_audit_validator.py
tests/test_scarep_2d_cpu_bem_panel112_material_geometry_transfer_audit_validation_sensitivity.py

10 passed
```

Figure check:

```text
2644x890, dynamic range=255
```

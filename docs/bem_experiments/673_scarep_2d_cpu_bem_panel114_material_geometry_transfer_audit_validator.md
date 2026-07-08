# BEM Experiment 673: 114-Panel Material/Geometry Transfer Audit Validator

Date: 2026-06-30

## Purpose

Validate run `672`, the tight-margin 114-panel material/geometry transfer
promotion.

## Output

```text
outputs/bem_experiments/673_scarep_2d_cpu_bem_panel114_material_geometry_transfer_audit_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel114_material_geometry_transfer_audit_validator_check_rows.csv
data/scarep_2d_cpu_bem_panel114_material_geometry_transfer_audit_validator_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel114_material_geometry_transfer_audit_validator.png
scripts/
```

## Result

```text
validation checks:                     5
failed checks:                         0
variant cases:                         4
solve rows:                            4
112-panel transfer pass cases:         3
114-panel transfer pass cases:         4
114-panel transfer fail cases:         0
116-panel transfer pass cases:         4
114-panel max high-band relative L2:   0.0009848005761020824
116-panel max high-band relative L2:   0.0009506170756247567
114-panel transfer ready:              true
116-panel endpoint transfer ready:     true
project FDTD comparison ready:         false
real 3D validation ready:              false
GPU/HPC ready:                         false
field transfer ready:                  false
field FWI ready:                       false
```

Validator checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | Source transfer audit ready | pass |
| 2 | Case and solve shape preserved | pass |
| 3 | 114-panel tight-promotion boundary preserved | pass |
| 4 | Analytic-only claim boundary preserved | pass |
| 5 | Figure and scripts exist | pass |

## Interpretation

Run `673` validates 114 panels as a tight-margin analytic material/geometry
transfer endpoint. The promotion is bounded to the analytic-cylinder evidence
stream.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel114_material_geometry_transfer_audit.py
tests/test_scarep_2d_cpu_bem_panel114_material_geometry_transfer_audit_validator.py

7 passed
```

Figure check:

```text
2321x857, dynamic range=255
```

# BEM Experiment 667: 120-Panel Material/Geometry Transfer Audit Validator

Date: 2026-06-30

## Purpose

Validate run `666`, the 120-panel material/geometry transfer promotion.

## Output

```text
outputs/bem_experiments/667_scarep_2d_cpu_bem_panel120_material_geometry_transfer_audit_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel120_material_geometry_transfer_audit_validator_check_rows.csv
data/scarep_2d_cpu_bem_panel120_material_geometry_transfer_audit_validator_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel120_material_geometry_transfer_audit_validator.png
scripts/
```

## Result

```text
validation checks:                     5
failed checks:                         0
variant cases:                         4
solve rows:                            4
112-panel transfer pass cases:         3
120-panel transfer pass cases:         4
120-panel transfer fail cases:         0
128-panel high-band pass cases:        4
120-panel max high-band relative L2:   0.0008874668710960488
128-panel max high-band relative L2:   0.0007789581648464677
120-panel transfer ready:              true
128-panel endpoint transfer ready:     true
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
| 3 | 120-panel transfer promotion boundary preserved | pass |
| 4 | Analytic-only claim boundary preserved | pass |
| 5 | Figure and scripts exist | pass |

## Interpretation

Run `667` validates 120 panels as the current analytic material/geometry
transfer endpoint for the tested variants. The promotion is bounded to the
analytic-cylinder evidence stream.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel120_material_geometry_transfer_audit.py
tests/test_scarep_2d_cpu_bem_panel120_material_geometry_transfer_audit_validator.py

7 passed
```

Figure check:

```text
2321x860, dynamic range=255
```

# BEM Experiment 676: 113-Panel Material/Geometry Transfer Audit Validator

Date: 2026-06-30

## Purpose

Validate run `675`, the 113-panel tight no-go below the 114-panel transfer
endpoint.

## Output

```text
outputs/bem_experiments/676_scarep_2d_cpu_bem_panel113_material_geometry_transfer_audit_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel113_material_geometry_transfer_audit_validator_check_rows.csv
data/scarep_2d_cpu_bem_panel113_material_geometry_transfer_audit_validator_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel113_material_geometry_transfer_audit_validator.png
scripts/
```

## Result

```text
validation checks:                     5
failed checks:                         0
variant cases:                         4
solve rows:                            4
112-panel transfer pass cases:         3
113-panel transfer pass cases:         3
113-panel transfer fail cases:         1
114-panel transfer pass cases:         4
113-panel max high-band relative L2:   0.0010026008820656063
114-panel max high-band relative L2:   0.0009848005761020824
113-panel transfer ready:              false
114-panel endpoint transfer ready:     true
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
| 3 | 113-panel tight no-go boundary preserved | pass |
| 4 | Analytic-only claim boundary preserved | pass |
| 5 | Figure and scripts exist | pass |

## Interpretation

Run `676` validates 113 panels as the nearest tested lower-side no-go and 114
panels as the current analytic transfer endpoint.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel113_material_geometry_transfer_audit.py
tests/test_scarep_2d_cpu_bem_panel113_material_geometry_transfer_audit_validator.py

7 passed
```

Figure check:

```text
2321x860, dynamic range=255
```

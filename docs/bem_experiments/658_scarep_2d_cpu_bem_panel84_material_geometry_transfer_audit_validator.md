# BEM Experiment 658: 84-Panel Material/Geometry Transfer Audit Validator

Date: 2026-06-30

## Purpose

Validate run `657`, the material/geometry transfer audit for the 84-panel
analytic-cylinder policy.

## Output

```text
outputs/bem_experiments/658_scarep_2d_cpu_bem_panel84_material_geometry_transfer_audit_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel84_material_geometry_transfer_audit_validator_check_rows.csv
data/scarep_2d_cpu_bem_panel84_material_geometry_transfer_audit_validator_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel84_material_geometry_transfer_audit_validator.png
scripts/
```

## Result

```text
validation checks:                    5
failed checks:                        0
variant cases:                        4
solve rows:                           8
84-panel transfer pass cases:         2
84-panel transfer fail cases:         2
128-panel high-band pass cases:       4
84-panel max high-band relative L2:   0.0018449395379997787
128-panel max high-band relative L2:  0.0007789581648464677
84-panel transfer ready:              false
128-panel endpoint transfer ready:    true
project FDTD comparison ready:        false
real 3D validation ready:             false
GPU/HPC ready:                        false
field transfer ready:                 false
field FWI ready:                      false
```

Validator checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | Source transfer audit ready | pass |
| 2 | Case and solve shape preserved | pass |
| 3 | 84-panel transfer no-go boundary preserved | pass |
| 4 | Analytic-only claim boundary preserved | pass |
| 5 | Figure and scripts exist | pass |

## Interpretation

Run `658` confirms the run `657` result as a validated no-go for broad
84-panel transfer. The 84-panel setting remains useful as a lower-cost
baseline candidate, but the tested material/geometry variants require the
128-panel endpoint for high-frequency analytic evidence.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel84_material_geometry_transfer_audit.py
tests/test_scarep_2d_cpu_bem_panel84_material_geometry_transfer_audit_validator.py

7 passed
```

Figure check:

```text
2321x860, dynamic range=255
```

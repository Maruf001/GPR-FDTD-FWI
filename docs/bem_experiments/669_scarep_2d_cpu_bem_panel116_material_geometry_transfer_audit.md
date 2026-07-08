# BEM Experiment 669: 116-Panel Material/Geometry Transfer Audit

Date: 2026-06-30

## Purpose

Test whether 116 panels can lower the passing material/geometry transfer
endpoint below the validated 120-panel result from run `666`.

This run uses the same four analytic-cylinder material/geometry variants and
compares 116 panels against the validated 120-panel endpoint. This is
analytic-only BEM evidence; it is not a project-FDTD, 3D, field, GPU/HPC, or
field-FWI comparison.

## Output

```text
outputs/bem_experiments/669_scarep_2d_cpu_bem_panel116_material_geometry_transfer_audit
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel116_material_geometry_transfer_audit_solve_rows.csv
data/scarep_2d_cpu_bem_panel116_material_geometry_transfer_audit_case_rows.csv
data/scarep_2d_cpu_bem_panel116_material_geometry_transfer_audit_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel116_material_geometry_transfer_audit.png
scripts/
```

## Result

```text
variant cases:                         4
solve rows:                            4
112-panel transfer pass cases:         3
116-panel transfer pass cases:         4
116-panel transfer fail cases:         0
120-panel transfer pass cases:         4
116-panel max high-band relative L2:   0.0009506170756247567
120-panel max high-band relative L2:   0.0008874668710960488
mean 116/120 wall-time ratio:          0.934122476353184
116-panel material/geometry transfer:  true
120-panel endpoint transfer:           true
project FDTD comparison ready:         false
real 3D validation ready:              false
GPU/HPC ready:                         false
field transfer ready:                  false
field FWI ready:                       false
```

Case outcomes:

| Case | 116-panel high-band L2 | 120-panel high-band L2 | 116 pass |
| --- | ---: | ---: | --- |
| radius 45 mm, baseline dielectric | 0.00029353083590203 | 0.0002746335341733692 | yes |
| radius 75 mm, baseline dielectric | 0.0009506170756247567 | 0.0008874668710960488 | yes |
| radius 60 mm, dielectric 2.5 | 0.00024947756590768487 | 0.0002334178594731874 | yes |
| radius 60 mm, dielectric 6.0 | 0.0006290553298080911 | 0.0005886249120685609 | yes |

## Interpretation

The 116-panel setting passes all four tested transfer variants. It reduces the
endpoint below 120 panels, but the larger-radius case has a smaller margin
than at 120 panels.

## Decision

Promote 116 panels as the current analytic material/geometry transfer endpoint
for these variants, pending validator and sensitivity hardening.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_material_geometry_transfer_audit.py

4 passed
```

Figure check:

```text
2536x884, dynamic range=255
```

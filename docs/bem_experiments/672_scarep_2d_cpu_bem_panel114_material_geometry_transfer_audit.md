# BEM Experiment 672: 114-Panel Material/Geometry Transfer Audit

Date: 2026-06-30

## Purpose

Test whether 114 panels can lower the passing material/geometry transfer
endpoint below the validated 116-panel result from run `669`.

This run uses the same four analytic-cylinder material/geometry variants and
compares 114 panels against the validated 116-panel endpoint. This is
analytic-only BEM evidence; it is not a project-FDTD, 3D, field, GPU/HPC, or
field-FWI comparison.

## Output

```text
outputs/bem_experiments/672_scarep_2d_cpu_bem_panel114_material_geometry_transfer_audit
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel114_material_geometry_transfer_audit_solve_rows.csv
data/scarep_2d_cpu_bem_panel114_material_geometry_transfer_audit_case_rows.csv
data/scarep_2d_cpu_bem_panel114_material_geometry_transfer_audit_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel114_material_geometry_transfer_audit.png
scripts/
```

## Result

```text
variant cases:                         4
solve rows:                            4
112-panel transfer pass cases:         3
114-panel transfer pass cases:         4
114-panel transfer fail cases:         0
116-panel transfer pass cases:         4
120-panel transfer pass cases:         4
114-panel max high-band relative L2:   0.0009848005761020824
116-panel max high-band relative L2:   0.0009506170756247567
mean 114/116 wall-time ratio:          0.9653357854619042
114-panel material/geometry transfer:  true
116-panel endpoint transfer:           true
project FDTD comparison ready:         false
real 3D validation ready:              false
GPU/HPC ready:                         false
field transfer ready:                  false
field FWI ready:                       false
```

Case outcomes:

| Case | 114-panel high-band L2 | 116-panel high-band L2 | 114 pass |
| --- | ---: | ---: | --- |
| radius 45 mm, baseline dielectric | 0.0003037350052058245 | 0.00029353083590203 | yes |
| radius 75 mm, baseline dielectric | 0.0009848005761020824 | 0.0009506170756247567 | yes |
| radius 60 mm, dielectric 2.5 | 0.000258151812146739 | 0.00024947756590768487 | yes |
| radius 60 mm, dielectric 6.0 | 0.000650882055307526 | 0.0006290553298080911 | yes |

## Interpretation

The 114-panel setting passes all four tested transfer variants, but the margin
is tight. The larger-radius case is only about `1.52e-5` below the `1e-3`
high-band target.

## Decision

Promote 114 panels as the current analytic material/geometry transfer endpoint
for these variants, pending validator and sensitivity hardening.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel114_material_geometry_transfer_audit.py

4 passed
```

Figure check:

```text
2536x884, dynamic range=255
```

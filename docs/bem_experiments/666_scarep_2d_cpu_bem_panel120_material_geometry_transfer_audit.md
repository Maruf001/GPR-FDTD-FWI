# BEM Experiment 666: 120-Panel Material/Geometry Transfer Audit

Date: 2026-06-30

## Purpose

Test whether 120 panels can close the material/geometry transfer gap left by
the 112-panel near miss in run `663`.

This run uses the same four analytic-cylinder material/geometry variants and
compares 120 panels against the existing 128-panel endpoint. This is
analytic-only BEM evidence; it is not a project-FDTD, 3D, field, GPU/HPC, or
field-FWI comparison.

## Output

```text
outputs/bem_experiments/666_scarep_2d_cpu_bem_panel120_material_geometry_transfer_audit
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel120_material_geometry_transfer_audit_solve_rows.csv
data/scarep_2d_cpu_bem_panel120_material_geometry_transfer_audit_case_rows.csv
data/scarep_2d_cpu_bem_panel120_material_geometry_transfer_audit_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel120_material_geometry_transfer_audit.png
scripts/
```

## Result

```text
variant cases:                         4
solve rows:                            4
112-panel transfer pass cases:         3
120-panel transfer pass cases:         4
120-panel transfer fail cases:         0
128-panel high-band pass cases:        4
120-panel max high-band relative L2:   0.0008874668710960488
128-panel max high-band relative L2:   0.0007789581648464677
mean 120/128 wall-time ratio:          0.8813044366721805
120-panel material/geometry transfer:  true
128-panel endpoint transfer:           true
project FDTD comparison ready:         false
real 3D validation ready:              false
GPU/HPC ready:                         false
field transfer ready:                  false
field FWI ready:                       false
```

Case outcomes:

| Case | 120-panel high-band L2 | 128-panel high-band L2 | 120 pass |
| --- | ---: | ---: | --- |
| radius 45 mm, baseline dielectric | 0.0002746335341733692 | 0.00024201679895085966 | yes |
| radius 75 mm, baseline dielectric | 0.0008874668710960488 | 0.0007789581648464677 | yes |
| radius 60 mm, dielectric 2.5 | 0.0002334178594731874 | 0.00020571195751163015 | yes |
| radius 60 mm, dielectric 6.0 | 0.0005886249120685609 | 0.0005188158397144224 | yes |

## Interpretation

The 120-panel setting closes the larger-radius transfer failure. It is the
lowest currently tested passing candidate above the 112-panel near miss and
uses about 88% of the 128-panel wall time in this four-case sweep.

The result is still analytic-cylinder evidence only. It does not validate
project FDTD matching, 3D geometry, field transfer, or GPU/HPC execution.

## Decision

Promote 120 panels as the current analytic material/geometry transfer endpoint
for these variants, pending validator and sensitivity hardening.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel120_material_geometry_transfer_audit.py

4 passed
```

Figure check:

```text
2536x884, dynamic range=255
```

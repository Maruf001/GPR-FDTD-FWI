# BEM Experiment 663: 112-Panel Material/Geometry Transfer Audit

Date: 2026-06-30

## Purpose

Test whether 112 panels can close the remaining transfer failure after the
96-panel partial-transfer result in run `660`.

This run uses the same four analytic-cylinder material/geometry variants and
compares 112 panels against the existing 128-panel endpoint. This is
analytic-only BEM evidence; it is not a project-FDTD, 3D, field, GPU/HPC, or
field-FWI comparison.

## Output

```text
outputs/bem_experiments/663_scarep_2d_cpu_bem_panel112_material_geometry_transfer_audit
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel112_material_geometry_transfer_audit_solve_rows.csv
data/scarep_2d_cpu_bem_panel112_material_geometry_transfer_audit_case_rows.csv
data/scarep_2d_cpu_bem_panel112_material_geometry_transfer_audit_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel112_material_geometry_transfer_audit.png
scripts/
```

## Result

```text
variant cases:                         4
solve rows:                            4
96-panel transfer pass cases:          3
112-panel transfer pass cases:         3
112-panel transfer fail cases:         1
128-panel high-band pass cases:        4
112-panel max high-band relative L2:   0.0010208970808398296
128-panel max high-band relative L2:   0.0007789581648464677
mean 112/128 wall-time ratio:          0.7698844158726142
112-panel material/geometry transfer:  false
128-panel endpoint transfer:           true
project FDTD comparison ready:         false
real 3D validation ready:              false
GPU/HPC ready:                         false
field transfer ready:                  false
field FWI ready:                       false
```

Case outcomes:

| Case | 112-panel high-band L2 | 128-panel high-band L2 | 112 pass |
| --- | ---: | ---: | --- |
| radius 45 mm, baseline dielectric | 0.00031449162831173627 | 0.00024201679895085966 | yes |
| radius 75 mm, baseline dielectric | 0.0010208970808398296 | 0.0007789581648464677 | no |
| radius 60 mm, dielectric 2.5 | 0.0002672974408275308 | 0.00020571195751163015 | yes |
| radius 60 mm, dielectric 6.0 | 0.0006738866408261121 | 0.0005188158397144224 | yes |

## Interpretation

The 112-panel setting is a near miss. It remains below the target for three
variants, but the larger-radius case is still just above the `1e-3`
high-band target.

The 128-panel endpoint still passes all four variants and remains the safe
analytic transfer endpoint.

## Decision

Keep 112 panels blocked as a general material/geometry transfer policy. The
next panel-search branch should test a higher intermediate count between 112
and 128.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel112_material_geometry_transfer_audit.py

4 passed
```

Figure check:

```text
2536x884, dynamic range=255
```

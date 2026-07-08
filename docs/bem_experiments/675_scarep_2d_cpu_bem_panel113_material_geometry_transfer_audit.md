# BEM Experiment 675: 113-Panel Material/Geometry Transfer Audit

Date: 2026-06-30

## Purpose

Test whether 113 panels can lower the passing material/geometry transfer
endpoint below the validated 114-panel result from run `672`.

This run uses the same four analytic-cylinder material/geometry variants and
compares 113 panels against the validated 114-panel endpoint. This is
analytic-only BEM evidence; it is not a project-FDTD, 3D, field, GPU/HPC, or
field-FWI comparison.

## Output

```text
outputs/bem_experiments/675_scarep_2d_cpu_bem_panel113_material_geometry_transfer_audit
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel113_material_geometry_transfer_audit_solve_rows.csv
data/scarep_2d_cpu_bem_panel113_material_geometry_transfer_audit_case_rows.csv
data/scarep_2d_cpu_bem_panel113_material_geometry_transfer_audit_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel113_material_geometry_transfer_audit.png
scripts/
```

## Result

```text
variant cases:                         4
solve rows:                            4
112-panel transfer pass cases:         3
113-panel transfer pass cases:         3
113-panel transfer fail cases:         1
114-panel transfer pass cases:         4
116-panel transfer pass cases:         4
113-panel max high-band relative L2:   0.0010026008820656063
114-panel max high-band relative L2:   0.0009848005761020824
mean 113/114 wall-time ratio:          0.9865254239909778
113-panel material/geometry transfer:  false
114-panel endpoint transfer:           true
project FDTD comparison ready:         false
real 3D validation ready:              false
GPU/HPC ready:                         false
field transfer ready:                  false
field FWI ready:                       false
```

Case outcomes:

| Case | 113-panel high-band L2 | 114-panel high-band L2 | 113 pass |
| --- | ---: | ---: | --- |
| radius 45 mm, baseline dielectric | 0.00030904179445031773 | 0.0003037350052058245 | yes |
| radius 75 mm, baseline dielectric | 0.0010026008820656063 | 0.0009848005761020824 | no |
| radius 60 mm, dielectric 2.5 | 0.0002626635906198611 | 0.000258151812146739 | yes |
| radius 60 mm, dielectric 6.0 | 0.0006622318853221262 | 0.000650882055307526 | yes |

## Interpretation

The 113-panel setting is the nearest tested lower-side no-go. It misses the
target only on the larger-radius case and only by about `2.6e-6`, but it is
still above the `1e-3` high-band target.

## Decision

Keep 113 panels blocked. Keep 114 panels as the current analytic
material/geometry transfer endpoint for these variants.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel113_material_geometry_transfer_audit.py

4 passed
```

Figure check:

```text
2536x884, dynamic range=255
```

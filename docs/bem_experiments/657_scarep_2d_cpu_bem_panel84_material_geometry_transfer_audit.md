# BEM Experiment 657: 84-Panel Material/Geometry Transfer Audit

Date: 2026-06-30

## Purpose

Test whether the 84-panel high-frequency policy from runs `654-656` transfers
beyond the baseline analytic-cylinder setup.

The audit solves four controlled variants with 84 panels and 128 panels:
smaller cylinder radius, larger cylinder radius, lower dielectric contrast,
and higher dielectric contrast. The result is still analytic-only BEM evidence;
it is not a project-FDTD, 3D, field, GPU/HPC, or field-FWI comparison.

## Output

```text
outputs/bem_experiments/657_scarep_2d_cpu_bem_panel84_material_geometry_transfer_audit
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel84_material_geometry_transfer_audit_solve_rows.csv
data/scarep_2d_cpu_bem_panel84_material_geometry_transfer_audit_case_rows.csv
data/scarep_2d_cpu_bem_panel84_material_geometry_transfer_audit_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel84_material_geometry_transfer_audit.png
scripts/
```

## Result

```text
variant cases:                         4
solve rows:                            8
84-panel transfer pass cases:          2
84-panel transfer fail cases:          2
128-panel high-band pass cases:        4
84-panel max high-band relative L2:    0.0018449395379997787
128-panel max high-band relative L2:   0.0007789581648464677
mean 84/128 wall-time ratio:           0.43962327328578926
84-panel material/geometry transfer:   false
128-panel endpoint transfer:           true
project FDTD comparison ready:         false
real 3D validation ready:              false
GPU/HPC ready:                         false
field transfer ready:                  false
field FWI ready:                       false
```

Case outcomes:

| Case | 84-panel high-band L2 | 128-panel high-band L2 | 84 pass |
| --- | ---: | ---: | --- |
| radius 45 mm, baseline dielectric | 0.0005555178804907428 | 0.00024201679895085966 | yes |
| radius 75 mm, baseline dielectric | 0.0018449395379997787 | 0.0007789581648464677 | no |
| radius 60 mm, dielectric 2.5 | 0.0004726802192390533 | 0.00020571195751163015 | yes |
| radius 60 mm, dielectric 6.0 | 0.001188193969563737 | 0.0005188158397144224 | no |

## Interpretation

The 84-panel setting is not a transferable high-frequency rule. It is fast
relative to 128 panels, but it fails the `1e-3` high-frequency target for the
larger-radius and higher-contrast variants.

The 128-panel endpoint passes all four variants and remains the safer analytic
endpoint for material/geometry transfer checks.

## Decision

Keep 84 panels as a baseline analytic-cylinder candidate only. Do not promote
84 panels as a general material/geometry policy. Use 128 panels for these
analytic transfer variants unless a separate lower-cost transfer policy is
validated.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel84_material_geometry_transfer_audit.py

4 passed
```

Figure check:

```text
2536x884, dynamic range=255
```

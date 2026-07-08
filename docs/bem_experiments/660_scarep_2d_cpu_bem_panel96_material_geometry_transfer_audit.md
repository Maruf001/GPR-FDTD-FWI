# BEM Experiment 660: 96-Panel Material/Geometry Transfer Audit

Date: 2026-06-30

## Purpose

Test whether 96 panels can close the material/geometry transfer gap exposed by
run `657`.

Run `657` showed that 84 panels are too aggressive for transfer beyond the
baseline analytic-cylinder setup. This run keeps the same four controlled
variants and evaluates 96 panels against the existing 128-panel endpoint.

This is analytic-cylinder BEM evidence only. It is not a project-FDTD, 3D,
field, GPU/HPC, or field-FWI comparison.

## Output

```text
outputs/bem_experiments/660_scarep_2d_cpu_bem_panel96_material_geometry_transfer_audit
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel96_material_geometry_transfer_audit_solve_rows.csv
data/scarep_2d_cpu_bem_panel96_material_geometry_transfer_audit_case_rows.csv
data/scarep_2d_cpu_bem_panel96_material_geometry_transfer_audit_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel96_material_geometry_transfer_audit.png
scripts/
```

## Result

```text
variant cases:                         4
solve rows:                            4
96-panel transfer pass cases:          3
96-panel transfer fail cases:          1
128-panel high-band pass cases:        4
96-panel max high-band relative L2:    0.0013995629205128856
128-panel max high-band relative L2:   0.0007789581648464677
mean 96/128 wall-time ratio:           0.569866438293348
96-panel material/geometry transfer:   false
128-panel endpoint transfer:           true
project FDTD comparison ready:         false
real 3D validation ready:              false
GPU/HPC ready:                         false
field transfer ready:                  false
field FWI ready:                       false
```

Case outcomes:

| Case | 96-panel high-band L2 | 128-panel high-band L2 | 96 pass |
| --- | ---: | ---: | --- |
| radius 45 mm, baseline dielectric | 0.0004262646357667119 | 0.00024201679895085966 | yes |
| radius 75 mm, baseline dielectric | 0.0013995629205128856 | 0.0007789581648464677 | no |
| radius 60 mm, dielectric 2.5 | 0.00036243544416731603 | 0.00020571195751163015 | yes |
| radius 60 mm, dielectric 6.0 | 0.0009126777010325269 | 0.0005188158397144224 | yes |

## Interpretation

The 96-panel setting improves materially over 84 panels. It fixes the
higher-contrast case and reduces every high-band error, but it still fails the
larger-radius case against the `1e-3` high-band target.

The 128-panel endpoint still passes all four variants and remains the safe
analytic endpoint for this transfer block.

## Decision

Keep 96 panels blocked as a general material/geometry transfer policy. Use
128 panels as the analytic transfer endpoint for these variants.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel96_material_geometry_transfer_audit.py

4 passed
```

Figure check:

```text
2536x884, dynamic range=255
```

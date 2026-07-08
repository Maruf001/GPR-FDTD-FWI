# BEM Experiment 869: Panel-116 Worst-Bin Spatial Residual Anatomy

Date: 2026-07-01

## Purpose

Inspect the spatial distribution of the worst remaining 116-panel high-band
frequency-bin residual across the receiver aperture.

This run re-solves the controlling 13-scan, 116-panel, 25-frequency analytic
BEM case and extracts the `2.3125 GHz` bin. It does not run project FDTD,
field processing, 3D/HPC work, or GPU kernels.

## Output

```text
outputs/bem_experiments/869_scarep_2d_cpu_bem_panel116_worst_bin_spatial_residual_anatomy_audit
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel116_worst_bin_spatial_residual_anatomy_audit_grid_row.csv
data/scarep_2d_cpu_bem_panel116_worst_bin_spatial_residual_anatomy_audit_receiver_rows.csv
data/scarep_2d_cpu_bem_panel116_worst_bin_spatial_residual_anatomy_audit_summary.json
figures/scarep_2d_cpu_bem_panel116_worst_bin_spatial_residual_anatomy_audit.png
```

## Result

```text
source decomposition ready:                  true
source validation ready:                     true
source sensitivity ready:                    true
panel count:                                 116
scan positions:                              13
receiver rows:                               13
frequency:                                   2.3125 GHz
complex relative L2 at frequency:            0.0020304660813910734
edge-quarter scan count:                     8
edge-quarter residual energy fraction:       0.5923362105102755
center-half residual energy fraction:        0.40766378948972465
maximum local relative error:                0.0024242103286349816
median local relative error:                 0.0018960777271085818
max/median local error ratio:                1.2785395313575958
worst scan order:                            3
edge-concentrated residual:                  true
scalar-gain correction promoted:             false
hard per-frequency endpoint ready:           false
project FDTD comparison ready:               false
field transfer ready:                        false
3D validation ready:                         false
```

## Interpretation

The worst-bin residual is edge-biased but not a single-receiver spike. The edge
quarters carry about 59.2% of residual energy, while the center half still
carries about 40.8%. The maximum local relative error is only about 1.28 times
the median local relative error.

This supports a spatial-shape diagnostic rather than a simple scalar gain
repair or a single bad receiver explanation.

## Decision

Keep this as diagnostic evidence only. Do not promote scalar-gain correction,
hard per-frequency acceptance, project-FDTD comparison, field transfer, or
3D/HPC claims from this run.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_spatial_residual_anatomy_audit.py
2 passed
```

Figure check:

```text
2826x853, dynamic range=255
```

# BEM Experiment 013: scarep 2D CPU BEM Scan Validation

Date: 2026-06-23

## Purpose

Validate the colleague-provided `scarep_gpr_forward_pkg` CPU Galerkin BEM path
on a small 2D TMz scan against its own analytic dielectric-cylinder reference.

This answers a more useful question than the single-point smoke from run `011`:

```text
Does the CPU 2D BEM path converge over a multi-source, multi-frequency scan?
```

This is still not a comparison against this repository's
`outputs/experiments` archive. It is the controlled method-validation step
needed before a fair BEM/FDTD comparison.

## Output

```text
outputs/bem_experiments/013_scarep_2d_cpu_bem_scan_validation
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_scan_validation_panel_summary.csv
data/scarep_2d_cpu_bem_scan_validation_best_panel_samples.csv
data/scarep_2d_cpu_bem_scan_validation_arrays.npz
data/scarep_2d_cpu_bem_scan_validation_summary.json
figures/scarep_2d_cpu_bem_scan_validation.png
figures/scarep_2d_cpu_bem_bscan_vs_analytic.png
docs/SCAREP_2D_CPU_BEM_SCAN_VALIDATION.md
run_manifest.json
```

## Result

```text
scan positions:                     11
frequencies:                        25
frequency range:                    0.25 to 3.0 GHz
panel values:                       8, 16, 32
best panels:                        32
best complex-spectrum relative L2:  0.0028625612719971973
best time-B-scan relative L2:       0.0021161825095859987
best wall time:                     6.115878419950604 s
total wall time:                    9.204148247139528 s
GPU/MFS required:                   false
CUDA/cuBLAS relevant:               false
compared to analytic reference:     true
compared to outputs/experiments:    false
```

Panel convergence:

| Panels | Complex relative L2 | Time B-scan relative L2 | Wall seconds |
| ---: | ---: | ---: | ---: |
| 8 | 0.04415449039471055 | 0.032036432437250406 | 0.724120473023504 |
| 16 | 0.011871573995031992 | 0.008758046125144577 | 1.8570082820951939 |
| 32 | 0.0028625612719971973 | 0.0021161825095859987 | 6.115878419950604 |

## Interpretation

The colleague's CPU 2D BEM path is useful. It converges over a small B-scan
style validation problem and does not depend on the currently broken
`cupy.linalg.solve`/`libcublas.so.12` path.

The code should be treated as a 2D method-validation and setup-reference
package, not as a direct replacement for our existing 2D FDTD archive and not
as a 3D Maxwell backend.

## Relation To Our 2D Work

Run `013` still does not compare directly to `outputs/experiments`.

The mismatch is setup, not just code quality:

```text
scarep validation:  frequency-domain, free-space, dielectric cylinder,
                    analytic Mie/cylindrical-harmonic reference

project FDTD runs:  time-domain, air/concrete, conductive rebar,
                    Ricker/GPR scans and inversion/detector studies
```

A fair comparison needs a shared case with the same geometry, material,
source/receiver definition, source spectrum, background medium, and observable.

## Decision

Use the `scarep` CPU Galerkin 2D BEM path as validated 2D method evidence.

Do not block on CUDA/cuBLAS for this branch. Fixing `libcublas.so.12` is only
needed if we want the optional GPU MFS demo path.

## Validation

Commands run:

```text
conda run -n gpr-fdtd-fwi python run_scarep_2d_cpu_bem_scan_validation.py
```

Image sanity check:

```text
PNG count:      2
all images:     nonblank
dynamic range:  255 for every generated PNG
```

## Next Action

Build a matched 2D BEM/FDTD comparison adapter. The first fair target should
match this analytic cylinder setup on the project FDTD side, then move to a
single conductive rebar setup closer to `outputs/experiments`.

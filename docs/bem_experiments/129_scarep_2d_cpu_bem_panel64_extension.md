# BEM Experiment 129: scarep 2D CPU BEM 64-Panel Extension

Date: 2026-06-27

## Purpose

Extend the colleague-provided `scarep` 2D CPU Galerkin BEM scan validation from
run `013` to include a 64-panel boundary discretization.

This run still compares only against the scarep analytic dielectric-cylinder
reference. It does not compare against `outputs/experiments`, run 3D FDTD,
launch GPU/HPC work, run field FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/129_scarep_2d_cpu_bem_panel64_extension
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_scan_validation_panel_summary.csv
data/scarep_2d_cpu_bem_scan_validation_best_panel_samples.csv
data/scarep_2d_cpu_bem_scan_validation_arrays.npz
data/scarep_2d_cpu_bem_panel64_extension_summary.json
figures/scarep_2d_cpu_bem_scan_validation.png
figures/scarep_2d_cpu_bem_bscan_vs_analytic.png
docs/SCAREP_2D_CPU_BEM_PANEL64_EXTENSION.md
scripts/script_snapshot_manifest.json
```

## Result

```text
scan positions:                       11
frequencies:                          25
panel values:                         [8, 16, 32, 64]
best panels:                          64
32-panel complex relative L2:          0.0028625612719971973
64-panel complex relative L2:          0.0007053747139208214
complex error reduction 32 to 64:      4.0582136210776065
32-panel time-B-scan relative L2:      0.0021161825095859987
64-panel time-B-scan relative L2:      0.0005202399688500149
time-B-scan error reduction 32 to 64:  4.067704590756066
32-panel wall seconds:                 5.936822667950764
64-panel wall seconds:                 20.658447734080255
64/32 wall-time ratio:                 3.479714468414636
panel64 extension ready:               true
compared to scarep analytic reference: true
compared to project FDTD archive:      false
```

Panel convergence:

| Panels | Complex relative L2 | Time B-scan relative L2 | Wall seconds |
| ---: | ---: | ---: | ---: |
| 8 | 0.04415449039471055 | 0.032036432437250406 | 0.7215461458545178 |
| 16 | 0.011871573995031992 | 0.008758046125144577 | 1.847267288947478 |
| 32 | 0.0028625612719971973 | 0.0021161825095859987 | 5.936822667950764 |
| 64 | 0.0007053747139208214 | 0.0005202399688500149 | 20.658447734080255 |

## Interpretation

The 64-panel CPU BEM solve improves both the complex-spectrum and reconstructed
time-B-scan errors by about `4x` relative to the 32-panel result, while taking
about `3.48x` as long. This strengthens the 2D scarep CPU Galerkin BEM
convergence evidence.

The limitation is unchanged: this is an analytic dielectric-cylinder
validation, not a direct comparison to this repository's time-domain FDTD
experiment archive.

## Decision

Use the 64-panel extension as stronger 2D method-validation evidence for the
colleague scarep CPU BEM path. Keep project FDTD comparison, 3D validation,
GPU/HPC, and field FWI blocked until a matched setup is used.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel64_extension.py
3 passed
```

Figure validation:

```text
scarep_2d_cpu_bem_scan_validation.png    1762x1289, dynamic range=255
scarep_2d_cpu_bem_bscan_vs_analytic.png  2139x740, dynamic range=255
```

Script snapshots:

```text
run_scarep_2d_cpu_bem_panel64_extension.py
sha256=07e6591882d3eeb77d563d4d268ad243c9a5d810e53b4bfada5f33ed1c158f1b

run_scarep_2d_cpu_bem_scan_validation.py
sha256=6fb3da41e7a74cfb1af7f73cd06e69e6e9c82f8a6ce1234de16b548b33718238

tests/test_scarep_2d_cpu_bem_panel64_extension.py
sha256=3d7b2447f0d32f9704b26b660c5350d2db371fd8db20810951b2daacf44421a6
```

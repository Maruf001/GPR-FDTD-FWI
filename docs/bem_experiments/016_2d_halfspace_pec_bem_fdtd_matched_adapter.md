# BEM Experiment 016: Matched 2D Half-Space PEC BEM/FDTD Adapter

Date: 2026-06-23

## Purpose

Move the matched PEC adapter from the homogeneous free-space case in run `015`
into an air/concrete half-space.

This is the closest BEM-side adapter so far to the rebar forward-modeling
problem. It is still not field evidence and does not use the older
`outputs/experiments` archive as input.

## Output

```text
outputs/bem_experiments/016_2d_halfspace_pec_bem_fdtd_matched_adapter
```

Key artifacts:

```text
data/matched_2d_halfspace_pec_bem_panel_summary.csv
data/matched_2d_halfspace_pec_fdtd_grid_summary.csv
data/matched_2d_halfspace_pec_bem_fdtd_adapter_summary.json
data/matched_2d_halfspace_pec_bem_fdtd_arrays.npz
figures/matched_2d_halfspace_pec_bem_fdtd_geometry.png
figures/matched_2d_halfspace_pec_bem_fdtd_error_runtime.png
figures/matched_2d_halfspace_pec_bem_fdtd_bscan_comparison.png
docs/MATCHED_2D_HALFSPACE_PEC_BEM_FDTD_ADAPTER.md
run_manifest.json
```

## Matched Setup

```text
geometry:       air/concrete half-space with one PEC cylinder
interface:      z=0.10 m
PEC center:     (0.6, 0.35) m
PEC radius:     0.0125 m
upper medium:   eps_r=1.0, sigma=0
lower medium:   eps_r=6.0, sigma=0.01 S/m
scan:           11 paired Tx/Rx positions
Tx/Rx offset:   0.06 m
frequencies:    81 samples, 50 MHz to 4 GHz
time window:    15 ns, 4096 common output samples
observable:     band-limited time-domain B-scan, >=0.5 GHz
BEM backend:    colleague CPU layered PEC 2D TMz BEM
FDTD backend:   colleague Yee 2D TMz FDTD baseline with half-space grid and PEC mask
```

There is no analytic reference in this path, so the 32-panel layered BEM result
is used as the comparison reference.

## Result

BEM panel check:

| Panels | Relative L2 vs 32-panel BEM | Wall seconds |
| ---: | ---: | ---: |
| 16 | 0.0004746867074423852 | 23.183080262038857 |
| 32 | 0.0 | 76.21174292522483 |

FDTD refinement:

| dx (mm) | Grid | PEC nodes | Relative L2 vs 32-panel BEM | Fair seconds |
| ---: | --- | ---: | ---: | ---: |
| 3.0 | 401x421 | 54 | 0.030998297443390457 | 28.665912175085396 |
| 5.0 | 241x253 | 21 | 0.05496823986057341 | 11.484113185899332 |

Summary:

```text
reference BEM:               32 panels
16-panel BEM vs reference:   0.0004746867074423852
best FDTD dx:                3 mm
best FDTD vs reference BEM:  0.030998297443390457
cuBLAS required:             false
GPU array backend for FDTD:  true
matched half-space ready:    true
project core FDTD matched:   false
```

## Interpretation

The half-space PEC adapter is viable.

The layered BEM panel check is tight: 16 panels are already within about
0.047% relative L2 of the 32-panel reference for this band-limited B-scan.
FDTD also behaves as expected: the 3 mm grid improves materially over the
5 mm grid.

The run is computationally heavier than the homogeneous adapters because the
layered BEM path uses CPU Sommerfeld quadrature. That is acceptable for
reference generation but not yet a production inversion inner loop.

## Decision

Use run `016` as the current BEM-side half-space PEC/rebar checkpoint.

The next technical fork is:

```text
publication/presentation: use runs 014-016 as the BEM/FDTD validation ladder
project integration: build a project-core FDTD source-normalization adapter
performance: accelerate/tabulate the layered Green function before inversion
```

## Validation

Commands run:

```text
conda run -n gpr-fdtd-fwi python run_2d_halfspace_pec_bem_fdtd_matched_adapter.py
```

Image sanity check:

```text
PNG count:      3
all images:     nonblank
dynamic range:  255 for every generated PNG
```

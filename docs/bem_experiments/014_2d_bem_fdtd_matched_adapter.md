# BEM Experiment 014: Matched 2D BEM/FDTD Adapter

Date: 2026-06-23

## Purpose

Create the first controlled 2D cross-solver benchmark for the BEM research
track.

The goal is to compare BEM and FDTD only after matching the setup:

```text
same geometry
same material
same source/receiver scan
same source spectrum
same observable
```

This run belongs in the BEM track because it is a solver-validation adapter. It
is not a field run and not part of the main synthetic FDTD/FWI/detector
experiment stream.

## Output

```text
outputs/bem_experiments/014_2d_bem_fdtd_matched_adapter
```

Key artifacts:

```text
data/matched_2d_bem_panel_summary.csv
data/matched_2d_fdtd_grid_summary.csv
data/matched_2d_bem_fdtd_adapter_summary.json
data/matched_2d_bem_fdtd_arrays.npz
figures/matched_2d_bem_fdtd_geometry.png
figures/matched_2d_bem_fdtd_error_runtime.png
figures/matched_2d_bem_fdtd_bscan_comparison.png
docs/MATCHED_2D_BEM_FDTD_ADAPTER.md
run_manifest.json
```

## Matched Setup

```text
geometry:       dielectric cylinder, center=(0.6, 0.4) m, radius=0.06 m
material:       exterior eps_r=1.0, interior eps_r=4.0
scan:           11 paired Tx/Rx positions
Tx/Rx offset:   0.06 m
frequencies:    121 samples, 50 MHz to 4 GHz
time window:    12 ns, 4096 common output samples
observable:     band-limited time-domain B-scan, >=0.5 GHz
reference:      analytic dielectric-cylinder series
BEM backend:    colleague CPU Galerkin 2D TMz BEM
FDTD backend:   colleague Yee 2D TMz FDTD baseline
```

This run does not use `outputs/experiments` as input and does not claim that
the older project FDTD archive has been matched yet.

## Result

BEM convergence:

| Panels | Relative L2 vs analytic | Wall seconds |
| ---: | ---: | ---: |
| 8 | 0.04922236457746863 | 3.4564417090732604 |
| 16 | 0.013225934629433566 | 8.889802388148382 |
| 32 | 0.003190629524250936 | 27.634085624013096 |

FDTD refinement:

| dx (mm) | Grid | Relative L2 vs analytic | Relative L2 vs best BEM | Fair seconds |
| ---: | --- | ---: | ---: | ---: |
| 5.0 | 241x261 | 0.024754323796019783 | 0.02330746966791303 | 6.408158769132569 |
| 8.0 | 151x163 | 0.03249817112136078 | 0.03257036852446959 | 4.085958046838641 |

Summary:

```text
best BEM:                    32 panels
best BEM relative L2:         0.003190629524250936
best FDTD dx:                 5 mm
best FDTD relative L2:        0.024754323796019783
best FDTD vs best BEM L2:     0.02330746966791303
cuBLAS required:              false
GPU array backend for FDTD:   true
matched adapter ready:        true
project core FDTD matched:    false
```

## Interpretation

The matched 2D adapter is now real. BEM and FDTD are being compared under the
same dielectric-cylinder setup, and the results are physically sensible:

- BEM error drops with panel refinement.
- FDTD error improves when the grid is refined from 8 mm to 5 mm.
- The 5 mm FDTD B-scan is within about 2.5% relative L2 of the analytic
  reference and about 2.3% of the best BEM result after the standard
  band-limited comparison.

The `libcublas.so.12` issue does not block this run. It blocks the optional GPU
MFS solve path, but the matched FDTD baseline uses CuPy array kernels and runs
successfully on the NVIDIA GB10.

## Decision

Use run `014` as the current matched 2D BEM/FDTD validation checkpoint.

Keep this checkpoint in `docs/bem_experiments` and
`outputs/bem_experiments`. If we need to connect this directly to our older
`outputs/experiments` archive, make that a separate project-core FDTD adapter
rather than mixing the tracks.

## Validation

Commands run:

```text
conda run -n gpr-fdtd-fwi python run_2d_bem_fdtd_matched_adapter.py \
  --num-frequencies 121 \
  --freq-min-hz 50000000 \
  --freq-max-hz 4000000000 \
  --time-samples 4096
```

The script defaults now match this successful configuration.

Image sanity check:

```text
PNG count:      3
all images:     nonblank
dynamic range:  255 for every generated PNG
```

## Next Action

The next defensible BEM-side step is to move from this free-space dielectric
cylinder to a matched conductive-rebar or half-space rebar case.

The separate project-integration step is to design a project-core FDTD adapter
with compatible source normalization and observables before comparing against
`outputs/experiments`.

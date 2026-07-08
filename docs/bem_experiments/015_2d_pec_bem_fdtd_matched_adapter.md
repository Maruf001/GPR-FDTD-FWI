# BEM Experiment 015: Matched 2D PEC BEM/FDTD Adapter

Date: 2026-06-23

## Purpose

Move the matched 2D adapter from the dielectric-cylinder benchmark in run `014`
to a PEC cylinder, which is closer to the rebar modeling branch.

This is still a BEM-track validation experiment. It is not a field run and does
not use `outputs/experiments` as input.

## Output

```text
outputs/bem_experiments/015_2d_pec_bem_fdtd_matched_adapter
```

Key artifacts:

```text
data/matched_2d_pec_bem_panel_summary.csv
data/matched_2d_pec_fdtd_grid_summary.csv
data/matched_2d_pec_bem_fdtd_adapter_summary.json
data/matched_2d_pec_bem_fdtd_arrays.npz
figures/matched_2d_pec_bem_fdtd_geometry.png
figures/matched_2d_pec_bem_fdtd_error_runtime.png
figures/matched_2d_pec_bem_fdtd_bscan_comparison.png
docs/MATCHED_2D_PEC_BEM_FDTD_ADAPTER.md
run_manifest.json
```

## Matched Setup

```text
geometry:       PEC cylinder, center=(0.6, 0.35) m, radius=0.0125 m
material:       homogeneous exterior eps_r=1.0, PEC interior
scan:           11 paired Tx/Rx positions
Tx/Rx offset:   0.06 m
frequencies:    121 samples, 50 MHz to 4 GHz
time window:    12 ns, 4096 common output samples
observable:     band-limited time-domain B-scan, >=0.5 GHz
reference:      analytic PEC circular-cylinder series
BEM backend:    colleague CPU PEC 2D TMz BEM
FDTD backend:   colleague Yee 2D TMz FDTD baseline with PEC mask
```

## Result

BEM convergence:

| Panels | Relative L2 vs analytic | Wall seconds |
| ---: | ---: | ---: |
| 16 | 0.0007614963100214913 | 2.0221532608848065 |
| 32 | 0.00019202112452958636 | 6.0983350810129195 |
| 64 | 4.762231342258939e-05 | 23.14085225807503 |

FDTD refinement:

| dx (mm) | Grid | PEC nodes | Relative L2 vs analytic | Relative L2 vs best BEM | Fair seconds |
| ---: | --- | ---: | ---: | ---: | ---: |
| 3.0 | 401x421 | 54 | 0.0343267003276678 | 0.03432024436144074 | 22.93082320992835 |
| 5.0 | 241x253 | 21 | 0.040876627981823586 | 0.04086789620238616 | 9.36831536795944 |

Summary:

```text
best BEM:                    64 panels
best BEM relative L2:         4.762231342258939e-05
best FDTD dx:                 3 mm
best FDTD relative L2:        0.0343267003276678
best FDTD vs best BEM L2:     0.03432024436144074
cuBLAS required:              false
GPU array backend for FDTD:   true
matched PEC adapter ready:    true
project core FDTD matched:    false
```

## Interpretation

The PEC-cylinder bridge is working.

The CPU PEC BEM path is highly accurate against the analytic PEC reference, and
the Yee FDTD PEC-mask baseline improves when the grid is refined from 5 mm to
3 mm. The remaining FDTD error is consistent with a volumetric grid resolving a
12.5 mm radius circular PEC object with only 21 to 54 physical PEC nodes.

This is materially closer to rebar than the dielectric-cylinder benchmark, but
it is still a homogeneous free-space case. It does not yet include concrete,
air/concrete coupling, antenna coupling, measured data, or our older project
FDTD archive.

## Decision

Use run `015` as the current matched 2D PEC/rebar-style BEM/FDTD checkpoint.

The next harder scientific step is a concrete half-space or project-core FDTD
adapter, not a field or `outputs/experiments` claim.

## Validation

Commands run:

```text
conda run -n gpr-fdtd-fwi python run_2d_pec_bem_fdtd_matched_adapter.py
```

Image sanity check:

```text
PNG count:      3
all images:     nonblank
dynamic range:  255 for every generated PNG
```

## Next Action

Two reasonable next branches:

1. Add a concrete half-space PEC rebar matched adapter.
2. Build a project-core FDTD source-normalization adapter before linking this
   branch to `outputs/experiments`.

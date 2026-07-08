# BEM Experiment 012: Track Figure Pack

Date: 2026-06-23

## Purpose

Add visual artifacts to the current BEM research track.

Runs `001`-`011` had useful numeric outputs, but several folders lacked
`figures/` artifacts. This run makes the current BEM state easier to inspect
and easier to discuss in the upcoming presentation.

This is a plotting/checkpoint run. It does not run new BEM solves, FDTD
simulations, FWI, field processing, GPU work, or 3D/HPC jobs.

## Output

```text
outputs/bem_experiments/012_bem_track_figure_pack
```

Key artifacts:

```text
data/bem_track_figure_manifest.csv
data/bem_track_figure_pack_summary.json
figures/bem_track_visual_checkpoint.png
docs/BEM_TRACK_FIGURE_PACK.md
run_manifest.json
```

This run also writes figure folders into prior BEM output runs:

```text
outputs/bem_experiments/003_bempp_direct_rebar_mesh_probe/figures
outputs/bem_experiments/004_bempp_rebar_receiver_response_probe/figures
outputs/bem_experiments/006_bempp_rebar_frequency_sweep_probe/figures
outputs/bem_experiments/007_bem_fdtd_2d_tmz_sanity_probe/figures
outputs/bem_experiments/011_colleague_scarep_2d_code_audit/figures
```

## Result

```text
figures generated:                         7
figures written into existing BEM runs:    6
aggregate checkpoint figures:              1
scarep compared to outputs/experiments:    false
scarep compared to analytic reference:     true
apples-to-apples BEM/FDTD ready:           false
CPU BEM blocked by CUDA/cuBLAS:            false
GPU MFS demo blocked by CUDA/cuBLAS:        true
```

Generated figures:

| Run | Figure | Meaning |
| --- | --- | --- |
| `003` | `figures/bempp_direct_rebar_mesh.png` | Direct finite-cylinder surface mesh for the Bempp Maxwell smoke test. |
| `004` | `figures/bempp_rebar_receiver_response.png` | Homogeneous 3D BEM receiver-line scattered and total-field response. |
| `006` | `figures/bempp_rebar_frequency_sweep.png` | BEM receiver-response envelope across `k=4,6,8,10,12 rad/m`. |
| `007` | `figures/fdtd_2d_tmz_receiver_line_response.png` | In-repo 2D TMz FDTD receiver-line response. |
| `007` | `figures/fdtd_2d_tmz_scattered_trace_image.png` | 2D TMz FDTD scattered `Ez` trace image over receiver position and time. |
| `011` | `figures/scarep_bem_convergence.png` | Colleague 2D TMz BEM convergence against its analytic dielectric-cylinder reference. |
| `012` | `figures/bem_track_visual_checkpoint.png` | Aggregate visual checkpoint across current BEM evidence. |

## Setup Clarification

The colleague package has not yet been compared directly against this
repository's `outputs/experiments` archive. The run `011` convergence result
compares the colleague package against its own analytic dielectric-cylinder
reference.

That is still useful, but it answers a narrower question:

```text
Does the colleague 2D TMz CPU BEM path converge on a known analytic 2D case?
```

It does not yet answer:

```text
Does the colleague 2D TMz BEM reproduce one of our existing 2D FDTD experiment
outputs under a matched setup?
```

For that, the BEM and FDTD sides need a shared case with the same geometry,
material model, source waveform or frequency, receiver line, background medium,
and observable.

## What Panels Mean

In the colleague 2D BEM convergence case, a panel is one straight boundary
element on the circular scatterer contour.

More panels means the circular boundary is represented by a finer polygon and
the BEM system has more unknowns. The observed error drop from 8 to 16 to 32
panels is therefore a boundary-refinement convergence check.

## CUDA/cuBLAS Decision

The immediate solution is not to block on CUDA. The CPU/numpy Galerkin BEM path
already works and is enough for the first 2D validation track.

The GPU MFS demo fails because `cupy.linalg.solve` cannot load
`libcublas.so.12`. That is an environment issue for the optional GPU path, not
a blocker for the CPU BEM validation result.

## Decision

Use the colleague code as a 2D method-validation and comparison-design
reference.

The next scientific step is a matched 2D BEM/FDTD comparison case, not a direct
claim that run `011` already validates against `outputs/experiments`.

## Validation

Commands run:

```text
conda run -n gpr-fdtd-fwi python run_bem_track_figure_pack.py
```

Image sanity check:

```text
PNG count:          7
all images:         nonblank
dynamic range:      255 for every generated PNG
largest figure:     1780x1289
```

# BEM Matched-Adapter Checkpoint

Date: 2026-06-23

## Scope

This checkpoint records the BEM research-track continuation after the colleague
2D GPR-BEM package was imported and audited.

The work stays in the BEM stream:

```text
outputs/bem_experiments
docs/bem_experiments
```

It does not promote anything to field evidence, does not use measured field
data, and does not claim direct agreement with the older
`outputs/experiments` archive.

## New Runs

```text
012_bem_track_figure_pack
013_scarep_2d_cpu_bem_scan_validation
014_2d_bem_fdtd_matched_adapter
015_2d_pec_bem_fdtd_matched_adapter
016_2d_halfspace_pec_bem_fdtd_matched_adapter
```

## Figure Fix

Run `012` added figure artifacts across the BEM track:

```text
figures generated:                         7
figures written into existing BEM runs:    6
aggregate checkpoint figures:              1
```

This addressed the missing-figure problem in `outputs/bem_experiments`.

## Colleague 2D BEM Validation

Run `013` validates the colleague CPU Galerkin 2D TMz BEM path against its
analytic dielectric-cylinder reference:

| Panels | Complex relative L2 | Time B-scan relative L2 |
| ---: | ---: | ---: |
| 8 | 0.04415449039471055 | 0.032036432437250406 |
| 16 | 0.011871573995031992 | 0.008758046125144577 |
| 32 | 0.0028625612719971973 | 0.0021161825095859987 |

This confirms the colleague package is useful as 2D method evidence. It does
not make it a direct 3D backend.

## Matched 2D BEM/FDTD Ladder

Run `014`: dielectric cylinder, analytic reference.

```text
best BEM:               32 panels
best BEM L2:            0.003190629524250936
best FDTD dx:           5 mm
best FDTD L2:           0.024754323796019783
best FDTD vs BEM L2:    0.02330746966791303
```

Run `015`: homogeneous PEC cylinder, analytic PEC reference.

```text
best BEM:               64 panels
best BEM L2:            4.762231342258939e-05
best FDTD dx:           3 mm
best FDTD L2:           0.0343267003276678
best FDTD vs BEM L2:    0.03432024436144074
```

Run `016`: air/concrete half-space PEC cylinder, 32-panel layered BEM
reference.

```text
16-panel BEM vs 32-panel BEM:  0.0004746867074423852
best FDTD dx:                  3 mm
best FDTD vs 32-panel BEM:     0.030998297443390457
```

The ladder is now:

```text
dielectric cylinder -> PEC cylinder -> concrete half-space PEC cylinder
```

## Current Decision

Use runs `014`-`016` as the current BEM/FDTD validation ladder for presentation
and report material.

Do not claim that the older `outputs/experiments` archive has already been
matched. If that linkage is needed, build a separate project-core FDTD
source-normalization adapter.

Do not block the CPU BEM track on `libcublas.so.12`. The cuBLAS issue blocks
the optional GPU MFS path, not the CPU BEM validation or the Yee FDTD baseline
runs used here.

## Remaining Technical Queue

1. Build a project-core FDTD source-normalization adapter if direct linkage to
   `outputs/experiments` is needed.
2. Accelerate or tabulate the layered Green function before using half-space
   BEM as an inversion inner loop.
3. Decide whether fixing CUDA/cuBLAS is worth it for the optional scarep GPU
   MFS demos.
4. Design a true 3D FDTD reference problem for the Bempp finite-cylinder result
   from run `004`.

## Validation

Commands run:

```text
conda run -n gpr-fdtd-fwi python run_bem_track_figure_pack.py
conda run -n gpr-fdtd-fwi python run_scarep_2d_cpu_bem_scan_validation.py
conda run -n gpr-fdtd-fwi python run_2d_bem_fdtd_matched_adapter.py
conda run -n gpr-fdtd-fwi python run_2d_pec_bem_fdtd_matched_adapter.py
conda run -n gpr-fdtd-fwi python run_2d_halfspace_pec_bem_fdtd_matched_adapter.py
conda run -n gpr-fdtd-fwi python -m py_compile \
  run_2d_bem_fdtd_matched_adapter.py \
  run_2d_pec_bem_fdtd_matched_adapter.py \
  run_2d_halfspace_pec_bem_fdtd_matched_adapter.py \
  run_bem_track_figure_pack.py \
  run_scarep_2d_cpu_bem_scan_validation.py
git diff --check
```

Image sanity checks:

```text
run 012 PNGs:  7 nonblank
run 013 PNGs:  2 nonblank
run 014 PNGs:  3 nonblank
run 015 PNGs:  3 nonblank
run 016 PNGs:  3 nonblank
```

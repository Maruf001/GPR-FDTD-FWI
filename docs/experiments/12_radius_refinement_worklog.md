# Experiment 12: Radius Refinement Worklog

## Goal

Continue from the single-rebar coarse-to-fine pipeline and remove the remaining
radius bias.

Current best staged result:

```text
outputs/experiments/009_single_rebar_grid1mm_powell_refine_from_2mm/
truth:     x=250.0 mm, z=90.0 mm, radius=6.0 mm
recovered: x=249.5 mm, z=90.7 mm, radius=7.0 mm
best J:    2.0828e-03
NRMS data: 7.8896e-03
```

The next work should avoid another broad global search. The useful question is
whether the high radius is caused by:

- a local radius/depth tradeoff near the recovered position,
- too few scan positions,
- single-frequency amplitude/waveform ambiguity,
- or optimizer termination before radius is profiled well.

## Working Rules

- Use `/home/lam001/miniforge3/envs/FNO/bin/python`.
- Keep outputs in `outputs/experiments/NNN_<run_name>/`.
- Prefer 1 mm hard-grid forward runs for production radius evidence.
- Use 2 mm subcell only as a cheaper diagnostic or fallback.
- Record every substantive run here before moving to the next one.

## Run Log

### 010 - radius profile at run 009 recovered x/z

Purpose: profile the 1 mm-grid radius objective near the recovered location
from run 009, with the same 5-source sampling. This separates a radius-only
bias from a coupled z-radius valley.

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_radius_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --run-name radius_profile_grid1mm_5src_at_run009 \
  --radius-count 31 \
  --z-bounds-mm 70,110 \
  --radius-bounds-mm 4,10 \
  --profile-x-mm 249.5333604898392 \
  --profile-z-mm 90.65264829814728 \
  --profile-radius-mm 6.954785108476757 \
  --compare-summary-json outputs/experiments/009_single_rebar_grid1mm_powell_refine_from_2mm/data/single_rebar_summary.json \
  --log-every 100
```

Output:

```text
outputs/experiments/010_radius_profile_grid1mm_5src_at_run009/
```

Result:

```text
fixed x/z: x=249.533 mm, z=90.653 mm
sampled minimum:   r=6.800 mm, J=2.0828e-03
quadratic minimum: r=6.834 mm, J=2.0462e-03
true point:        r=6.000 mm at x=250.000 mm, z=90.000 mm, J=0
```

Interpretation: at the run 009 recovered x/z, the high radius is genuinely
preferred by the current waveform objective. This is not just Powell failing to
move radius; it is probably a coupled z-radius valley caused by the recovered
depth being about 0.65 mm deeper than truth.

### 011 - radius profile at run 009 x and true z

Purpose: profile radius at the same recovered x from run 009 but with z fixed
to the known synthetic truth. This cheaply tests whether a sub-millimeter depth
shift is enough to explain the high-radius preference.

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_radius_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --run-name radius_profile_grid1mm_5src_run009x_truez \
  --radius-count 31 \
  --z-bounds-mm 70,110 \
  --radius-bounds-mm 4,10 \
  --profile-x-mm 249.5333604898392 \
  --profile-z-mm 90.0 \
  --profile-radius-mm 6.0 \
  --compare-summary-json outputs/experiments/009_single_rebar_grid1mm_powell_refine_from_2mm/data/single_rebar_summary.json \
  --log-every 100
```

Output:

```text
outputs/experiments/011_radius_profile_grid1mm_5src_run009x_truez/
```

Result:

```text
fixed x/z: x=249.533 mm, z=90.000 mm
sampled minimum:   r=6.000 mm, J=0
quadratic minimum: r=6.070 mm, J≈-4.13e-04
run 009 compare:   x=249.533 mm, z=90.653 mm, r=6.955 mm, J=2.0828e-03
```

Interpretation: the high-radius result is a depth-radius coupling. A
0.65 mm deeper center can trade against about +0.8 to +1.0 mm radius and still
match the waveform closely. The x coordinate is effectively correct on the
1 mm hard grid: x=249.533 mm and x=250.000 mm rasterize to the same center.

### 012 - z-radius grid at run 009 x

Purpose: sample a compact z-radius grid around the true local basin at the run
009 x coordinate. This checks whether a deterministic local grid polish would
recover the zero-misfit basin after the Powell stage.

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_radius_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --run-name z_radius_grid1mm_5src_run009x \
  --radius-count 17 \
  --radius-bounds-mm 5.2,6.8 \
  --z-count 9 \
  --z-half-window-mm 1.0 \
  --z-bounds-mm 70,110 \
  --profile-x-mm 249.5333604898392 \
  --profile-z-mm 90.0 \
  --profile-radius-mm 6.0 \
  --compare-summary-json outputs/experiments/009_single_rebar_grid1mm_powell_refine_from_2mm/data/single_rebar_summary.json \
  --progress-every 25 \
  --log-every 100
```

Output:

```text
outputs/experiments/012_z_radius_grid1mm_5src_run009x/
```

Result:

```text
fixed x: x=249.533 mm
radius profile minimum: r=6.000 mm, J=0
z-radius minimum:       z=89.500 mm, r=6.000 mm, J=0
zero plateau:           z=89.500,89.750,90.000,90.250,90.500 mm at r=6.000 mm
run 009 compare:        z=90.653 mm, r=6.955 mm, J=2.0828e-03
```

Interpretation: the local 1 mm hard-grid objective is rasterized. The true
material mask appears as a plateau in sub-millimeter physical coordinates, and
a deterministic local grid polish over z/r can recover the correct radius after
Powell. The continuous optimizer stopped in a nearby nonzero basin because
smooth numerical tolerances are not aligned with the rasterized geometry.

### 013 - radius profile at run 009 x/z with 9 sources

Purpose: repeat the radius profile at the run 009 recovered x/z with 9 sources
instead of 5. This tests whether more scan positions raise the wrong-depth /
high-radius valley enough to reduce the bias.

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_radius_profile.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 9 \
  --run-name radius_profile_grid1mm_9src_at_run009 \
  --radius-count 31 \
  --z-bounds-mm 70,110 \
  --radius-bounds-mm 4,10 \
  --profile-x-mm 249.5333604898392 \
  --profile-z-mm 90.65264829814728 \
  --profile-radius-mm 6.954785108476757 \
  --compare-summary-json outputs/experiments/009_single_rebar_grid1mm_powell_refine_from_2mm/data/single_rebar_summary.json \
  --log-every 100
```

Output:

```text
outputs/experiments/013_radius_profile_grid1mm_9src_at_run009/
```

Result:

```text
fixed x/z: x=249.533 mm, z=90.653 mm
sampled minimum:   r=6.800 mm, J=1.3710e-03
quadratic minimum: r=6.788 mm, J=1.3669e-03
5-source run 010:  r=6.800 mm, J=2.0828e-03
```

Interpretation: using 9 scan positions lowers the wrong-depth valley but does
not move its radius minimum toward 6 mm. More sources alone are not enough;
the pipeline needs a deterministic local polish or a different parameterization.

### 014 - grid-polish integration from run 009 seed

Purpose: validate the new `--grid-polish` inversion option. Start from the run
009 seed, cap Powell almost immediately, and let the deterministic local grid
polish recover the best rasterized z/r cell.

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_inversion.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --optimizer powell \
  --max-iter 1 \
  --max-evals 1 \
  --run-name single_rebar_grid1mm_gridpolish_from_run009 \
  --init-x-mm 249.5333604898392 \
  --init-z-mm 90.65264829814728 \
  --init-radius-mm 6.954785108476757 \
  --x-bounds-mm 220,280 \
  --z-bounds-mm 70,110 \
  --radius-bounds-mm 4,10 \
  --grid-polish \
  --polish-x-half-window-mm 0 \
  --polish-z-half-window-mm 1.0 \
  --polish-radius-half-window-mm 1.0 \
  --polish-x-step-mm 1.0 \
  --polish-z-step-mm 0.25 \
  --polish-radius-step-mm 0.1 \
  --polish-progress-every 25
```

Output:

```text
outputs/experiments/014_single_rebar_grid1mm_gridpolish_from_run009/
```

Result:

```text
optimizer seed: x=249.533 mm, z=90.653 mm, radius=6.955 mm, J=2.0828e-03
polish best:    x=250.000 mm, z=89.750 mm, radius=6.000 mm, J=0
recovered:      x=250.000 mm, z=89.750 mm, radius=6.000 mm
NRMS model:     0
NRMS data:      0
runtime:        865.7 s total, 855.1 s polish, 160 polish evaluations
```

Interpretation: `--grid-polish` fixes the radius bias for the hard-grid
1 mm staged case. The z value is reported as 89.75 mm because the hard-grid
circle rasterizes to the same material mask as the true z=90.0 mm model. The
scientifically meaningful recovered geometry on this grid is radius=6.0 mm and
the true rasterized material mask.

## Current Conclusion

The best current pipeline for the synthetic single-rebar case is:

```text
2 mm bounded global search
-> 1 mm local continuous refinement
-> 1 mm deterministic local grid polish
```

The local grid polish is not a cosmetic post-process. It handles the fact that
hard-grid geometry is piecewise constant in physical coordinates. A continuous
optimizer can stop inside a nearby low-misfit z/r tradeoff, while an absolute
millimeter grid search recovers the correct rasterized radius.

## Next Candidate Work

- Consider a cheaper two-stage polish: coarse z/r grid first, then only refine
  around the best rasterized cell.
- Decide whether production should use 1 mm hard-grid + polish or 2 mm subcell
  + polish for speed.

## 016 - early-stop grid polish check

Purpose: validate the new `--polish-stop-misfit` early-stop option. For exact
synthetic inversion, the polish can stop as soon as it finds J=0 instead of
evaluating the whole local grid.

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_inversion.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --optimizer powell \
  --max-iter 1 \
  --max-evals 1 \
  --run-name single_rebar_grid1mm_gridpolish_earlystop_from_run009 \
  --init-x-mm 249.5333604898392 \
  --init-z-mm 90.65264829814728 \
  --init-radius-mm 6.954785108476757 \
  --x-bounds-mm 220,280 \
  --z-bounds-mm 70,110 \
  --radius-bounds-mm 4,10 \
  --grid-polish \
  --polish-x-half-window-mm 0 \
  --polish-z-half-window-mm 1.0 \
  --polish-radius-half-window-mm 1.0 \
  --polish-x-step-mm 1.0 \
  --polish-z-step-mm 0.25 \
  --polish-radius-step-mm 0.1 \
  --polish-stop-misfit 0
```

Output:

```text
outputs/experiments/016_single_rebar_grid1mm_gridpolish_earlystop_from_run009/
```

Result:

```text
optimizer seed:   x=249.533 mm, z=90.653 mm, radius=6.955 mm, J=2.0828e-03
grid-polish best: x=250.000 mm, z=89.750 mm, radius=6.000 mm, J=0
polish evals:     1 of 160 configured candidates
stopped early:    true
runtime:          15.8 s total, 5.3 s optimizer, 5.3 s polish
NRMS model/data:  0 / 0
```

Interpretation: `--polish-stop-misfit 0` is useful for exact synthetic
experiments where a zero-misfit grid cell exists. For noisy or field data, do
not use zero early stopping; either omit the stop threshold or set a defensible
noise-level threshold.

## Validation

Passed after adding the radius profiler, inversion `--grid-polish`, and
`--polish-stop-misfit` option:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/lam001/miniforge3/envs/FNO/bin/python -m py_compile \
  core/geometry.py core/materials.py gpu/fdtd_gpu_v2.py \
  inversion/single_rebar_pipeline.py run_single_rebar_inversion.py \
  run_single_rebar_objective_landscape.py run_single_rebar_radius_profile.py \
  core/run_outputs.py tests/test_gpu_cpml_parity.py \
  tests/test_single_rebar_pipeline.py tests/test_fdtd_basic.py

/home/lam001/miniforge3/envs/FNO/bin/python tests/test_fdtd_basic.py
# 6 passed, 0 failed

/home/lam001/miniforge3/envs/FNO/bin/python tests/test_single_rebar_pipeline.py
# 2 passed, 0 failed

/home/lam001/miniforge3/envs/FNO/bin/python tests/test_gpu_cpml_parity.py
# 2 passed, 0 failed
```

## 015 - full staged Powell plus grid polish

Purpose: run the production-shaped staged 1 mm refinement from the 2 mm coarse
seed, now with `--grid-polish` enabled. This repeats run 009 with the new
post-optimizer stage.

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_inversion.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --optimizer powell \
  --max-iter 10 \
  --max-evals 50 \
  --run-name single_rebar_grid1mm_powell_gridpolish_from_2mm \
  --init-x-mm 252.5 \
  --init-z-mm 91.8 \
  --init-radius-mm 6.76 \
  --x-bounds-mm 220,280 \
  --z-bounds-mm 70,110 \
  --radius-bounds-mm 4,10 \
  --grid-polish \
  --polish-x-half-window-mm 0 \
  --polish-z-half-window-mm 1.0 \
  --polish-radius-half-window-mm 1.0 \
  --polish-x-step-mm 1.0 \
  --polish-z-step-mm 0.25 \
  --polish-radius-step-mm 0.1 \
  --polish-progress-every 25
```

Output:

```text
outputs/experiments/015_single_rebar_grid1mm_powell_gridpolish_from_2mm/
```

Result:

```text
Powell result:    x=249.533 mm, z=90.653 mm, radius=6.955 mm, J=2.0828e-03
grid-polish best: x=250.000 mm, z=89.750 mm, radius=6.000 mm, J=0
recovered:        x=250.000 mm, z=89.750 mm, radius=6.000 mm
NRMS model:       0
NRMS data:        0
runtime:          1123.7 s total, 265.6 s optimizer, 852.7 s polish
```

Interpretation: the full staged run confirms the production path. Powell gets
close in x/z and data fit but remains radius-biased; grid polish resolves the
hard-grid rasterized geometry exactly.

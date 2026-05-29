# Experiment 14: Grid-Polish Speed Worklog

## Goal

Experiment 12 proved that local grid polish fixes the radius bias in the exact
single-rebar synthetic case. Experiment 13 showed the same correction still
works with controlled 1% and 5% observed-data noise.

The remaining practical issue is runtime. The fine polish used in those runs
evaluates 160 nearby candidates. That is acceptable for audit runs, but too
expensive as a default inner loop if we will run many development iterations.

This experiment tests whether a coarser local polish grid can recover the same
geometry with fewer forward solves.

## Plain Terms

- **Fine polish**: the existing local search with `z` step 0.25 mm and radius
  step 0.1 mm. In the current single-x setup this evaluates 160 candidates.
- **Coarse polish**: a cheaper local search with `z` step 0.5 mm and radius
  step 0.2 mm. In the same window this evaluates about 40 candidates.
- **Forward solve**: one simulated B-scan for one candidate geometry. This is
  the expensive unit of work.
- **Acceptable outcome**: the coarse search recovers the same rasterized model
  as fine polish, or gets close enough that a small second fine pass would be
  justified.

## Working Rules

- Use `/home/lam001/miniforge3/envs/FNO/bin/python`.
- Store outputs under `outputs/experiments/NNN_<run_name>/`.
- Do not assume early stopping is available for field-style data. A speed
  improvement should be measured without relying on a guessed noise threshold.

## Plan

1. Run a 5% noise production-shaped refinement from the same 2 mm seed used in
   experiment 13, but replace the 160-candidate fine polish with a 40-candidate
   coarse polish.
2. Compare recovered geometry, objective, model NRMS, data NRMS, polish
   evaluations, and runtime against run 018 from experiment 13.
3. If coarse polish is good enough, document it as the default cheap polish.
   If it fails or lands near the right basin but not the exact model, add a
   staged coarse-to-fine polish option.

## Run Log

### 020 - 5% noise production run with coarse polish

Purpose: repeat the 5% noisy production-shaped run from experiment 13, but use
a cheaper polish grid. This isolates whether the 160-candidate fine polish is
needed for the current one-rebar case.

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_inversion.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --optimizer powell \
  --max-iter 10 \
  --max-evals 50 \
  --run-name single_rebar_grid1mm_noise05_coarsepolish \
  --init-x-mm 252.5 \
  --init-z-mm 91.8 \
  --init-radius-mm 6.76 \
  --x-bounds-mm 220,280 \
  --z-bounds-mm 70,110 \
  --radius-bounds-mm 4,10 \
  --observed-noise-rms-fraction 0.05 \
  --noise-seed 13 \
  --grid-polish \
  --polish-x-half-window-mm 0 \
  --polish-z-half-window-mm 1.0 \
  --polish-radius-half-window-mm 1.0 \
  --polish-x-step-mm 1.0 \
  --polish-z-step-mm 0.5 \
  --polish-radius-step-mm 0.2 \
  --polish-progress-every 10
```

Output:

```text
outputs/experiments/020_single_rebar_grid1mm_noise05_coarsepolish/
```

Result:

```text
noise:             5% observed B-scan RMS, seed=13
Powell result:     x=249.546 mm, z=90.635 mm, radius=6.973 mm, J=6.0876e-02
coarse polish:     x=250.000 mm, z=90.000 mm, radius=6.000 mm, J=5.8565e-02
recovered:         x=250.000 mm, z=90.000 mm, radius=6.000 mm
NRMS model:        0
NRMS data:         5.021%
polish evals:      40
polish runtime:    215.8 s
total runtime:     490.5 s
```

Comparison with run 018 from experiment 13:

```text
fine polish:       160 evals, 854.5 s polish, 1126.7 s total
coarse polish:      40 evals, 215.8 s polish,  490.5 s total
same objective:    5.8565e-02
same model NRMS:   0
```

Interpretation: for this 5% noisy seed, the cheaper grid is enough. The best
coarse candidate gives the same objective and same rasterized material model as
the fine run. The reported depth differs by 0.25 mm (`90.0 mm` vs `89.75 mm`),
but both depths produce the same model mask on the 1 mm grid.

This makes the coarse polish a better default development loop than the fine
160-candidate polish. Fine polish should still be kept as an audit option or as
the second stage if a coarse run lands near, but not exactly on, the best
radius/depth basin.

### 021 - second 5% noise seed with coarse polish

Purpose: check whether run 020's coarse-polish success was specific to one
noise realization.

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_inversion.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --optimizer powell \
  --max-iter 10 \
  --max-evals 50 \
  --run-name single_rebar_grid1mm_noise05_seed21_coarsepolish \
  --init-x-mm 252.5 \
  --init-z-mm 91.8 \
  --init-radius-mm 6.76 \
  --x-bounds-mm 220,280 \
  --z-bounds-mm 70,110 \
  --radius-bounds-mm 4,10 \
  --observed-noise-rms-fraction 0.05 \
  --noise-seed 21 \
  --grid-polish \
  --polish-x-half-window-mm 0 \
  --polish-z-half-window-mm 1.0 \
  --polish-radius-half-window-mm 1.0 \
  --polish-x-step-mm 1.0 \
  --polish-z-step-mm 0.5 \
  --polish-radius-step-mm 0.2 \
  --polish-progress-every 10
```

Output:

```text
outputs/experiments/021_single_rebar_grid1mm_noise05_seed21_coarsepolish/
```

Result:

```text
noise:             5% observed B-scan RMS, seed=21
Powell result:     x=249.664 mm, z=90.634 mm, radius=6.976 mm, J=5.9899e-02
coarse polish:     x=250.000 mm, z=90.000 mm, radius=6.000 mm, J=5.7724e-02
recovered:         x=250.000 mm, z=90.000 mm, radius=6.000 mm
NRMS model:        0
NRMS data:         4.983%
polish evals:      40
polish runtime:    213.0 s
total runtime:     483.6 s
```

Interpretation: the second 5% noise seed agrees with run 020. Powell again
lands in the high-radius basin, and the coarse polish again recovers the true
rasterized geometry without relying on an early-stop threshold.

### Interim note after run 021

The coarse grid-polish recipe now has two 5% noise-seed checks:

```text
seed 13: x=250.0 mm, z=90.0 mm, radius=6.0 mm, model NRMS=0
seed 21: x=250.0 mm, z=90.0 mm, radius=6.0 mm, model NRMS=0
```

For routine development, this is a better tradeoff than the original fine
polish:

```text
recommended routine polish:
  --polish-z-step-mm 0.5
  --polish-radius-step-mm 0.2

audit/final polish:
  --polish-z-step-mm 0.25
  --polish-radius-step-mm 0.1
```

The next useful stress test is 10% observed-data noise. That will tell us where
the current one-rebar synthetic setup starts to become ambiguous.

### 022 - 10% noise stress run with coarse polish

Purpose: stress the coarse-polish recipe beyond the moderate 5% noise cases.
This should be read as a breaking-point probe, not as the expected operating
level.

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_inversion.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --optimizer powell \
  --max-iter 10 \
  --max-evals 50 \
  --run-name single_rebar_grid1mm_noise10_coarsepolish \
  --init-x-mm 252.5 \
  --init-z-mm 91.8 \
  --init-radius-mm 6.76 \
  --x-bounds-mm 220,280 \
  --z-bounds-mm 70,110 \
  --radius-bounds-mm 4,10 \
  --observed-noise-rms-fraction 0.10 \
  --noise-seed 13 \
  --grid-polish \
  --polish-x-half-window-mm 0 \
  --polish-z-half-window-mm 1.0 \
  --polish-radius-half-window-mm 1.0 \
  --polish-x-step-mm 1.0 \
  --polish-z-step-mm 0.5 \
  --polish-radius-step-mm 0.2 \
  --polish-progress-every 10
```

Output:

```text
outputs/experiments/022_single_rebar_grid1mm_noise10_coarsepolish/
```

Result:

```text
noise:             10% observed B-scan RMS, seed=13
Powell result:     x=249.720 mm, z=90.617 mm, radius=6.991 mm, J=2.0142e-01
coarse polish:     x=250.000 mm, z=90.000 mm, radius=6.000 mm, J=1.9916e-01
recovered:         x=250.000 mm, z=90.000 mm, radius=6.000 mm
NRMS model:        0
NRMS data:         10.005%
polish evals:      40
polish runtime:    214.4 s
total runtime:     487.1 s
```

Interpretation: the coarse polish still recovers the true rasterized geometry
for this 10% noise seed. The objective margin is small:

```text
true-radius coarse candidate:  J=1.9916e-01
Powell high-radius basin:      J=2.0142e-01
margin:                        about 2.3e-03
```

That means 10% noise should be treated as an ambiguous regime until more seeds
or a larger scan/source configuration are tested.

## Final State For This Work Loop

The best routine development command should use coarse local polish:

```text
--grid-polish --grid-polish-preset coarse
```

This keeps the radius correction that fixed run 009, while reducing polish cost
from 160 candidates to 40 candidates for the current one-x local setup.

Fine polish remains useful for final/audit runs:

```text
--grid-polish --grid-polish-preset fine
```

Next development direction: make the pipeline automatically choose coarse
polish first, then optionally run fine polish only when the coarse best is near
a competing candidate or when the user requests final audit quality.

## Code Change: Top Polish Candidates

After the 10% stress run, I added `top_candidates` metadata to the grid-polish
result. The previous metadata only recorded the best candidate. The new field
keeps the best few candidates sorted by objective:

```text
grid_polish.top_candidates:
  - misfit
  - params: x_mm, z_mm, radius_mm
```

The CLI option is:

```text
--polish-top-k 8
```

Why this matters: the 10% stress run recovered the right model, but the margin
over the high-radius basin was small. Saving the top candidates makes that
margin auditable in future runs and gives the later automatic coarse-then-fine
policy a clean signal.

I also added a grid-polish preset so the routine 40-candidate configuration can
be requested without spelling out all step-size flags:

```text
--grid-polish --grid-polish-preset coarse
```

Explicit polish flags still override the preset. The original fine behavior is
available as:

```text
--grid-polish --grid-polish-preset fine
```

## Validation

Passed after adding `top_candidates` metadata and polish presets:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/lam001/miniforge3/envs/FNO/bin/python -m py_compile \
  core/geometry.py core/materials.py gpu/fdtd_gpu_v2.py \
  inversion/single_rebar_pipeline.py run_single_rebar_inversion.py \
  run_single_rebar_objective_landscape.py run_single_rebar_radius_profile.py \
  core/run_outputs.py tests/test_gpu_cpml_parity.py \
  tests/test_single_rebar_pipeline.py tests/test_fdtd_basic.py tests/test_grid_polish.py

/home/lam001/miniforge3/envs/FNO/bin/python tests/test_grid_polish.py
# 5 passed, 0 failed

/home/lam001/miniforge3/envs/FNO/bin/python tests/test_fdtd_basic.py
# 6 passed, 0 failed

/home/lam001/miniforge3/envs/FNO/bin/python tests/test_single_rebar_pipeline.py
# 2 passed, 0 failed

/home/lam001/miniforge3/envs/FNO/bin/python tests/test_gpu_cpml_parity.py
# 2 passed, 0 failed
```

### 023 - 10% coarse polish rerun with top candidates

Purpose: regenerate the 10% stress coarse-polish result after adding
`top_candidates` metadata. This starts from run 022's Powell endpoint and only
runs one optimizer evaluation before the 40-candidate polish.

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_inversion.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --optimizer powell \
  --max-iter 1 \
  --max-evals 1 \
  --run-name single_rebar_grid1mm_noise10_coarsepolish_topk \
  --init-x-mm 249.7198908118568 \
  --init-z-mm 90.6168011961733 \
  --init-radius-mm 6.991116714813948 \
  --x-bounds-mm 220,280 \
  --z-bounds-mm 70,110 \
  --radius-bounds-mm 4,10 \
  --observed-noise-rms-fraction 0.10 \
  --noise-seed 13 \
  --grid-polish \
  --polish-x-half-window-mm 0 \
  --polish-z-half-window-mm 1.0 \
  --polish-radius-half-window-mm 1.0 \
  --polish-x-step-mm 1.0 \
  --polish-z-step-mm 0.5 \
  --polish-radius-step-mm 0.2 \
  --polish-progress-every 10 \
  --polish-top-k 8
```

Output:

```text
outputs/experiments/023_single_rebar_grid1mm_noise10_coarsepolish_topk/
```

Result:

```text
noise:             10% observed B-scan RMS, seed=13
optimizer seed:    x=249.720 mm, z=90.617 mm, radius=6.991 mm, J=2.0142e-01
coarse polish:     x=250.000 mm, z=90.000 mm, radius=6.000 mm, J=1.9916e-01
recovered:         x=250.000 mm, z=90.000 mm, radius=6.000 mm
NRMS model:        0
NRMS data:         10.005%
polish evals:      40
polish runtime:    213.6 s
total runtime:     224.3 s
```

Top polish candidates:

```text
rank  J             x_mm   z_mm   radius_mm
1     1.991582715e-01 250.0 90.0  6.0
2     1.991582715e-01 250.0 90.5  6.0
3     1.997176498e-01 250.0 90.0  6.2
4     1.997176498e-01 250.0 90.5  6.2
5     2.014225497e-01 250.0 91.0  6.8
6     2.018331652e-01 250.0 91.0  7.0
7     2.024074686e-01 250.0 90.0  6.4
8     2.024074686e-01 250.0 90.5  6.4
```

Interpretation: the selected radius is stable at 6.0 mm, but the local
uncertainty is visible. Radius 6.2 mm is only about `5.6e-04` objective units
above the winner at 10% noise. The `z=90.0` and `z=90.5` ties are expected hard
grid equivalences.

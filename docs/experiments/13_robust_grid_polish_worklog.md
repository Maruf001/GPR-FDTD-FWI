# Experiment 13: Robust Grid-Polish Worklog

## Goal

Take the exact-synthetic single-rebar pipeline from experiment 12 and test
whether the final grid-polish stage is still useful when the data are less
perfect.

Experiment 12 showed:

```text
2 mm bounded global search
-> 1 mm local continuous refinement
-> 1 mm deterministic local grid polish
```

This recovered the correct 1 mm-grid material mask and radius in the exact
synthetic case. The next question is whether this remains a sensible workflow
when observed traces include controlled noise.

## Plain Terms

- **Observed data**: the B-scan traces treated as the measurement.
- **Synthetic data**: the B-scan produced by a candidate rebar geometry.
- **Objective / J**: the mismatch between observed and synthetic data. Lower is
  better. `J=0` means exact match in the current synthetic setup.
- **Grid polish**: a small deterministic search over nearby x, z, and radius
  values after a continuous optimizer has found an approximate solution.
- **Hard-grid rasterization**: the circle is represented by grid cells. Nearby
  physical positions can produce exactly the same cell mask.
- **Noise robustness**: whether the method still recovers plausible geometry
  after small random perturbations are added to observed traces.

## Working Rules

- Use `/home/lam001/miniforge3/envs/FNO/bin/python`.
- Store experiment outputs under `outputs/experiments/NNN_<run_name>/`.
- Record every substantive run here before interpreting or moving on.
- For exact synthetic runs, `--polish-stop-misfit 0` is valid. For noisy runs,
  do not use a zero stop threshold because the true model will not match noisy
  observations exactly.

## Plan

1. Add a plain-language report that explains experiments 11 and 12.
2. Add lightweight unit coverage for the grid-polish helper.
3. Add controlled observed-data noise to the single-rebar engine and CLI.
4. Run short noisy staged refinements from the known coarse seed.
5. Decide whether production grid polish should use full-grid evaluation, early
   stopping, or a noise-aware threshold.

## Run Log

### 017 - grid-polish helper tests

Purpose: validate the grid-polish helper and no-noise code path after adding
observation-noise support.

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python tests/test_grid_polish.py
```

Result:

```text
tests/test_grid_polish.py: 3 passed, 0 failed
```

### 018 - 1% observed-noise staged refinement

Purpose: run a noisy 1 mm staged refinement from the 2 mm coarse seed with a
small noise level. This should test whether full grid polish still picks the
true rasterized geometry or overfits noise.

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_inversion.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --optimizer powell \
  --max-iter 10 \
  --max-evals 50 \
  --run-name single_rebar_grid1mm_noise01_gridpolish \
  --init-x-mm 252.5 \
  --init-z-mm 91.8 \
  --init-radius-mm 6.76 \
  --x-bounds-mm 220,280 \
  --z-bounds-mm 70,110 \
  --radius-bounds-mm 4,10 \
  --observed-noise-rms-fraction 0.01 \
  --noise-seed 13 \
  --grid-polish \
  --polish-x-half-window-mm 0 \
  --polish-z-half-window-mm 1.0 \
  --polish-radius-half-window-mm 1.0 \
  --polish-x-step-mm 1.0 \
  --polish-z-step-mm 0.25 \
  --polish-radius-step-mm 0.1
```

Output:

```text
outputs/experiments/017_single_rebar_grid1mm_noise01_gridpolish/
```

Result:

```text
noise:           1% observed B-scan RMS, seed=13
Powell result:   x=249.505 mm, z=90.649 mm, radius=6.958 mm, J=4.6353e-03
polish result:   x=250.000 mm, z=89.750 mm, radius=6.000 mm, J=2.4833e-03
recovered:       x=250.000 mm, z=89.750 mm, radius=6.000 mm
NRMS model:      0
NRMS data:       1.005%
polish evals:    160
```

Interpretation: 1% noise does not break the grid-polish stage. The best
polished candidate is still the true rasterized geometry. The data NRMS is at
the injected noise level, as expected.

### 019 - 5% observed-noise staged refinement

Purpose: repeat the noisy staged refinement with 5% RMS observed-data noise.
This checks whether full grid polish begins to follow noise instead of geometry.

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_inversion.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --optimizer powell \
  --max-iter 10 \
  --max-evals 50 \
  --run-name single_rebar_grid1mm_noise05_gridpolish \
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
  --polish-z-step-mm 0.25 \
  --polish-radius-step-mm 0.1 \
  --polish-progress-every 25
```

Output:

```text
outputs/experiments/018_single_rebar_grid1mm_noise05_gridpolish/
```

Result:

```text
noise:           5% observed B-scan RMS, seed=13
Powell result:   x=249.546 mm, z=90.635 mm, radius=6.973 mm, J=6.0876e-02
polish result:   x=250.000 mm, z=89.750 mm, radius=6.000 mm, J=5.8565e-02
recovered:       x=250.000 mm, z=89.750 mm, radius=6.000 mm
NRMS model:      0
NRMS data:       5.021%
polish evals:    160
```

Interpretation: even at 5% additive observed-data noise, full grid polish
still prefers the true rasterized geometry over the Powell high-radius basin.
The margin is small, so noisy runs should not use a zero stop threshold.

### 020 - 5% noise-aware early-stop polish

Purpose: test a noise-aware polish stop threshold for the 5% noisy case. This
uses the known noise-floor objective from run 019 and stops once polish reaches
`J <= 0.06`.

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_inversion.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --optimizer powell \
  --max-iter 1 \
  --max-evals 1 \
  --run-name single_rebar_grid1mm_noise05_gridpolish_stop006 \
  --init-x-mm 249.5333604898392 \
  --init-z-mm 90.65264829814728 \
  --init-radius-mm 6.954785108476757 \
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
  --polish-z-step-mm 0.25 \
  --polish-radius-step-mm 0.1 \
  --polish-stop-misfit 0.06
```

Output:

```text
outputs/experiments/019_single_rebar_grid1mm_noise05_gridpolish_stop006/
```

Result:

```text
noise:             5% observed B-scan RMS, seed=13
optimizer seed:    x=249.533 mm, z=90.653 mm, radius=6.955 mm, J=6.0876e-02
stop threshold:    J <= 6.0000e-02
polish result:     x=250.000 mm, z=89.750 mm, radius=6.000 mm, J=5.8565e-02
polish evals:      1 of 160 configured candidates
stopped early:     true
runtime:           15.9 s total
NRMS model/data:   0 / 5.021%
```

Interpretation: a noise-aware stop threshold can make polish cheap once the
noise floor is known or estimated. This threshold should not be guessed blindly
for field data. Full grid polish is safer when the noise floor is unknown.

## Current Conclusion

The grid-polish stage remains useful under controlled 1% and 5% observed-data
noise for this one-rebar synthetic case. In both noisy runs, continuous Powell
landed in the same high-radius basin, while grid polish recovered the true
rasterized radius.

Practical guidance:

- Exact synthetic data: `--polish-stop-misfit 0` is safe and fast.
- Known-noise synthetic data: a stop threshold near the expected noise floor can
  be fast, but full polish is safer for audit runs.
- Unknown/noisy field data: do not stop early unless a defensible noise-floor
  threshold has been estimated.

## Validation

Passed after adding observed-data noise support and grid-polish helper tests:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/lam001/miniforge3/envs/FNO/bin/python -m py_compile \
  core/geometry.py core/materials.py gpu/fdtd_gpu_v2.py \
  inversion/single_rebar_pipeline.py run_single_rebar_inversion.py \
  run_single_rebar_objective_landscape.py run_single_rebar_radius_profile.py \
  core/run_outputs.py tests/test_gpu_cpml_parity.py \
  tests/test_single_rebar_pipeline.py tests/test_fdtd_basic.py tests/test_grid_polish.py

/home/lam001/miniforge3/envs/FNO/bin/python tests/test_grid_polish.py
# 3 passed, 0 failed

/home/lam001/miniforge3/envs/FNO/bin/python tests/test_fdtd_basic.py
# 6 passed, 0 failed

/home/lam001/miniforge3/envs/FNO/bin/python tests/test_single_rebar_pipeline.py
# 2 passed, 0 failed

/home/lam001/miniforge3/envs/FNO/bin/python tests/test_gpu_cpml_parity.py
# 2 passed, 0 failed
```

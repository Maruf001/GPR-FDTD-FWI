# Experiment 18: Cumulative Frequency Diagnostics

## Goal

Adapt the WRI paper's cumulative-frequency idea to the current time-domain
single-rebar pipeline without building a new frequency-domain WRI solver.

The first step is diagnostic, not a new optimizer:

```text
save the normalized objective contribution from each center frequency
for final models and grid-polish top candidates.
```

This lets us ask which frequency content favors the high-radius basin and
whether a cumulative schedule should weight or stage frequencies differently.

## Plain Terms

- **Per-frequency misfit**: the objective value split by source wavelet center
  frequency instead of only averaged into one number.
- **Cumulative frequency schedule**: optimize with one frequency, then two,
  then three, carrying the previous result forward.
- **Why this matters**: radius ambiguity may be driven by one part of the
  spectrum. We need to see that before adding OT or WRI machinery.

## Code Changes

Updated:

```text
inversion/single_rebar_pipeline.py
run_single_rebar_inversion.py
tests/test_single_rebar_pipeline.py
```

New summary fields:

```text
objective_misfit_average
objective_misfit_by_frequency
objective_frequency_weights
grid_polish.top_candidates[*].misfit_by_frequency
```

New CLI flag:

```text
--frequency-weights W1,W2,...
```

Weights are non-negative and must match `--frequencies-ghz`. The objective is
the weighted average of the per-frequency normalized misfits. Default behavior
is unchanged because all frequencies use equal weight.

## Run Log

### 038 - summary smoke, 1.0+1.5 GHz

Purpose: verify that final summaries report per-frequency objective
contributions.

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_inversion.py \
  --backend gpu-cpml \
  --sources 1 \
  --frequencies-ghz 1.0,1.5 \
  --max-iter 1 \
  --max-evals 1 \
  --run-name cumulative_frequency_misfit_summary_smoke \
  --optimizer powell
```

Output:

```text
outputs/experiments/038_cumulative_frequency_misfit_summary_smoke/
```

Result:

```text
best J average: 3.9839e-02
1.0 GHz J:      3.8919e-03
1.5 GHz J:      7.5786e-02
```

The average is the mean of the per-frequency values. This verifies that the
summary can expose which frequency dominates the objective.

### 039 - top-candidate smoke, 1.0+1.5 GHz

Purpose: verify that local grid-polish top candidates include per-frequency
misfit.

Output:

```text
outputs/experiments/039_cumulative_frequency_gridpolish_topk_smoke/
```

Result:

```text
grid_polish.top_candidates[0].misfit_by_frequency:
  1.0 GHz: 0
  1.5 GHz: 0
```

This run used the true model and a one-point polish grid, so zero misfit is
expected.

### 040 - exact data, 1.0+1.5 GHz coarse polish from high-radius seed

Purpose: test whether adding a lower center frequency improves radius
separation in the known high-radius local basin.

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_inversion.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequencies-ghz 1.0,1.5 \
  --optimizer powell \
  --max-iter 1 \
  --max-evals 1 \
  --run-name cumulative_frequency_10_15_coarsepolish_from_highradius \
  --init-x-mm 249.53336048978386 \
  --init-z-mm 90.6526482993157 \
  --init-radius-mm 6.954785109185667 \
  --x-bounds-mm 220,280 \
  --z-bounds-mm 70,110 \
  --radius-bounds-mm 4,10 \
  --grid-polish \
  --grid-polish-preset coarse \
  --polish-top-k 10
```

Output:

```text
outputs/experiments/040_cumulative_frequency_10_15_coarsepolish_from_highradius/
```

Result:

```text
recovered:      x=250.000 mm, z=90.000 mm, radius=6.000 mm
best J:         0
runtime:        451.6 s
polish evals:   40
```

Top polish candidates:

```text
rank  avg J       1.0 GHz J    1.5 GHz J    x_mm   z_mm   radius_mm
1     0           0            0            250.0  90.0   6.0
2     0           0            0            250.0  90.5   6.0
3     5.3636e-04  3.5600e-05   1.0371e-03  250.0  90.0   6.2
4     5.3636e-04  3.5600e-05   1.0371e-03  250.0  90.5   6.2
5     1.0846e-03  8.6443e-05   2.0828e-03  250.0  91.0   6.8
6     1.5228e-03  1.3017e-04   2.9154e-03  250.0  91.0   7.0
```

Interpretation:

```text
1.0 GHz is much less sensitive to the small radius differences than 1.5 GHz.
For r=6.2 mm, the 1.0 GHz penalty is only 3.56e-05 while the 1.5 GHz penalty
is 1.037e-03.
```

So a simple unweighted average of 1.0+1.5 GHz dilutes radius separation. It
still recovers the exact model because the true candidate has zero misfit, but
it makes the near-radius margin smaller than the 1.5 GHz-only objective.

### 041 - weighted objective smoke, 1.0+1.5 GHz

Purpose: verify the new frequency-weighted objective path.

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_inversion.py \
  --backend gpu-cpml \
  --sources 1 \
  --frequencies-ghz 1.0,1.5 \
  --frequency-weights 0.2,1.0 \
  --max-iter 1 \
  --max-evals 1 \
  --run-name cumulative_frequency_weighted_objective_smoke \
  --optimizer powell
```

Output:

```text
outputs/experiments/041_cumulative_frequency_weighted_objective_smoke/
```

Result:

```text
weighted average J: 6.3804e-02
1.0 GHz weight/J:   0.2 / 3.8919e-03
1.5 GHz weight/J:   1.0 / 7.5786e-02
```

This matches:

```text
(0.2 * J_1.0GHz + 1.0 * J_1.5GHz) / 1.2
```

Post-hoc weighted margins from run 040, using the same weights:

```text
rank  unweighted J  weighted J   x_mm   z_mm   radius_mm
1     0             0            250.0  90.0   6.0
2     0             0            250.0  90.5   6.0
3     5.3636e-04    8.7020e-04   250.0  90.0   6.2
4     5.3636e-04    8.7020e-04   250.0  90.5   6.2
5     1.0846e-03    1.7501e-03   250.0  91.0   6.8
6     1.5228e-03    2.4512e-03   250.0  91.0   7.0
```

Interpretation: downweighting 1.0 GHz restores much of the higher-frequency
radius separation while still leaving a mechanism to include low-frequency
information during basin selection.

## Current Conclusion

The cumulative-frequency idea should not be implemented as a naive unweighted
average. Lower center frequencies help large-scale basin selection, but they
are weak radius discriminators in this single-rebar setup.

Recommended next implementation:

```text
Use low frequencies for early x-z basin stages.
Use higher-frequency-weighted objectives or full-band polish for radius
selection.
Run a controlled weighted multi-frequency polish under 10% noise if the
unweighted noisy margin is still too small.
```

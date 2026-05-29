# Experiment 16: Progressive Bandwidth Objective Schedule

## Goal

Adapt the 2021 PEBDD paper idea to the current time-domain single-rebar
pipeline:

```text
filter both observed and synthetic traces in the objective,
start with a limited bandwidth,
progressively expand the bandwidth,
then finish with full-band least squares and coarse grid polish.
```

This is not a full reproduction of the crosshole PEBDD paper. It is the
lowest-risk adaptation that reuses our existing FDTD solver and geometry
pipeline.

## Plain Terms

- **Objective bandpass**: a frequency filter applied only when computing the
  inversion objective. Saved final B-scans and NRMS still use the full traces.
- **Progressive bandwidth**: use a narrower band first, then expand to include
  more waveform detail.
- **Success target**: reduce the high-radius Powell bias before grid polish, or
  improve the final top-candidate margin.

## Code Changes

Added:

```text
inversion/trace_filters.py
tests/test_trace_filters.py
```

Updated:

```text
inversion/single_rebar_pipeline.py
run_single_rebar_inversion.py
```

New CLI flags:

```text
--objective-bandpass-ghz LOW,HIGH
--objective-bandpass-taper-ghz TAPER
```

The filter is applied symmetrically to observed and synthetic traces before
the residual is computed.

## Run Log

### 028 - bandpass objective smoke

Purpose: verify the filtered objective path and summary metadata.

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_inversion.py \
  --backend gpu-cpml \
  --sources 1 \
  --max-iter 1 \
  --max-evals 1 \
  --run-name bandpass_objective_summary_smoke \
  --optimizer powell \
  --objective-bandpass-ghz 0.2,1.1 \
  --objective-bandpass-taper-ghz 0.05
```

Output:

```text
outputs/experiments/028_bandpass_objective_summary_smoke/
```

Result: `single_rebar_summary.json` contains `objective_bandpass` and
`trace_shift_by_frequency`.

### 029 - stage 1, 0.2-0.8 GHz objective

Purpose: start from the 2 mm-derived seed and run a low-band objective.

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_inversion.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --optimizer powell \
  --max-iter 8 \
  --max-evals 35 \
  --run-name bandwidth_stage1_020_080_from_2mm \
  --init-x-mm 252.5 \
  --init-z-mm 91.8 \
  --init-radius-mm 6.76 \
  --x-bounds-mm 220,280 \
  --z-bounds-mm 70,110 \
  --radius-bounds-mm 4,10 \
  --objective-bandpass-ghz 0.2,0.8 \
  --objective-bandpass-taper-ghz 0.05
```

Output:

```text
outputs/experiments/029_bandwidth_stage1_020_080_from_2mm/
```

Result:

```text
recovered:       x=249.823 mm, z=90.591 mm, radius=6.573 mm
objective:       1.0052e-04 filtered objective
full-data NRMS:  1.068%
runtime:         185.3 s
```

Interpretation: the low-band stage improves the radius basin relative to the
old full-band Powell result (`radius≈6.95 mm`). It does not recover radius
exactly, but it moves the seed closer to the true 6.0 mm radius.

### 030 - stage 2, 0.2-1.1 GHz objective

Purpose: expand the objective bandwidth from the stage-1 result.

Output:

```text
outputs/experiments/030_bandwidth_stage2_020_110_from_stage1/
```

Result:

```text
recovered:       x=249.735 mm, z=90.731 mm, radius=6.864 mm
objective:       8.6533e-05 filtered objective
full-data NRMS:  0.789%
runtime:         185.2 s
```

Interpretation: expanding to 1.1 GHz improves full-data NRMS, but pushes the
radius back toward the high-radius basin. This means the wider-band
least-squares objective is already reintroducing the depth/radius tradeoff.

### 031 - full-band stage from stage 2 plus coarse polish

Purpose: complete the staged schedule with full-band Powell and coarse polish.

Output:

```text
outputs/experiments/031_bandwidth_stage3_full_from_stage2_coarsepolish/
```

Result:

```text
full-band Powell: x=249.533 mm, z=90.653 mm, radius=6.955 mm, J=2.0828e-03
coarse polish:    x=250.000 mm, z=90.000 mm, radius=6.000 mm, J=0
NRMS model/data:  0 / 0
runtime:          361.0 s for this stage
polish evals:     40
```

Top polish candidates:

```text
rank  J             x_mm   z_mm   radius_mm
1     0             250.0  90.0   6.0
2     0             250.0  90.5   6.0
3     1.0371e-03    250.0  90.0   6.2
4     1.0371e-03    250.0  90.5   6.2
5     2.0828e-03    250.0  91.0   6.8
```

Interpretation: full-band Powell erases the low-band radius improvement and
returns to the same high-radius basin as run 009. Grid polish still fixes the
model.

### 032 - full-band control from stage 1, no polish

Purpose: determine whether stage 2 caused the regression or whether full-band
Powell itself causes it.

Output:

```text
outputs/experiments/032_bandwidth_full_from_stage1_no_polish/
```

Result:

```text
initial seed:     x=249.823 mm, z=90.591 mm, radius=6.573 mm
full-band result: x=249.533 mm, z=90.653 mm, radius=6.955 mm
objective:        2.0828e-03
full-data NRMS:   0.789%
runtime:          263.6 s
```

Interpretation: the full-band Powell objective pulls the improved stage-1 seed
back to the old high-radius basin. The issue is not stage 2 specifically.

### 033 - stage 1 seed directly to full-band coarse polish

Purpose: test a pragmatic adaptation: use low-band Powell only to get a better
local seed, then skip full-band Powell and run full-band coarse polish.

Output:

```text
outputs/experiments/033_bandwidth_stage1_then_full_coarsepolish/
```

Result:

```text
stage-1 seed:      x=249.823 mm, z=90.591 mm, radius=6.573 mm
coarse polish:     x=250.000 mm, z=90.000 mm, radius=6.000 mm, J=0
NRMS model/data:   0 / 0
polish evals:      40
stage runtime:     215.9 s
combined runtime:  401.2 s including run 029
```

Interpretation: this is the best PEBDD-style result from this work loop.
Progressive bandwidth did not make full-band Powell radius-accurate, but the
low-band stage produced a better seed that can go directly to full-band grid
polish. That avoids the full-band Powell step that reintroduces the radius
bias.

## Current Conclusion

The simple PEBDD-style objective filter gives a useful low-band seed, but a
standard expanded/full-band Powell stage still prefers the high-radius
depth/radius basin.

Recommended exact-synthetic workflow from this experiment:

```text
2 mm coarse seed
-> 1 mm low-band Powell objective, 0.2-0.8 GHz
-> full-band coarse grid polish
```

This recovered the exact model and took about 401 s across runs 029 and 033.
It is faster than the previous full Powell plus coarse polish shape, but it
still depends on deterministic polish for the final radius.

Do not claim that progressive bandwidth alone solves radius estimation. It
does not. Its current value is to provide a better local seed and justify
skipping a full-band Powell refinement that is known to reintroduce bias.

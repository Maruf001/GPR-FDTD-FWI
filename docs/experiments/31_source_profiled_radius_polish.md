# Experiment 31: Source-Profiled Radius Polish

## Goal

Turn the source-mismatch lesson from Experiment 26 into a production-style
single-rebar local polish step.

The target use case is:

```text
given a good x/z basin from the existing staged pipeline,
choose radius using a local grid,
profile low-dimensional source nuisance parameters,
report top-k candidates and distinct-radius confidence.
```

This is Stage 1 of the post-summary plan. Stage 2 should not start until this
runner passes focused tests, exact-data smoke, controlled source-mismatch
smoke, tracker documentation, and plot validation.

## Paper Link

This follows the five-paper synthesis:

```text
PEBDD / cumulative bandwidth:
  source and bandwidth must be handled explicitly before trusting high-frequency
  radius evidence

OT-LS:
  final accuracy should still come from LS after basin issues are controlled

Quadratic W2:
  W2 was tested as an objective-landscape candidate but did not beat LS for the
  single-rebar radius gate
```

## Code Changes

Added:

```text
inversion/source_profile.py
run_single_rebar_source_profiled_polish.py
tests/test_source_profile.py
tests/test_source_profiled_polish_runner.py
```

The runner evaluates a local x/z/r grid and profiles:

```text
center-frequency scale,
global source time shift,
scalar amplitude.
```

Outputs:

```text
data/source_profiled_polish_candidates.csv
data/source_profiled_polish_summary.json
figures/source_profiled_radius_profile.png
```

## Validation Before GPU Runs

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest \
  tests/test_source_profiled_polish_runner.py \
  tests/test_source_profile.py \
  -q
```

Result:

```text
8 passed
```

Compile check:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -m py_compile \
  run_single_rebar_source_profiled_polish.py \
  inversion/source_profile.py
```

Result:

```text
passed
```

## Stage 1 Decision Gates

- [x] Add source-profile helper tests.
- [x] Add runner helper tests.
- [x] Pass focused tests and compile checks.
- [x] Run exact-data nominal smoke.
- [x] Validate exact-data radius plot.
- [x] Run controlled combined source-mismatch smoke.
- [x] Validate mismatch radius plot.
- [x] Update the master plan ledger.
- [x] Decide whether Stage 2 replication can use this runner.

## Planned Runs

### Nominal exact-data smoke

Purpose:

```text
Confirm the production runner reproduces the known exact synthetic behavior
with no source mismatch.
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_source_profiled_polish.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --x-values-mm 250.0 \
  --z-values-mm 90.0,90.5,91.0 \
  --radius-values-mm 5.8:6.4:0.2 \
  --source-frequency-scales 1.0 \
  --source-time-shift-ps-values 0 \
  --fit-amplitude \
  --run-name source_profiled_polish_nominal_smoke
```

### Controlled combined source-mismatch smoke

Purpose:

```text
Confirm amplitude + time-shift + center-frequency profiling recovers radius
when the observed source is intentionally mismatched.
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_source_profiled_polish.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --x-values-mm 250.0 \
  --z-values-mm 90.0,90.5,91.0,91.5 \
  --radius-values-mm 5.4:7.8:0.2 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-80,-50,-25,0,25,50,80 \
  --fit-amplitude \
  --observed-frequency-scale 1.1 \
  --observed-time-shift-ps -50 \
  --observed-amplitude-scale 1.1 \
  --run-name source_profiled_polish_combined_mismatch
```

## Running Log

### 057_source_profiled_polish_nominal_smoke

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_source_profiled_polish.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --x-values-mm 250.0 \
  --z-values-mm 90.0,90.5,91.0 \
  --radius-values-mm 5.8:6.4:0.2 \
  --source-frequency-scales 1.0 \
  --source-time-shift-ps-values 0 \
  --fit-amplitude \
  --run-name source_profiled_polish_nominal_smoke
```

Output:

```text
outputs/experiments/057_source_profiled_polish_nominal_smoke
```

Runtime and count:

```text
12 candidates
58.75 s
```

Result:

| Rank | x [mm] | z [mm] | r [mm] | J | source fc scale | shift [ps] | amp |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 250.0 | 90.0 | 6.0 | 0.000e+00 | 1.0 | 0.0 | 1.000 |
| 2 distinct radius | 250.0 | 90.0 | 6.2 | 9.815e-04 | 1.0 | 0.0 | 0.993 |

Distinct-radius margin:

```text
r=6.0 beats r=6.2 by 9.815e-04
```

Plot validation:

```text
source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 29.570
```

Interpretation:

```text
The production runner reproduces the exact-data radius result. Source profiling
does not damage the nominal case; it leaves frequency scale, time shift, and
amplitude at the true values.
```

Note:

```text
The 90.0 and 90.5 mm z entries can be tied on the 1 mm hard grid because the
geometry snaps to the same cell. This is acceptable for the smoke gate, whose
purpose is radius/source validation, but sub-cell geometry remains relevant for
later fine depth reporting.
```

Next decision:

```text
Run the controlled combined source-mismatch smoke. If the best radius remains
6.0 mm with a reasonable source profile, promote the runner to Stage 2
replication across seeds.
```

### 058_source_profiled_polish_combined_mismatch

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_source_profiled_polish.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --x-values-mm 250.0 \
  --z-values-mm 90.0,90.5,91.0,91.5 \
  --radius-values-mm 5.4:7.8:0.2 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-80,-50,-25,0,25,50,80 \
  --fit-amplitude \
  --observed-frequency-scale 1.1 \
  --observed-time-shift-ps -50 \
  --observed-amplitude-scale 1.1 \
  --run-name source_profiled_polish_combined_mismatch
```

Output:

```text
outputs/experiments/058_source_profiled_polish_combined_mismatch
```

Runtime and count:

```text
52 geometry candidates
3 modeled source-frequency scales per candidate
771.05 s
```

Injected observed-source mismatch:

```text
center-frequency scale: 1.1
time shift:             -50 ps
amplitude scale:        1.1
noise:                  0%
```

Result:

| Rank | x [mm] | z [mm] | r [mm] | J | source fc scale | shift [ps] | amp |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 250.0 | 90.0 | 6.0 | 1.295e-05 | 1.1 | -50.0 | 1.100 |
| 2 tied cell | 250.0 | 90.5 | 6.0 | 1.295e-05 | 1.1 | -50.0 | 1.100 |
| 3 distinct radius | 250.0 | 90.0 | 6.2 | 1.159e-03 | 1.1 | -50.0 | 1.092 |

Distinct-radius margin:

```text
r=6.0 beats r=6.2 by 1.146e-03
```

Plot validation:

```text
source_profiled_radius_profile.png: 1515x886 px, dynamic range 255, std 30.194
```

Interpretation:

```text
The source-profiled polish recovered the true radius while also recovering the
injected nuisance source parameters. This converts the Experiment 26 source
mismatch fix from a diagnostic matrix into a reusable local-polish runner.
```

The best non-true radius in the top list is r=6.2 mm. Larger radii begin to
prefer a shifted source profile around -25 ps, which is a useful warning: source
profiling improves robustness, but the final report still needs top-k candidate
inspection and radius margins rather than only a single best value.

## Stage 1 Decision

Stage 1 passes.

Use `run_single_rebar_source_profiled_polish.py` for Stage 2 replication, with
these controls:

```text
frequency scales:       0.9, 1.0, 1.1
time-shift values:      -80, -50, -25, 0, 25, 50, 80 ps
amplitude profiling:    enabled
radius report:          top-k plus distinct-radius margin
plot validation:        required for every matrix summary
```

The next stage should be a compact replication matrix across noise and source
mismatch cases, not a blind large Cartesian sweep. At roughly 13 minutes per
52-candidate case, a focused matrix gives better research throughput.

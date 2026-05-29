# Experiment 32: Source-Profiled Replication Matrix

## Goal

Replicate the Stage 1 source-profiled local radius polish across a compact set
of noise and source-mismatch cases.

The key question is:

```text
Does the promoted local polish still choose r=6.0 mm when exact data, noisy
data, and source-mismatched data are evaluated in one consistent matrix?
```

## Why A Matrix Runner

The Stage 1 mismatch smoke took about 13 minutes for:

```text
52 geometry candidates
3 modeled source-frequency scales per candidate
```

Running separate commands for each replication case would repeat the same
synthetic FDTD simulations. The Stage 2 runner simulates each candidate/source
scale once, then profiles source nuisance parameters against multiple observed
cases in trace space.

## Code Changes

Added:

```text
run_single_rebar_source_profiled_replication.py
tests/test_source_profiled_replication_runner.py
```

Reused:

```text
inversion/source_profile.py
run_single_rebar_source_profiled_polish.py
```

## Validation Before GPU Run

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest \
  tests/test_source_profiled_replication_runner.py \
  tests/test_source_profiled_polish_runner.py \
  tests/test_source_profile.py \
  -q
```

Result:

```text
13 passed
```

Compile check:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -m py_compile \
  run_single_rebar_source_profiled_replication.py \
  run_single_rebar_source_profiled_polish.py \
  inversion/source_profile.py
```

Result:

```text
passed
```

## Stage 2A Decision Gates

- [x] Add parser/ranking helper tests.
- [x] Reuse Stage 1 source-profile objective.
- [x] Pass focused tests and compile checks.
- [x] Run compact five-case replication matrix.
- [x] Validate matrix radius plot.
- [x] Interpret all case margins and fitted source profiles.
- [x] Update master plan ledger.
- [x] Decide whether Stage 3 seed-offset stress tests can start.

## Planned Compact Matrix

Cases:

| Case | Source fc scale | Shift [ps] | Amp | Noise |
| --- | ---: | ---: | ---: | ---: |
| nominal | 1.0 | 0 | 1.0 | 0% |
| noise05_seed13 | 1.0 | 0 | 1.0 | 5% |
| noise10_seed13 | 1.0 | 0 | 1.0 | 10% |
| source_mismatch | 1.1 | -50 | 1.1 | 0% |
| source_mismatch_noise05_seed13 | 1.1 | -50 | 1.1 | 5% |

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_source_profiled_replication.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --x-values-mm 250.0 \
  --z-values-mm 90.0,90.5,91.0,91.5 \
  --radius-values-mm 5.4:7.8:0.2 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-80,-50,-25,0,25,50,80 \
  --run-name source_profiled_replication_compact
```

Expected runtime:

```text
about 13-15 minutes, because synthetic FDTD work is shared across cases
```

## Running Log

### 059_source_profiled_replication_compact

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_source_profiled_replication.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --x-values-mm 250.0 \
  --z-values-mm 90.0,90.5,91.0,91.5 \
  --radius-values-mm 5.4:7.8:0.2 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-80,-50,-25,0,25,50,80 \
  --run-name source_profiled_replication_compact
```

Output:

```text
outputs/experiments/059_source_profiled_replication_compact
```

Runtime and count:

```text
52 geometry candidates
5 observed cases
3 modeled source-frequency scales per candidate
813.68 s
```

Summary:

| Case | Best r [mm] | Next r [mm] | Margin | Best J | Best source profile |
| --- | ---: | ---: | ---: | ---: | --- |
| nominal | 6.0 | 6.2 | 9.815e-04 | 0.000e+00 | fc=1.0, shift=0 ps, amp=1.000 |
| noise05_seed13 | 6.0 | 6.2 | 7.697e-04 | 5.856e-02 | fc=1.0, shift=0 ps, amp=1.000 |
| noise10_seed13 | 6.0 | 6.2 | 5.236e-04 | 1.992e-01 | fc=1.0, shift=0 ps, amp=1.001 |
| source_mismatch | 6.0 | 6.2 | 1.146e-03 | 1.295e-05 | fc=1.1, shift=-50 ps, amp=1.100 |
| source_mismatch_noise05_seed13 | 6.0 | 6.2 | 9.366e-04 | 6.614e-02 | fc=1.1, shift=-50 ps, amp=1.103 |

Plot validation:

```text
source_profiled_replication_radius_profiles.png: 1651x937 px, dynamic range 255, std 34.054
```

Interpretation:

```text
The compact Stage 2 matrix passes. Noise reduces radius margin monotonically in
the nominal-source cases, but the best distinct radius remains r=6.0 mm through
10% noise. The source-mismatch cases recover the injected nuisance source
parameters and still choose r=6.0 mm.
```

This result is stronger than the Stage 1 smoke because it evaluates exact,
noisy, and source-mismatched observations against the same synthetic candidate
grid. It supports using this matrix runner for broader noise/source seed
replication.

## Stage 2A Decision

Stage 2A passes.

Next action:

```text
Run a seed replication matrix before moving to x/z/r seed-offset stress tests.
Use the same 52-candidate geometry grid and shared synthetic simulations, but
expand observed cases across several noise seeds at 5% and 10%, plus a compact
source-mismatch-noise seed set.
```

## Stage 2B Seed Replication Plan

Purpose:

```text
Quantify whether the accepted source-profiled polish keeps r=6.0 mm across
multiple noise seeds and whether source-mismatch recovery remains stable when
noise is also present.
```

Cases:

```text
nominal
noise05_seed7, noise05_seed13, noise05_seed21, noise05_seed37
noise10_seed7, noise10_seed13, noise10_seed21, noise10_seed37
source_mismatch
source_mismatch_noise05_seed7, source_mismatch_noise05_seed13,
source_mismatch_noise05_seed21
source_mismatch_noise10_seed7, source_mismatch_noise10_seed13,
source_mismatch_noise10_seed21
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_source_profiled_replication.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --replication-cases "nominal:1.0,0.0,1.0,0.0,13|noise05_seed7:1.0,0.0,1.0,0.05,7|noise05_seed13:1.0,0.0,1.0,0.05,13|noise05_seed21:1.0,0.0,1.0,0.05,21|noise05_seed37:1.0,0.0,1.0,0.05,37|noise10_seed7:1.0,0.0,1.0,0.10,7|noise10_seed13:1.0,0.0,1.0,0.10,13|noise10_seed21:1.0,0.0,1.0,0.10,21|noise10_seed37:1.0,0.0,1.0,0.10,37|source_mismatch:1.1,-50.0,1.1,0.0,13|source_mismatch_noise05_seed7:1.1,-50.0,1.1,0.05,7|source_mismatch_noise05_seed13:1.1,-50.0,1.1,0.05,13|source_mismatch_noise05_seed21:1.1,-50.0,1.1,0.05,21|source_mismatch_noise10_seed7:1.1,-50.0,1.1,0.10,7|source_mismatch_noise10_seed13:1.1,-50.0,1.1,0.10,13|source_mismatch_noise10_seed21:1.1,-50.0,1.1,0.10,21" \
  --x-values-mm 250.0 \
  --z-values-mm 90.0,90.5,91.0,91.5 \
  --radius-values-mm 5.4:7.8:0.2 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-80,-50,-25,0,25,50,80 \
  --run-name source_profiled_replication_seed_matrix
```

Decision gate:

```text
Pass if every case selects r=6.0 mm and the 10% noise margins stay positive
against r=6.2 mm. If any seed fails, inspect top-k source profiles before
moving to Stage 3.
```

### 060_source_profiled_replication_seed_matrix

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_single_rebar_source_profiled_replication.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --replication-cases "nominal:1.0,0.0,1.0,0.0,13|noise05_seed7:1.0,0.0,1.0,0.05,7|noise05_seed13:1.0,0.0,1.0,0.05,13|noise05_seed21:1.0,0.0,1.0,0.05,21|noise05_seed37:1.0,0.0,1.0,0.05,37|noise10_seed7:1.0,0.0,1.0,0.10,7|noise10_seed13:1.0,0.0,1.0,0.10,13|noise10_seed21:1.0,0.0,1.0,0.10,21|noise10_seed37:1.0,0.0,1.0,0.10,37|source_mismatch:1.1,-50.0,1.1,0.0,13|source_mismatch_noise05_seed7:1.1,-50.0,1.1,0.05,7|source_mismatch_noise05_seed13:1.1,-50.0,1.1,0.05,13|source_mismatch_noise05_seed21:1.1,-50.0,1.1,0.05,21|source_mismatch_noise10_seed7:1.1,-50.0,1.1,0.10,7|source_mismatch_noise10_seed13:1.1,-50.0,1.1,0.10,13|source_mismatch_noise10_seed21:1.1,-50.0,1.1,0.10,21" \
  --x-values-mm 250.0 \
  --z-values-mm 90.0,90.5,91.0,91.5 \
  --radius-values-mm 5.4:7.8:0.2 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-80,-50,-25,0,25,50,80 \
  --run-name source_profiled_replication_seed_matrix
```

Output:

```text
outputs/experiments/060_source_profiled_replication_seed_matrix
```

Runtime and count:

```text
52 geometry candidates
16 observed cases
3 modeled source-frequency scales per candidate
about 772 s for the candidate grid after observed-case generation
```

Case summary:

| Group | n | Margin min | Margin mean | Margin max | Radius result |
| --- | ---: | ---: | ---: | ---: | --- |
| exact_nominal | 1 | 9.815e-04 | 9.815e-04 | 9.815e-04 | all r=6.0 |
| nominal_noise05 | 4 | 6.902e-04 | 8.793e-04 | 1.045e-03 | all r=6.0 |
| nominal_noise10 | 4 | 3.869e-04 | 5.923e-04 | 7.574e-04 | all r=6.0 |
| exact_mismatch | 1 | 1.146e-03 | 1.146e-03 | 1.146e-03 | all r=6.0 |
| mismatch_noise05 | 3 | 9.366e-04 | 1.011e-03 | 1.137e-03 | all r=6.0 |
| mismatch_noise10 | 3 | 6.715e-04 | 7.952e-04 | 1.004e-03 | all r=6.0 |

Plot validation:

```text
source_profiled_replication_radius_profiles.png: 1651x937 px, dynamic range 255, std 43.127
```

Interpretation:

```text
Stage 2B passes. Every seed case selects r=6.0 mm. The lowest observed margin
is 3.869e-04 for nominal 10% noise seed 21, still positive against the next
distinct radius. Nominal-source noisy cases keep source frequency scale 1.0 and
time shift 0 ps. Source-mismatched noisy cases keep source frequency scale 1.1
and time shift -50 ps.
```

The margins shrink under 10% nominal noise, so later field-data work should not
report radius without a margin table. But for this controlled synthetic stage,
noise/source seed replication is strong enough to move to x/z/r window stress
tests.

## Stage 2B Decision

Stage 2B passes.

Next action:

```text
Start Stage 3 with a wider x/z/r local-window stress test. The goal is no
longer source/noise robustness at fixed location; it is to determine how wide
the final local polish window can be before geometry ambiguity or grid snapping
creates misleading top candidates.
```

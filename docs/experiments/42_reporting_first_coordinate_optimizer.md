# Experiment 42: Reporting-First Coordinate Optimizer

## Goal

Build the first full multi-rebar optimizer branch without losing the reporting
discipline from Stages 6-7.

This is not a blind 9-parameter global optimizer. The first implementation is a
staged coordinate optimizer:

```text
target 0 local x/z/r profile,
update target 0 from ranked candidate,
target 1 local x/z/r profile,
update target 1 from ranked candidate,
target 2 local x/z/r profile,
update target 2 from ranked candidate,
repeat if requested.
```

Every target update must emit:

```text
top-k candidates,
distinct-radius margin,
confidence label,
fallback warning,
ambiguity interval,
source-profile selection.
```

## Initial Design

Use the existing GPU CPML local-geometry machinery:

```text
run_multi_rebar_local_geometry_profile.py
inversion.candidate_confidence
```

Add only the missing pieces:

```text
per-target coordinate state,
window generation around current x/z/r,
non-target radii preserved from current state,
combined per-pass/per-target report.
```

## Decision Gates

CPU smoke gate:

```text
small local windows, one source, CPU backend, exact case.
pass if the runner writes summary, confidence rows, and nonblank plot.
```

GPU gate:

```text
compact windows around a deliberately perturbed seed, GPU CPML backend.
pass if all three target updates recover or move toward true x/z/r and emit
confidence/ambiguity fields.
```

Promotion rule:

```text
Do not treat the optimizer as production-ready unless the combined report
exposes weak-confidence target updates and ambiguity intervals.
```

## Implementation Status

- [x] Added `inversion.multi_rebar_coordinate` for coordinate state, target
  windows, case selection, and state updates.
- [x] Extended `run_multi_rebar_local_geometry_profile.py` so coordinate runs
  can preserve non-target radii from the current state instead of resetting all
  non-target bars to the truth radius.
- [x] Added `run_multi_rebar_coordinate_optimizer.py` with per-step candidate
  CSVs, combined confidence CSV, coordinate state history CSV, summary JSON,
  and validated confidence-margin plot.
- [x] Added focused helper tests, including duplicate-preserving vector parsing
  for coordinate arrays such as `90,90,90` and `6,6,6`.
- [x] Focused validation passed:
  `py_compile` plus 21 tests across coordinate, confidence, and local-geometry
  helper suites.

## 081: CPU CLI/Artifact Smoke

Output:

```text
outputs/experiments/081_coordinate_optimizer_cpu_smoke
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend cpu \
  --grid-step-mm 10.0 \
  --sources 1 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 150,250,350 \
  --true-z-values-mm 90,90,90 \
  --truth-radius-mm 6.0 \
  --initial-x-values-mm 150,250,350 \
  --initial-z-values-mm 90,90,90 \
  --initial-radius-values-mm 6,6,6 \
  --target-indices 0 \
  --passes 1 \
  --x-offsets-mm 0 \
  --z-offsets-mm 0 \
  --radius-offsets-mm 0 \
  --replication-cases exact:1.0,0.0,1.0,0.0,0 \
  --source-frequency-scales 1.0 \
  --source-time-shift-ps-values=0 \
  --progress-every 1 \
  --run-name coordinate_optimizer_cpu_smoke
```

Result:

- Final state stayed at the exact truth:
  `x=[150,250,350] mm`, `z=[90,90,90] mm`, `r=[6,6,6] mm`.
- The single-candidate smoke correctly reports `confidence_label=missing`
  because no competing radius exists.
- Artifacts written: summary JSON, coordinate confidence CSV, state-history CSV,
  and confidence-margin PNG.
- Plot validation: size `1549x903`, dynamic range `255`, standard deviation
  `26.35`; this is nonblank and usable for a one-bar smoke plot.

Interpretation:

The smoke only validates CLI wiring and output contracts. It deliberately does
not validate inversion quality. The next decision is to run the same optimizer
on GPU CPML with all three targets, compact windows, and a perturbed seed that
contains the truth inside each target window.

## 082: GPU Compact Perturbed-Seed Coordinate Gate

Output:

```text
outputs/experiments/082_coordinate_optimizer_gpu_compact_perturbed_seed
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 150,250,350 \
  --true-z-values-mm 90,90,90 \
  --truth-radius-mm 6.0 \
  --initial-x-values-mm 149,251,349 \
  --initial-z-values-mm 91,89,91 \
  --initial-radius-values-mm 6.2,5.8,6.2 \
  --target-indices 0,1,2 \
  --passes 1 \
  --x-offsets-mm=-1:1:1 \
  --z-offsets-mm=-1:1:1 \
  --radius-offsets-mm=-0.2:0.2:0.2 \
  --replication-cases 'nominal:1.0,0.0,1.0,0.0,0|source_mismatch:1.1,-50.0,1.1,0.0,0' \
  --update-case-label nominal \
  --source-frequency-scales 0.9,1.0,1.1 \
  --source-time-shift-ps-values=-50,0,50 \
  --progress-every 9 \
  --run-name coordinate_optimizer_gpu_compact_perturbed_seed
```

GPU verification:

```text
nvidia-smi showed the FNO Python process active on NVIDIA GB10 at 87% GPU
utilization during the run.
```

Result:

| Target | Initial x/z/r [mm] | Final x/z/r [mm] | Nominal margin | Nominal label | Source-mismatch label |
| ---: | --- | --- | ---: | --- | --- |
| 0 | 149 / 91 / 6.2 | 150 / 90 / 6.0 | 4.773e-04 | weak | weak |
| 1 | 251 / 89 / 5.8 | 250 / 90 / 6.0 | 1.620e-03 | strong | strong |
| 2 | 349 / 91 / 6.2 | 350 / 90 / 6.0 | 3.658e-04 | weak | weak |

Summary:

- Final state recovered the exact truth:
  `x=[150,250,350] mm`, `z=[90,90,90] mm`, `r=[6,6,6] mm`.
- Runtime was `1294.5 s` for 3 coordinate steps, 27 candidates per target, 5
  scan positions, and two observed cases.
- Confidence rows: 6 total; 2 strong center-target rows and 4 weak edge-target
  rows with `radius_weak_confidence` fallback warnings.
- Ambiguity interval was narrow in this exact/source-mismatch gate:
  all rows reported one close candidate with `r=[6.0,6.0] mm` and
  `z=[90,90] mm`.
- The source profiler selected the true nuisance source in each case:
  nominal selected `fc=1.0`, `shift=0 ps`; source mismatch selected
  `fc=1.1`, `shift=-50 ps`.
- Plot validation: size `1549x903`, dynamic range `255`, standard deviation
  `77.18`.

Interpretation:

The first reporting-first coordinate optimizer gate passed for accuracy and
artifact quality. It is not yet a robustness result because this gate did not
include random noise. The weak absolute radius margins on targets 0 and 2 are
consistent with the Stage 6 confidence synthesis, so the optimizer should be
promoted only with confidence/fallback reporting attached.

Next decision:

Run the same coordinate optimizer under 10% noise/source mismatch seeds before
trying wider windows or more passes. This tests whether sequential coordinate
updates remain stable when the observed data are noisy, while keeping the
search window small enough that the truth is inside each target window.

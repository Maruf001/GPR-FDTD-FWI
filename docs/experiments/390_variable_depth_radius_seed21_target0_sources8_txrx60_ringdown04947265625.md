# Experiment 390: Seed21 Target-0 Sources=8 Tx/Rx=60 Ringdown04947265625

## Purpose

Run 856 tests the lower midpoint between accepted run 854 and rejected run
855. It is intended to close the seed21 target-0 threshold branch without
continuing into diminishing micro-brackets.

## 856: Coordinate Optimizer Variable-Depth/Radius Seed21 Target-0 Sources=8 Tx/Rx=60 Ringdown04947265625

Output:

```text
outputs/experiments/856_coordinate_optimizer_variable_depth_radius_seed21_target0_sources8_txrx60_ringdown04947265625_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 8 \
  --tx-rx-offset-mm 60 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 150,250,350 \
  --true-z-values-mm 80,100,120 \
  --truth-radius-values-mm 5,6,8 \
  --initial-x-values-mm 150,250,350 \
  --initial-z-values-mm 80,100,120 \
  --initial-radius-values-mm 5,6,8 \
  --target-indices 0 \
  --passes 1 \
  --x-offsets-mm=0 \
  --z-offsets-mm=0:1:1 \
  --radius-offsets-mm=0:1.25:0.25 \
  --replication-cases source_mismatch_ringdown04947265625_noise10_seed21:1.1,-50.0,1.1,0.10,21,0.4947265625,180.0,0.8 \
  --update-case-label source_mismatch_ringdown04947265625_noise10_seed21 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed21_target0_sources8_txrx60_ringdown04947265625_objectives
```

## Results

The final recovered coordinate state is exact:

```text
x = [150, 250, 350] mm
z = [80, 100, 120] mm
r = [5, 6, 8] mm
```

Base confidence row:

```text
case: source_mismatch_ringdown04947265625_noise10_seed21
target: 0
sources: 8
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 4.999420e-04
relative radius margin: 3.169587e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 0.015771510582150282
next radius misfit: 0.016271452535257584
elapsed: 600.9 s
```

Diagnostic objective rows all preserved the true target-0 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 4.999420e-04 | below cutoff, weak |
| highband | 6.454412e-04 | above cutoff |
| late | 3.290097e-04 | below cutoff, truth-preserving |
| late_high | 4.123367e-04 | below cutoff, truth-preserving |
| veryhigh | 6.086112e-04 | above cutoff |
| early_high | 5.505480e-04 | above cutoff |

## Interpretation

Run 856 is another exact but weak near-miss, missing cutoff by only
`5.805e-08`. It rejects the lower midpoint above run 854, leaving the
accepted/failed seed21 target-0 interval at `[0.49453125, 0.4947265625)`.

This is tight enough to summarize rather than continuing midpoint runs. The
highest accepted target-0 point is run 854, but it should be presented as a
razor-edge threshold, not a robust stress reserve.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.230143 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one weak row
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_mm is target-specific at 5.0 mm
resources: GPU utilization held around 91%; RAM stayed about 97-98 GiB available
elapsed: 600.9 s
```

## Next Decision

Create the seed21 target-0 threshold summary from runs 849, 852, 853, 854,
855, and 856. Do not continue midpoint bracketing unless a later analysis
needs a stricter numerical threshold.

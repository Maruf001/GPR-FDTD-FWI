# Experiment 425: Seed610 Target-2 Sources=9 Tx/Rx=60 Ringdown049453125

## Purpose

Run 891 tests whether seed610 target 2 becomes production-confident at the
existing practical threshold point `ringdown049453125` after 5-, 9-, and
11-source full-ringdown050 rows all remained exact but weak.

## 891: Coordinate Optimizer Variable-Depth/Radius Seed610 Target-2 Sources=9 Tx/Rx=60 Ringdown049453125

Output:

```text
outputs/experiments/891_coordinate_optimizer_variable_depth_radius_seed610_target2_sources9_txrx60_ringdown049453125_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 9 \
  --tx-rx-offset-mm 60 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 150,250,350 \
  --true-z-values-mm 80,100,120 \
  --truth-radius-values-mm 5,6,8 \
  --initial-x-values-mm 150,250,350 \
  --initial-z-values-mm 80,100,120 \
  --initial-radius-values-mm 5,6,8 \
  --target-indices 2 \
  --passes 1 \
  --x-offsets-mm=0 \
  --z-offsets-mm=0:1:1 \
  --radius-offsets-mm=0:1.25:0.25 \
  --replication-cases source_mismatch_ringdown049453125_noise10_seed610:1.1,-50.0,1.1,0.10,610,0.49453125,180.0,0.8 \
  --update-case-label source_mismatch_ringdown049453125_noise10_seed610 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed610_target2_sources9_txrx60_ringdown049453125_objectives
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
case: source_mismatch_ringdown049453125_noise10_seed610
target: 2
sources: 9
ringdown coefficient: 0.49453125
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 4.818309e-04
offset from cutoff: -1.816907e-05
relative radius margin: 3.061405e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 0.01574460722134132
next radius misfit: 0.016226438150403213
listed competing geometry: x=350 mm, z=121 mm, r=8.75 mm
elapsed: 732.16 s
```

Diagnostic objective rows all preserve the true target-2 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 4.818309e-04 | below cutoff |
| highband | 6.149381e-04 | above cutoff |
| late | 6.841174e-04 | above cutoff |
| late_high | 7.800690e-04 | above cutoff |
| veryhigh | 6.576093e-04 | above cutoff |
| early_high | 4.561506e-04 | below cutoff |

## Interpretation

Run 891 is exact but still weak. Compared with full-ringdown050 run 889, the
base margin improves by only `1.587e-06`:

| Run | Sources | Ringdown | Margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | ---: | --- |
| 889 | 9 | 0.50000000 | 4.802438e-04 | -1.976e-05 | rejected |
| 891 | 9 | 0.49453125 | 4.818309e-04 | -1.817e-05 | rejected |

This is not enough movement to justify fine bisection near `0.49453125`.
Seed610 target 2 needs a coarser stress bracket. The next run should keep the
best source count at 9 and test `ringdown0475`.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target-2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.224643 and full dynamic range
visual inspection: confidence figure is readable and correctly shows one weak row below the 0.0005 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target2 truth_radius_mm is 8.0 mm
resources: GPU utilization held around 91%; RAM stayed about 97 GiB available
elapsed: 732.16 s
```

## Next Decision

Run seed610 target 2 with 9 sources at `ringdown0475`. If that passes, bracket
the practical threshold between 0.475 and 0.49453125; if it fails, the seed610
target-2 stress threshold is materially lower than the seed21 practical point.

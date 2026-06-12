# Experiment 384: Seed21 Target-2 Sources=9 Tx/Rx=60 Ringdown049375

## Purpose

Run 850 tests seed21 target 2 at the seed21 target-0 practical stress boundary
from run 849. The acquisition uses 9 sources because seed89 target 2 required
the 9-source rescue at ringdown050 in run 844.

## 850: Coordinate Optimizer Variable-Depth/Radius Seed21 Target-2 Sources=9 Tx/Rx=60 Ringdown049375

Output:

```text
outputs/experiments/850_coordinate_optimizer_variable_depth_radius_seed21_target2_sources9_txrx60_ringdown049375_objectives
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
  --replication-cases source_mismatch_ringdown049375_noise10_seed21:1.1,-50.0,1.1,0.10,21,0.49375,180.0,0.8 \
  --update-case-label source_mismatch_ringdown049375_noise10_seed21 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed21_target2_sources9_txrx60_ringdown049375_objectives
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
case: source_mismatch_ringdown049375_noise10_seed21
target: 2
sources: 9
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 5.151258e-04
relative radius margin: 3.286832e-02
confidence label: moderate
fallback warning: none
best misfit: 0.015672412336457612
next radius misfit: 0.016187538152775877
listed competing geometry: x=350 mm, z=121 mm, r=8.75 mm
elapsed: 698.75 s
```

Diagnostic objective rows all preserved the true target-2 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 5.151258e-04 | above cutoff |
| highband | 6.858613e-04 | above cutoff |
| late | 7.528084e-04 | above cutoff |
| late_high | 9.028151e-04 | above cutoff |
| veryhigh | 7.092312e-04 | above cutoff |
| early_high | 5.080143e-04 | above cutoff |

## Interpretation

Run 850 passes. Seed21 target 2 remains exact/moderate at ringdown049375 with
the 9-source Tx/Rx=60 acquisition. The base margin is `1.5126e-05` above the
production cutoff, so the row is accepted but close.

This is stronger than target 0 at the same stress: run 849 cleared cutoff by
only `3.891e-07`. Seed21 target 0 remains the limiting seed21 row, and
ringdown050 remains rejected for target 0 under the current source/objective
policy.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.253242 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_mm is target-specific at 8.0 mm
resources: GPU utilization held around 91-92%; RAM stayed about 98 GiB available
elapsed: 698.75 s
```

## Next Decision

Create the seed21 ringdown049375 target-specific policy summary. Use run 849
for target 0, run 836 for target 1 as a higher-stress ringdown050 pass, and
run 850 for target 2. The summary should make clear that target 0 sets the
seed21 limit while target 1 has already survived the stronger ringdown050
condition.

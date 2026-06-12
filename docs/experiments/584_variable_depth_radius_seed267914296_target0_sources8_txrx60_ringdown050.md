# Experiment 584: Seed267914296 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Begin the seed267914296 branch with the established target0 standard control:
8 sources, Tx/Rx=60, ringdown050 source mismatch, and the six-objective
diagnostic bracket.

## 1050: Coordinate Optimizer Variable-Depth/Radius Seed267914296 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1050_coordinate_optimizer_variable_depth_radius_seed267914296_target0_sources8_txrx60_ringdown050_objectives
```

Command:

```bash
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
  --replication-cases source_mismatch_ringdown050_noise10_seed267914296:1.1,-50.0,1.1,0.10,267914296,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed267914296 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed267914296_target0_sources8_txrx60_ringdown050_objectives
```

## Results

Run 1050 is exact but weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 60.0
absolute radius margin: 4.963954e-04
offset from cutoff: -3.604568e-06
relative margin: 3.161948e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.569904e-02
next radius misfit: 1.619543e-02
elapsed: 571.3 s
```

Diagnostic objective margins:

```text
base       4.963954e-04  below cutoff
highband   6.514595e-04  above cutoff
late       3.462022e-04  below cutoff
late_high  4.175809e-04  below cutoff
veryhigh   6.306942e-04  above cutoff
early_high 5.513296e-04  above cutoff
```

All six objective variants rank the true target0 geometry first.

## Interpretation

The target0 geometry is correct, but the standard 8-source Tx/Rx=60 control is
not formally accepted because the base margin is 3.605e-06 below cutoff.
Highband, veryhigh, and early_high are healthy; late and late_high show the
recurring target0 late-window weakness. Because the result is exact but weak,
use the established target0 acquisition rescue before changing source
density or advancing the branch.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.231015 and unique_colors=264
visual inspection: confidence figure is readable and shows one weak target0 row just below the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 91%; peak observed temperature was about 74C
```

## Next Decision

Run seed267914296 target0 with 8 sources and Tx/Rx=52.5. If that acquisition
rescue worsens the base margin, switch to the source-density bracket at
Tx/Rx=60 rather than sweeping lower offsets blindly.

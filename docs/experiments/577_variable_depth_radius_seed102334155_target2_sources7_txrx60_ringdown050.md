# Experiment 577: Seed102334155 Target2 Sources=7 Tx/Rx=60 Ringdown050

## Purpose

Run the seed102334155 target2 7-source Tx/Rx=60 source-density rescue after
the standard 5-source control was exact but weak.

## 1043: Coordinate Optimizer Variable-Depth/Radius Seed102334155 Target2 Sources=7 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1043_coordinate_optimizer_variable_depth_radius_seed102334155_target2_sources7_txrx60_ringdown050_objectives
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 7 \
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
  --replication-cases source_mismatch_ringdown050_noise10_seed102334155:1.1,-50.0,1.1,0.10,102334155,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed102334155 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed102334155_target2_sources7_txrx60_ringdown050_objectives
```

## Results

Run 1043 is exact but still weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 7
tx_rx_offset_mm: 60.0
absolute radius margin: 4.777000e-04
offset from cutoff: -2.222997e-05
relative margin: 3.259031e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.465773e-02
next radius misfit: 1.513543e-02
elapsed: 490.0 s
```

Diagnostic objective margins:

```text
base       4.777000e-04  below cutoff
highband   6.312724e-04  above cutoff
late       6.894547e-04  above cutoff
late_high  7.982333e-04  above cutoff
veryhigh   6.672632e-04  above cutoff
early_high 4.102570e-04  below cutoff
```

All six objective variants rank the true target2 geometry first.

## Interpretation

The 7-source rescue is partial. Base improves from 4.590702e-04 in experiment
1042 to 4.777000e-04 here, a gain of about 1.86e-05, but it remains
2.223e-05 below cutoff. Early_high remains weak and is slightly worse than the
5-source control.

Since the true geometry remains rank 1 across all objective variants and
source density moved base in the right direction, continue one more
source-density escalation to 9 sources at Tx/Rx=60 before trying acquisition
offsets.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.222869 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one weak target2 row below the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=7; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 90%; system memory remained near 95 GiB available
```

## Next Decision

Run seed102334155 target2 with 9 sources and Tx/Rx=60. That escalation is
experiment 1044.

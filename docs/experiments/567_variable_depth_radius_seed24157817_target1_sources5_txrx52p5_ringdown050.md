# Experiment 567: Seed24157817 Target1 Sources=5 Tx/Rx=52.5 Ringdown050

## Purpose

Run the seed24157817 target1 Tx/Rx=52.5 acquisition rescue after the standard
5-source Tx/Rx=60 control selected the exact geometry but stayed weak on base
and early_high margins.

## 1033: Coordinate Optimizer Variable-Depth/Radius Seed24157817 Target1 Sources=5 Tx/Rx=52.5 Ringdown050

Output:

```text
outputs/experiments/1033_coordinate_optimizer_variable_depth_radius_seed24157817_target1_sources5_txrx52p5_ringdown050_objectives
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --tx-rx-offset-mm 52.5 \
  --frequency-ghz 1.5 \
  --true-x-values-mm 150,250,350 \
  --true-z-values-mm 80,100,120 \
  --truth-radius-values-mm 5,6,8 \
  --initial-x-values-mm 150,250,350 \
  --initial-z-values-mm 80,100,120 \
  --initial-radius-values-mm 5,6,8 \
  --target-indices 1 \
  --passes 1 \
  --x-offsets-mm=0 \
  --z-offsets-mm=0:1:1 \
  --radius-offsets-mm=0:1.25:0.25 \
  --replication-cases source_mismatch_ringdown050_noise10_seed24157817:1.1,-50.0,1.1,0.10,24157817,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed24157817 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed24157817_target1_sources5_txrx52p5_ringdown050_objectives
```

## Results

Run 1033 is exact and accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 5
tx_rx_offset_mm: 52.5
absolute radius margin: 5.591909e-04
offset from cutoff: +5.919087e-05
relative margin: 2.779846e-02
confidence label: moderate
fallback warning: none
best misfit: 2.011589e-02
next radius misfit: 2.067508e-02
elapsed: 363.7 s
```

Diagnostic objective margins:

```text
base       5.591909e-04  above cutoff
highband   7.313241e-04  above cutoff
late       9.117899e-04  above cutoff
late_high  9.785526e-04  above cutoff
veryhigh   6.700701e-04  above cutoff
early_high 5.026949e-04  above cutoff
```

All six objective variants rank the true target1 geometry first.

## Interpretation

The Tx/Rx=52.5 rescue succeeds. Relative to the weak Tx/Rx=60 control in
experiment 1032, base confidence improves from 4.794239e-04 to 5.591909e-04,
a gain of about 7.98e-05. Early_high also improves enough to clear the cutoff,
although its reserve is small at about 2.69e-06.

This closes the seed24157817 branch:

```text
target0: accepted at 8-source Tx/Rx=60 with late-window caveats.
target2: cleanly accepted at 5-source Tx/Rx=60.
target1: accepted at 5-source Tx/Rx=52.5, with a narrow early_high reserve.
```

Continue the Fibonacci replication chain with seed39088169 target0 at
8 sources and Tx/Rx=60.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.261547 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one moderate target1 row above the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 52.5; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 88%; system memory remained near 95 GiB available
```

## Next Decision

Run seed39088169 target0 with 8 sources and Tx/Rx=60. That control is
experiment 1034.

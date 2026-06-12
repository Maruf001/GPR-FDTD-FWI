# Experiment 573: Seed63245986 Target1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run the seed63245986 target1 standard control after target0 accepted with
caveats and target2 cleanly accepted.

## 1039: Coordinate Optimizer Variable-Depth/Radius Seed63245986 Target1 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1039_coordinate_optimizer_variable_depth_radius_seed63245986_target1_sources5_txrx60_ringdown050_objectives
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --tx-rx-offset-mm 60 \
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
  --replication-cases source_mismatch_ringdown050_noise10_seed63245986:1.1,-50.0,1.1,0.10,63245986,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed63245986 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed63245986_target1_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1039 is exact but weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 4.746005e-04
offset from cutoff: -2.539949e-05
relative margin: 2.815296e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.685793e-02
next radius misfit: 1.733253e-02
elapsed: 362.5 s
```

Diagnostic objective margins:

```text
base       4.746005e-04  below cutoff
highband   6.006095e-04  above cutoff
late       7.522790e-04  above cutoff
late_high  8.069520e-04  above cutoff
veryhigh   6.099324e-04  above cutoff
early_high 4.534072e-04  below cutoff
```

All six objective variants rank the true target1 geometry first.

## Interpretation

The standard target1 control selects the exact geometry but is not accepted:
base misses cutoff by 2.540e-05 and early_high is also weak. This repeats the
target1 pattern seen in seed9227465 and seed24157817, where the first rescue
to try is a 5-source Tx/Rx=52.5 acquisition probe.

Run Tx/Rx=52.5 before escalating source density. If that clears base
confidence, the seed63245986 branch can close with target0 accepted with
caveats, target2 clean, and target1 rescued.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.224683 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one weak target1 row below the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 88%; system memory remained near 95 GiB available
```

## Next Decision

Run seed63245986 target1 with 5 sources and Tx/Rx=52.5. That rescue is
experiment 1040.

# Experiment 558: Seed14930352 Target0 Sources=8 Tx/Rx=52.5 Ringdown050

## Purpose

Test the first acquisition-offset rescue for seed14930352 target0 after the
8-source Tx/Rx=60 control was exact but weak.

## 1024: Coordinate Optimizer Variable-Depth/Radius Seed14930352 Target0 Sources=8 Tx/Rx=52.5 Ringdown050

Output:

```text
outputs/experiments/1024_coordinate_optimizer_variable_depth_radius_seed14930352_target0_sources8_txrx52p5_ringdown050_objectives
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 8 \
  --tx-rx-offset-mm 52.5 \
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
  --replication-cases source_mismatch_ringdown050_noise10_seed14930352:1.1,-50.0,1.1,0.10,14930352,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed14930352 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed14930352_target0_sources8_txrx52p5_ringdown050_objectives
```

## Results

Run 1024 is exact but weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 52.5
absolute radius margin: 4.842836e-04
offset from cutoff: -1.571643e-05
confidence label: weak
fallback warning: radius_weak_confidence
elapsed: 561.5 s
```

Diagnostic objective margins:

```text
base       4.842836e-04  below cutoff by 1.571643e-05
highband   6.430479e-04  above cutoff
late       4.097333e-04  below cutoff by 9.026666e-05
late_high  4.364832e-04  below cutoff by 6.351683e-05
veryhigh   5.541121e-04  above cutoff
early_high 5.090140e-04  above cutoff
```

All six objective variants rank the true target0 geometry first.

## Interpretation

Tx/Rx=52.5 does not rescue seed14930352 target0. It worsens the base margin
relative to the Tx/Rx=60 control by about 8.94e-06, while late and late_high
remain below cutoff. Because the first acquisition-offset probe moved the
wrong direction on base confidence, continue by changing mechanism to source
density at Tx/Rx=60 instead of blindly bracketing lower Tx/Rx offsets.

The next run should be a 9-source Tx/Rx=60 bracket. If 9 sources remain weak,
the seed1346269 target0 precedent supports an 11-source escalation before
declaring this target unresolved.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.229170 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one weak target0 row below the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 52.5; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 91%; nvidia-smi process memory was about 294 MiB
```

## Next Decision

Run seed14930352 target0 with 9 sources and Tx/Rx=60. That source-density
bracket is experiment 1025.

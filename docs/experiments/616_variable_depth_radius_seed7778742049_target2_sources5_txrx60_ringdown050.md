# Experiment 616: Seed7778742049 Target2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Continue the seed7778742049 branch with the standard target2 control after
target0 was accepted through the 9-source source-density bracket.

## 1082: Coordinate Optimizer Variable-Depth/Radius Seed7778742049 Target2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1082_coordinate_optimizer_variable_depth_radius_seed7778742049_target2_sources5_txrx60_ringdown050_objectives
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
  --target-indices 2 \
  --passes 1 \
  --x-offsets-mm=0 \
  --z-offsets-mm=0:1:1 \
  --radius-offsets-mm=0:1.25:0.25 \
  --replication-cases source_mismatch_ringdown050_noise10_seed7778742049:1.1,-50.0,1.1,0.10,7778742049,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed7778742049 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed7778742049_target2_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1082 is exact but weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 4.903626e-04
offset from cutoff: -9.637360e-06
relative margin: 2.923442e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.677347e-02
next radius misfit: 1.726383e-02
elapsed: 397.8 s
```

Diagnostic objective margins:

```text
base       4.903626e-04  weak, below cutoff
highband   6.250434e-04  above cutoff
late       7.009049e-04  above cutoff
late_high  7.634205e-04  above cutoff
veryhigh   6.538180e-04  above cutoff
early_high 4.449874e-04  weak, below cutoff
```

All six objective variants rank the true target2 geometry first.

## Interpretation

Target2 selects the exact geometry, but the standard 5-source Tx/Rx=60 control
is not formally accepted because base and early_high are weak. This matches
the target2 weak-control pattern from seed267914296: highband, late,
late_high, and veryhigh clear cutoff while base and early_high remain below.
The next justified mechanism is a 7-source Tx/Rx=60 source-density bracket
before considering a 9-source escalation.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.225599 and unique_colors=264
visual inspection: confidence figure is readable and shows one weak target2 row below cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 87-88%; host RAM stayed about 94-95 GiB available
```

## Next Decision

Run seed7778742049 target2 with 7 sources and Tx/Rx=60.

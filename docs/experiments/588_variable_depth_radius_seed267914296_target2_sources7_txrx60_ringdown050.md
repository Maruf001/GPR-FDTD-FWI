# Experiment 588: Seed267914296 Target2 Sources=7 Tx/Rx=60 Ringdown050

## Purpose

Run the first source-density bracket for seed267914296 target2 after the
standard 5-source Tx/Rx=60 control selected the exact geometry but remained
weak on base and early_high objectives.

## 1054: Coordinate Optimizer Variable-Depth/Radius Seed267914296 Target2 Sources=7 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1054_coordinate_optimizer_variable_depth_radius_seed267914296_target2_sources7_txrx60_ringdown050_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed267914296_target2_sources7_txrx60_ringdown050_objectives
```

## Results

Run 1054 is exact but weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 7
tx_rx_offset_mm: 60.0
absolute radius margin: 4.728239e-04
offset from cutoff: -2.717614e-05
relative margin: 3.233940e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.462068e-02
next radius misfit: 1.509350e-02
elapsed: 495.1 s
```

Diagnostic objective margins:

```text
base       4.728239e-04  below cutoff
highband   6.347555e-04  above cutoff
late       6.855467e-04  above cutoff
late_high  7.900926e-04  above cutoff
veryhigh   6.048640e-04  above cutoff
early_high 4.205028e-04  below cutoff
```

All six objective variants rank the true target2 geometry first.

## Interpretation

The 7-source bracket does not rescue seed267914296 target2. It worsens the
base margin relative to the 5-source control by about 1.95e-05, while
early_high remains weak. Because the geometry is still truth-ranked and the
highband/late/late_high/veryhigh objectives are accepted, continue to one
9-source Tx/Rx=60 escalation before changing acquisition policy.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.221087 and unique_colors=264
visual inspection: confidence figure is readable and shows one weak target2 row below the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=7; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 90%; peak observed temperature was about 74C
```

## Next Decision

Run seed267914296 target2 with 9 sources and Tx/Rx=60.

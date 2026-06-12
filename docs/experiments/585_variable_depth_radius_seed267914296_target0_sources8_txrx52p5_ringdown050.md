# Experiment 585: Seed267914296 Target0 Sources=8 Tx/Rx=52.5 Ringdown050

## Purpose

Test the target0 acquisition-offset rescue after seed267914296 target0 was
exact but weak at the standard 8-source Tx/Rx=60 control.

## 1051: Coordinate Optimizer Variable-Depth/Radius Seed267914296 Target0 Sources=8 Tx/Rx=52.5 Ringdown050

Output:

```text
outputs/experiments/1051_coordinate_optimizer_variable_depth_radius_seed267914296_target0_sources8_txrx52p5_ringdown050_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed267914296_target0_sources8_txrx52p5_ringdown050_objectives
```

## Results

Run 1051 is exact but weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 52.5
absolute radius margin: 4.933085e-04
offset from cutoff: -6.691528e-06
relative margin: 2.695027e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.830440e-02
next radius misfit: 1.879771e-02
elapsed: 563.9 s
```

Diagnostic objective margins:

```text
base       4.933085e-04  below cutoff
highband   6.295227e-04  above cutoff
late       3.191052e-04  below cutoff
late_high  3.434604e-04  below cutoff
veryhigh   6.250076e-04  above cutoff
early_high 5.196557e-04  above cutoff
```

All six objective variants rank the true target0 geometry first.

## Interpretation

Tx/Rx=52.5 does not rescue seed267914296 target0. It worsens the base margin
relative to the Tx/Rx=60 control by about 3.09e-06, and late_high also moves
further below cutoff. Because the first acquisition-offset probe moved in the
wrong direction on base confidence, change mechanism to a source-density
bracket at Tx/Rx=60 instead of sweeping lower offsets blindly.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.230113 and unique_colors=264
visual inspection: confidence figure is readable and shows one weak target0 row below the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 52.5; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 91%; peak observed temperature was about 75C
```

## Next Decision

Run seed267914296 target0 with 9 sources and Tx/Rx=60. If 9 sources remain
weak, the seed1346269 and seed14930352 target0 precedent supports an
11-source escalation before declaring this target unresolved.

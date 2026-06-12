# Experiment 598: Seed701408733 Target0 Sources=8 Tx/Rx=52.5 Ringdown050

## Purpose

Run the target0 acquisition probe after the seed701408733 8-source Tx/Rx=60
control selected the exact target0 geometry but missed the base radius-margin
cutoff.

## 1064: Coordinate Optimizer Variable-Depth/Radius Seed701408733 Target0 Sources=8 Tx/Rx=52.5 Ringdown050

Output:

```text
outputs/experiments/1064_coordinate_optimizer_variable_depth_radius_seed701408733_target0_sources8_txrx52p5_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed701408733:1.1,-50.0,1.1,0.10,701408733,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed701408733 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed701408733_target0_sources8_txrx52p5_ringdown050_objectives
```

## Results

Run 1064 is exact and accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 52.5
absolute radius margin: 5.137347e-04
offset from cutoff: +1.373468e-05
relative margin: 2.779932e-02
confidence label: moderate
fallback warning: none
best misfit: 1.848012e-02
next radius misfit: 1.899385e-02
elapsed: 618.8 s
```

Diagnostic objective margins:

```text
base       5.137347e-04  above cutoff
highband   6.985708e-04  above cutoff
late       3.603501e-04  below cutoff
late_high  4.364269e-04  below cutoff
veryhigh   6.614760e-04  above cutoff
early_high 5.570815e-04  above cutoff
```

All six objective variants rank the true target0 geometry first.

## Interpretation

The Tx/Rx=52.5 acquisition probe rescues seed701408733 target0 by the base
confidence rule. It improves the base margin by about 2.84e-05 relative to
the Tx/Rx=60 control. Late and late_high remain below cutoff, so target0
stays accepted with the recurring late-window caveat. No source-density
escalation is justified before checking target2 and target1.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.238203 and unique_colors=264
visual inspection: confidence figure is readable and shows one moderate target0 row above the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 52.5; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 90-91%; host RAM stayed about 94-95 GiB available
```

## Next Decision

Continue seed701408733 with target2 at the standard 5-source Tx/Rx=60
control.

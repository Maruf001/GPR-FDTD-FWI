# Experiment 586: Seed267914296 Target0 Sources=9 Tx/Rx=60 Ringdown050

## Purpose

Run the source-density rescue bracket for seed267914296 target0 after both the
8-source Tx/Rx=60 control and the 8-source Tx/Rx=52.5 acquisition probe were
exact but weak.

## 1052: Coordinate Optimizer Variable-Depth/Radius Seed267914296 Target0 Sources=9 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1052_coordinate_optimizer_variable_depth_radius_seed267914296_target0_sources9_txrx60_ringdown050_objectives
```

Command:

```bash
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
  --run-name coordinate_optimizer_variable_depth_radius_seed267914296_target0_sources9_txrx60_ringdown050_objectives
```

## Results

Run 1052 is exact and accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 9
tx_rx_offset_mm: 60.0
absolute radius margin: 5.319292e-04
offset from cutoff: +3.192924e-05
relative margin: 3.408434e-02
confidence label: moderate
fallback warning: none
best misfit: 1.560626e-02
next radius misfit: 1.613819e-02
elapsed: 661.9 s
```

Diagnostic objective margins:

```text
base       5.319292e-04  above cutoff
highband   7.260094e-04  above cutoff
late       3.990896e-04  below cutoff
late_high  4.740279e-04  below cutoff
veryhigh   7.732793e-04  above cutoff
early_high 6.238098e-04  above cutoff
```

All six objective variants rank the true target0 geometry first.

## Interpretation

The 9-source Tx/Rx=60 source-density bracket rescues seed267914296 target0.
It improves the base margin by about 3.56e-05 relative to the 8-source
Tx/Rx=60 control and by about 3.86e-05 relative to the Tx/Rx=52.5 acquisition
probe. Late and late_high remain below cutoff, so carry the target0
late-window caveat forward, but no 11-source escalation is justified because
base confidence is now accepted and all variants rank the truth first.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.246340 and unique_colors=264
visual inspection: confidence figure is readable and shows one moderate target0 row above the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=9; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 90-92%; peak observed temperature was about 75C
```

## Next Decision

Continue the seed267914296 branch with target2 at 5 sources and Tx/Rx=60.

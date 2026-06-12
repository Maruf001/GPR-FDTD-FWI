# Experiment 711: Seed117669030670994 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Start the seed117669030670994 Fibonacci replication branch with the standard
target0 8-source Tx/Rx=60 control.

## 1174: Coordinate Optimizer Variable-Depth/Radius Seed117669030670994 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1174_coordinate_optimizer_variable_depth_radius_seed117669030670994_target0_sources8_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed117669030670994:1.1,-50.0,1.1,0.10,117669030670994,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed117669030670994 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed117669030670994_target0_sources8_txrx60_ringdown050_objectives
```

## Results

Run 1174 selected the exact geometry and crossed the moderate cutoff:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 60.0
absolute radius margin: 5.365146e-04
offset from cutoff: 3.651464e-05
relative margin: 3.398942e-02
confidence label: moderate
fallback warning: none
best misfit: 1.578475e-02
next radius misfit: 1.632127e-02
elapsed: 588.4 s
```

Diagnostic objective margins:

```text
base       5.365146e-04  above cutoff
highband   7.044646e-04  above cutoff
late       4.048865e-04  below cutoff
late_high  4.638562e-04  below cutoff
veryhigh   6.441039e-04  above cutoff
early_high 5.739118e-04  above cutoff
```

All six objective variants rank the exact target0 geometry first. The closest
base objective distinct-radius competitor is `r=5.25 mm` at the same depth,
and the closest changed-geometry competitor is `r=6.0 mm` at `z=81 mm`.

## Interpretation

This is an accepted target0 control for seed117669030670994. Late and
late_high remain below cutoff, so keep the recurring target0 late-window
caveat. Because the base, highband, veryhigh, and early_high objectives clear
cutoff and all objective variants rank the true geometry first, no target0
rescue branch is justified.

Continue seed117669030670994 with target2 at the standard 5-source Tx/Rx=60
control. No separate numbered summary output folder was created for this
decision.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3395 and sampled_unique_colors=173
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1745 and sampled_unique_colors=209
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0679 and sampled_unique_colors=435
figure validation: system_scene_geometry.png is 1770x1065 RGB with nonwhite_fraction=0.6333 and sampled_unique_colors=392
figure notes: figures/FIGURE_NOTES.md present, reports one moderate row and lists late and late_high below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 588.4 s through the candidate sweep
```

## Next Decision

Run seed117669030670994 target2 with the standard 5-source Tx/Rx=60 control.

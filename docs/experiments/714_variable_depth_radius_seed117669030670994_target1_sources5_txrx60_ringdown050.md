# Experiment 714: Seed117669030670994 Target1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Close the seed117669030670994 Fibonacci replication branch with the standard
target1 5-source Tx/Rx=60 control after target0 accepted and target2 accepted
through a 7-source bracket.

## 1177: Coordinate Optimizer Variable-Depth/Radius Seed117669030670994 Target1 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1177_coordinate_optimizer_variable_depth_radius_seed117669030670994_target1_sources5_txrx60_ringdown050_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed117669030670994_target1_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1177 selected the exact geometry and cleared the moderate cutoff cleanly:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 5.747783e-04
offset from cutoff: 7.477828e-05
relative margin: 3.410898e-02
confidence label: moderate
fallback warning: none
best misfit: 1.685123e-02
next radius misfit: 1.742601e-02
elapsed: 376.9 s
```

Diagnostic objective margins:

```text
base       5.747783e-04  above cutoff
highband   7.686292e-04  above cutoff
late       9.007734e-04  above cutoff
late_high  1.012685e-03  above cutoff
veryhigh   7.220919e-04  above cutoff
early_high 5.708561e-04  above cutoff
```

All six objective variants rank the exact target1 geometry first. The closest
base objective distinct-radius competitor is `r=6.25 mm` at the same depth,
and the closest changed-geometry competitor is `r=6.75 mm` at `z=101 mm`.

## Interpretation

This is a clean target1 acceptance at the standard 5-source Tx/Rx=60 setting.
It closes seed117669030670994 without a separate numbered summary output
folder: target0 accepted at 8-source Tx/Rx=60 with the recurring late-window
caveat, target2 accepted after a near-threshold 7-source bracket with an
early_high caveat, and target1 accepted cleanly at 5-source Tx/Rx=60.

Seed validation confirmed that `np.random.default_rng(190392491049135)`
succeeds in the active FNO environment. Continue the Fibonacci replication
chain with seed190392491049135 target0.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3613 and sampled_unique_colors=173
figure validation: coordinate_radius_decision_panel.png is 2128x1583 RGB with nonwhite_fraction=0.1774 and sampled_unique_colors=219
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0680 and sampled_unique_colors=432
figure validation: system_scene_geometry.png is 1769x1065 RGB with nonwhite_fraction=0.6336 and sampled_unique_colors=366
figure notes: figures/FIGURE_NOTES.md present, reports one moderate row and lists no objective variants below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 376.9 s through the candidate sweep
```

## Next Decision

Run seed190392491049135 target0 with the standard 8-source Tx/Rx=60 control.

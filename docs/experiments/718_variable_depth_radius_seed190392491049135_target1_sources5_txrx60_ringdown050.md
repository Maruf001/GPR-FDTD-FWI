# Experiment 718: Seed190392491049135 Target1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Close the seed190392491049135 Fibonacci replication branch with the standard
target1 5-source Tx/Rx=60 control after target0 accepted through the Tx/Rx=52.5
probe and target2 accepted at 5 sources.

## 1181: Coordinate Optimizer Variable-Depth/Radius Seed190392491049135 Target1 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1181_coordinate_optimizer_variable_depth_radius_seed190392491049135_target1_sources5_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed190392491049135:1.1,-50.0,1.1,0.10,190392491049135,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed190392491049135 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed190392491049135_target1_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1181 selected the exact geometry and crossed the moderate cutoff:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 5.327854e-04
offset from cutoff: 3.278541e-05
relative margin: 3.103039e-02
confidence label: moderate
fallback warning: none
best misfit: 1.716980e-02
next radius misfit: 1.770258e-02
elapsed: 380.6 s
```

Diagnostic objective margins:

```text
base       5.327854e-04  above cutoff
highband   7.030121e-04  above cutoff
late       8.680260e-04  above cutoff
late_high  9.304217e-04  above cutoff
veryhigh   6.483739e-04  above cutoff
early_high 5.122604e-04  above cutoff
```

All six objective variants rank the exact target1 geometry first. The closest
base objective distinct-radius competitor is `r=6.25 mm` at the same depth,
and the closest changed-geometry competitor is `r=6.75 mm` at `z=101 mm`.

## Interpretation

This is an accepted target1 control at the standard 5-source Tx/Rx=60 setting.
It closes seed190392491049135 without a separate numbered summary output
folder: target0 accepted after a Tx/Rx=52.5 acquisition probe rescued the
near-zero Tx/Rx=60 miss, target2 accepted cleanly at 5-source Tx/Rx=60, and
target1 accepted at 5-source Tx/Rx=60.

Seed validation confirmed that `np.random.default_rng(308061521720129)`
succeeds in the active FNO environment. Continue the Fibonacci replication
chain with seed308061521720129 target0.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3371 and sampled_unique_colors=172
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1693 and sampled_unique_colors=219
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0680 and sampled_unique_colors=432
figure validation: system_scene_geometry.png is 1769x1065 RGB with nonwhite_fraction=0.6335 and sampled_unique_colors=367
figure notes: figures/FIGURE_NOTES.md present, reports one moderate row and lists no objective variants below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 380.6 s through the candidate sweep
```

## Next Decision

Run seed308061521720129 target0 with the standard 8-source Tx/Rx=60 control.

# Experiment 710: Seed72723460378141 Target1 Sources=9 Tx/Rx=60 Ringdown050

## Purpose

Rescue-check the weak seed72723460378141 target1 5-source Tx/Rx=60 control with
a 9-source Tx/Rx=60 source-density escalation.

## 1173: Coordinate Optimizer Variable-Depth/Radius Seed72723460378141 Target1 Sources=9 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1173_coordinate_optimizer_variable_depth_radius_seed72723460378141_target1_sources9_txrx60_ringdown050_objectives
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
  --target-indices 1 \
  --passes 1 \
  --x-offsets-mm=0 \
  --z-offsets-mm=0:1:1 \
  --radius-offsets-mm=0:1.25:0.25 \
  --replication-cases source_mismatch_ringdown050_noise10_seed72723460378141:1.1,-50.0,1.1,0.10,72723460378141,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed72723460378141 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed72723460378141_target1_sources9_txrx60_ringdown050_objectives
```

## Results

Run 1173 selected the exact geometry and rescued the weak 5-source target1
control:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 9
tx_rx_offset_mm: 60.0
absolute radius margin: 5.446072e-04
offset from cutoff: 4.460715e-05
relative margin: 3.435035e-02
confidence label: moderate
fallback warning: none
best misfit: 1.585449e-02
next radius misfit: 1.639909e-02
elapsed: 677.9 s
```

Diagnostic objective margins:

```text
base       5.446072e-04  above cutoff
highband   7.614329e-04  above cutoff
late       8.530456e-04  above cutoff
late_high  1.030315e-03  above cutoff
veryhigh   6.652166e-04  above cutoff
early_high 5.495607e-04  above cutoff
```

All six objective variants rank the exact target1 geometry first. The closest
base objective distinct-radius competitor is `r=6.25 mm` at the same depth,
and the closest changed-geometry competitor is `r=6.75 mm` at `z=101 mm`.

## Interpretation

The 9-source Tx/Rx=60 rescue converts the weak target1 5-source control into a
clean acceptance. This closes seed72723460378141 without a separate numbered
summary output folder: target0 accepted at 8-source Tx/Rx=60 with the recurring
late-window caveat, target2 accepted at 5-source Tx/Rx=60 by a thin margin with
an early_high caveat, and target1 accepted cleanly after the 9-source rescue.

Seed validation confirmed that `np.random.default_rng(117669030670994)`
succeeds in the active FNO environment. Continue the Fibonacci replication
chain with seed117669030670994 target0.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3463 and sampled_unique_colors=165
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1715 and sampled_unique_colors=222
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0680 and sampled_unique_colors=432
figure validation: system_scene_geometry.png is 1769x1065 RGB with nonwhite_fraction=0.6334 and sampled_unique_colors=379
figure notes: figures/FIGURE_NOTES.md present, reports one moderate row and lists no objective variants below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=9; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 677.9 s through the candidate sweep
```

## Next Decision

Run seed117669030670994 target0 with the standard 8-source Tx/Rx=60 control.

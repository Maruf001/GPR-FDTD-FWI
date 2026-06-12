# Experiment 719: Seed308061521720129 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Start the seed308061521720129 Fibonacci replication branch with the standard
target0 8-source Tx/Rx=60 control.

## 1182: Coordinate Optimizer Variable-Depth/Radius Seed308061521720129 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1182_coordinate_optimizer_variable_depth_radius_seed308061521720129_target0_sources8_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed308061521720129:1.1,-50.0,1.1,0.10,308061521720129,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed308061521720129 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed308061521720129_target0_sources8_txrx60_ringdown050_objectives
```

## Results

Run 1182 selected the exact geometry but remains below the moderate cutoff:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 60.0
absolute radius margin: 4.679208e-04
offset from cutoff: -3.207919e-05
relative margin: 2.970926e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.575000e-02
next radius misfit: 1.621792e-02
elapsed: 573.3 s
```

Diagnostic objective margins:

```text
base       4.679208e-04  below cutoff
highband   5.891843e-04  above cutoff
late       3.780466e-04  below cutoff
late_high  3.976115e-04  below cutoff
veryhigh   5.633091e-04  above cutoff
early_high 5.116336e-04  above cutoff
```

All six objective variants rank the exact target0 geometry first. The closest
base objective distinct-radius competitor is `r=5.25 mm` at the same depth,
and the closest changed-geometry competitor is `r=6.0 mm` at `z=81 mm`.

## Interpretation

This is a target0 radius-confidence weakness rather than a geometry failure:
base, late, and late_high are below cutoff, while highband, veryhigh, and
early_high clear cutoff, and every objective ranks the exact geometry first.
Follow the target0 weak-control policy with an 8-source Tx/Rx=52.5 mm
acquisition probe.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3008 and sampled_unique_colors=171
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1708 and sampled_unique_colors=216
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0679 and sampled_unique_colors=435
figure validation: system_scene_geometry.png is 1769x1065 RGB with nonwhite_fraction=0.6338 and sampled_unique_colors=391
figure notes: figures/FIGURE_NOTES.md present, reports one weak row and lists base, late, and late_high below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 573.3 s through the candidate sweep
```

## Next Decision

Run seed308061521720129 target0 with the same 8-source aperture at Tx/Rx=52.5
mm.

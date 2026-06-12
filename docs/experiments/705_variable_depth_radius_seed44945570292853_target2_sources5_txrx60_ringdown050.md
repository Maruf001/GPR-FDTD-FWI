# Experiment 705: Seed44945570292853 Target2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Continue the seed44945570292853 Fibonacci replication branch with the standard
target2 5-source Tx/Rx=60 control after the target0 Tx/Rx=52.5 rescue.

## 1168: Coordinate Optimizer Variable-Depth/Radius Seed44945570292853 Target2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1168_coordinate_optimizer_variable_depth_radius_seed44945570292853_target2_sources5_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed44945570292853:1.1,-50.0,1.1,0.10,44945570292853,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed44945570292853 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed44945570292853_target2_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1168 selected the exact geometry and crossed the moderate cutoff:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 5.391246e-04
offset from cutoff: 3.912463e-05
relative margin: 3.159421e-02
confidence label: moderate
fallback warning: none
best misfit: 1.706390e-02
next radius misfit: 1.760302e-02
elapsed: 377.7 s
```

Diagnostic objective margins:

```text
base       5.391246e-04  above cutoff
highband   6.320254e-04  above cutoff
late       8.659964e-04  above cutoff
late_high  8.904429e-04  above cutoff
veryhigh   6.979896e-04  above cutoff
early_high 4.422807e-04  below cutoff
```

All six objective variants rank the exact target2 geometry first. The closest
base objective distinct-radius and changed-geometry competitor is `r=8.75 mm`
at `z=121 mm`.

## Interpretation

This is an accepted target2 control at the standard 5-source Tx/Rx=60 setting.
The early_high diagnostic remains weak, but the base objective is above cutoff
and five of six diagnostic objective margins support the exact geometry. This
is consistent with prior target2 cases where an isolated early_high weakness
did not justify an escalation after the base objective accepted.

Continue seed44945570292853 with target1 at the standard 5-source Tx/Rx=60
control. No separate numbered summary output folder was created for this
decision.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3436 and sampled_unique_colors=167
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1727 and sampled_unique_colors=211
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0681 and sampled_unique_colors=427
figure validation: system_scene_geometry.png is 1769x1065 RGB with nonwhite_fraction=0.6336 and sampled_unique_colors=373
figure notes: figures/FIGURE_NOTES.md present, reports one moderate row and lists early_high below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 377.7 s through the candidate sweep
```

## Next Decision

Run seed44945570292853 target1 with the standard 5-source Tx/Rx=60 control.

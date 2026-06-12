# Experiment 721: Seed308061521720129 Target2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Continue seed308061521720129 after the accepted target0 Tx/Rx=52.5 rescue
with the standard target2 5-source Tx/Rx=60 control.

## 1184: Coordinate Optimizer Variable-Depth/Radius Seed308061521720129 Target2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1184_coordinate_optimizer_variable_depth_radius_seed308061521720129_target2_sources5_txrx60_ringdown050_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed308061521720129_target2_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1184 selected the exact geometry but missed the moderate cutoff:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 4.908834e-04
offset from cutoff: -9.116617e-06
relative margin: 2.911469e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.686033e-02
next radius misfit: 1.735122e-02
elapsed: 379.6 s
```

Diagnostic objective margins:

```text
base       4.908834e-04  below cutoff
highband   5.945703e-04  above cutoff
late       7.300008e-04  above cutoff
late_high  7.452294e-04  above cutoff
veryhigh   6.064892e-04  above cutoff
early_high 4.250145e-04  below cutoff
```

All six objective variants rank the exact target2 geometry first. The closest
base objective distinct-radius competitor is `r=8.75 mm` at `z=121 mm`, which
is also the closest changed-geometry competitor.

## Interpretation

This is a near-miss target2 radius-confidence weakness rather than a geometry
failure. The exact target2 candidate wins every diagnostic objective, but the
base margin is `9.12e-06` below cutoff and early_high is weak. Follow the
standard target2 weak-control policy with a 7-source Tx/Rx=60 source-density
bracket before accepting or escalating further.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3067 and sampled_unique_colors=78
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1524 and sampled_unique_colors=76
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0618 and sampled_unique_colors=157
figure validation: system_scene_geometry.png is 1769x1065 RGB with nonwhite_fraction=0.6260 and sampled_unique_colors=103
figure notes: figures/FIGURE_NOTES.md present, reports one weak row and lists base and early_high below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 379.6 s through the candidate sweep
```

## Next Decision

Run seed308061521720129 target2 with 7 sources at Tx/Rx=60 mm.

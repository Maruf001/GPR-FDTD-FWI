# Experiment 728: Seed498454012769264 Target2 Sources=7 Tx/Rx=60 Ringdown050

## Purpose

Follow up the practical near-zero seed498454012769264 target2 5-source control
with a 7-source Tx/Rx=60 source-density bracket.

## 1191: Coordinate Optimizer Variable-Depth/Radius Seed498454012769264 Target2 Sources=7 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1191_coordinate_optimizer_variable_depth_radius_seed498454012769264_target2_sources7_txrx60_ringdown050_objectives
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 7 \
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
  --replication-cases source_mismatch_ringdown050_noise10_seed498454012769264:1.1,-50.0,1.1,0.10,498454012769264,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed498454012769264 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed498454012769264_target2_sources7_txrx60_ringdown050_objectives
```

## Results

Run 1191 selected the exact geometry but remained weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 7
tx_rx_offset_mm: 60.0
absolute radius margin: 4.324615e-04
offset from cutoff: -6.753846e-05
relative margin: 2.914069e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.484047e-02
next radius misfit: 1.527293e-02
elapsed: 506.7 s
```

Diagnostic objective margins:

```text
base       4.324615e-04  below cutoff
highband   5.410031e-04  above cutoff
late       6.413696e-04  above cutoff
late_high  6.500376e-04  above cutoff
veryhigh   5.703270e-04  above cutoff
early_high 3.753206e-04  below cutoff
```

All six objective variants rank the exact target2 geometry first. The closest
base objective distinct-radius competitor is `r=8.75 mm` at `z=121 mm`, which
is also the closest changed-geometry competitor.

## Interpretation

The 7-source bracket did not stabilize the target2 point-radius confidence.
It moves the base margin from a practical near-zero `5.000581e-04` at
5 sources to a weak `4.324615e-04` at 7 sources, while preserving exact rank-1
geometry across all objectives. Escalate once to the 9-source Tx/Rx=60 bracket
before deciding whether this seed's target2 should be carried as an exact
geometry with weak point-radius confidence.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.2732 and sampled_unique_colors=71
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1918 and sampled_unique_colors=85
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0618 and sampled_unique_colors=157
figure validation: system_scene_geometry.png is 1769x1065 RGB with nonwhite_fraction=0.6260 and sampled_unique_colors=112
figure notes: figures/FIGURE_NOTES.md present, reports one weak row and lists base and early_high below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=7; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 506.7 s through the candidate sweep
```

## Next Decision

Run seed498454012769264 target2 with 9 sources at Tx/Rx=60 mm.

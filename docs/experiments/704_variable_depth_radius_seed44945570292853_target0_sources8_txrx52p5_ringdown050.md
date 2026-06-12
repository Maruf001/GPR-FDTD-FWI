# Experiment 704: Seed44945570292853 Target0 Sources=8 Tx/Rx=52.5 Ringdown050

## Purpose

Rescue-check the seed44945570292853 target0 weak 8-source Tx/Rx=60 control by
holding source count fixed and reducing Tx/Rx offset to 52.5 mm.

## 1167: Coordinate Optimizer Variable-Depth/Radius Seed44945570292853 Target0 Sources=8 Tx/Rx=52.5 Ringdown050

Output:

```text
outputs/experiments/1167_coordinate_optimizer_variable_depth_radius_seed44945570292853_target0_sources8_txrx52p5_ringdown050_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed44945570292853_target0_sources8_txrx52p5_ringdown050_objectives
```

## Results

Run 1167 selected the exact geometry and crossed the moderate cutoff:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 52.5
absolute radius margin: 5.400010e-04
offset from cutoff: 4.000103e-05
relative margin: 2.945274e-02
confidence label: moderate
fallback warning: none
best misfit: 1.833449e-02
next radius misfit: 1.887449e-02
elapsed: 578.2 s
```

Diagnostic objective margins:

```text
base       5.400010e-04  above cutoff
highband   6.835313e-04  above cutoff
late       4.403326e-04  below cutoff
late_high  4.641480e-04  below cutoff
veryhigh   6.487844e-04  above cutoff
early_high 5.521463e-04  above cutoff
```

All six objective variants rank the exact target0 geometry first. The closest
base objective distinct-radius competitor is `r=5.25 mm` at the same depth,
and the closest changed-geometry competitor is `r=6.0 mm` at `z=81 mm`.

## Interpretation

The Tx/Rx=52.5 mm acquisition probe rescues the seed44945570292853 target0
near-miss seen at Tx/Rx=60. The late and late_high objective variants remain
below cutoff, so keep the recurring target0 late-window caveat, but the base,
highband, veryhigh, and early_high objectives all support the exact geometry.

No further target0 rescue is justified for this seed. Continue
seed44945570292853 with target2 at the standard 5-source Tx/Rx=60 control.
No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3440 and sampled_unique_colors=163
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1810 and sampled_unique_colors=215
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0679 and sampled_unique_colors=434
figure validation: system_scene_geometry.png is 1769x1065 RGB with nonwhite_fraction=0.6339 and sampled_unique_colors=396
figure notes: figures/FIGURE_NOTES.md present, reports one moderate row and lists late and late_high below cutoff
metadata validation: tx_rx_offset_mm is 52.5; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 578.2 s through the candidate sweep
```

## Next Decision

Run seed44945570292853 target2 with the standard 5-source Tx/Rx=60 control.

# Experiment 743: Seed3416454629006707 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Start the next Fibonacci seed replication chain after closing
seed2111485081748050. The first control is the standard target0 8-source
Tx/Rx=60 configuration.

Seed validation:

```text
np.random.default_rng(3416454629006707) pass in the active FNO environment
```

## 1206: Coordinate Optimizer Variable-Depth/Radius Seed3416454629006707 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1206_coordinate_optimizer_variable_depth_radius_seed3416454629006707_target0_sources8_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed3416454629006707:1.1,-50.0,1.1,0.10,3416454629006707,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed3416454629006707 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed3416454629006707_target0_sources8_txrx60_ringdown050_objectives
```

## Results

Run 1206 selected the exact target0 geometry and cleared the base moderate
confidence cutoff:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 60.0
absolute radius margin: 5.540487e-04
offset from cutoff: 5.404872e-05
relative margin: 3.538330e-02
confidence label: moderate
fallback warning: none
best misfit: 1.565848e-02
next radius misfit: 1.621253e-02
elapsed: 574.4 s
```

Diagnostic objective margins:

```text
base       5.540487e-04  above cutoff
highband   6.989266e-04  above cutoff
late       4.391125e-04  below cutoff
late_high  4.942303e-04  below cutoff
veryhigh   6.494273e-04  above cutoff
early_high 5.802490e-04  above cutoff
```

All six objective variants rank the exact target0 geometry first. The closest
base objective distinct-radius competitor is `r=5.25 mm`; the closest
changed-geometry competitor is `x=150 mm`, `z=81 mm`, `r=6.0 mm`.

## Interpretation

This is an accepted target0 control with the recurring target0 late-window
caveat. Base confidence is moderate, no fallback warning is emitted, and all
diagnostic objectives select the true target0 geometry. The late and late_high
windows remain below cutoff, but this matches the established accepted target0
pattern and does not justify a rescue branch by itself.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB and nonblank
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB and nonblank
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB and nonblank
figure validation: system_scene_geometry.png is 1769x1065 RGB and nonblank
figure notes: figures/FIGURE_NOTES.md present and reports objective variants below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 574.4 s through the candidate sweep
```

## Next Decision

Continue seed3416454629006707 with target2 at the standard 5-source Tx/Rx=60 mm
control.

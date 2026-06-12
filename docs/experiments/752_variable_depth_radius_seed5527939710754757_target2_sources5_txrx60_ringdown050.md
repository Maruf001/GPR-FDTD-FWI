# Experiment 752: Seed5527939710754757 Target2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Continue seed5527939710754757 after closing target0 at the Tx/Rx=45 lower-edge
acquisition point. This run uses the standard target2 5-source Tx/Rx=60
control.

## 1215: Coordinate Optimizer Variable-Depth/Radius Seed5527939710754757 Target2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1215_coordinate_optimizer_variable_depth_radius_seed5527939710754757_target2_sources5_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed5527939710754757:1.1,-50.0,1.1,0.10,5527939710754757,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed5527939710754757 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed5527939710754757_target2_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1215 selected the exact target2 geometry and cleared the base moderate
confidence cutoff:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 5.875412e-04
offset from cutoff: 8.754119e-05
relative margin: 3.526337e-02
confidence label: moderate
fallback warning: none
best misfit: 1.666152e-02
next radius misfit: 1.724906e-02
elapsed: 378.5 s
```

Diagnostic objective margins:

```text
base       5.875412e-04  above cutoff
highband   7.303431e-04  above cutoff
late       9.112414e-04  above cutoff
late_high  9.580795e-04  above cutoff
veryhigh   7.723078e-04  above cutoff
early_high 4.863737e-04  below cutoff
```

All six objective variants rank the exact target2 geometry first. The closest
base objective distinct-radius and changed-geometry competitor is `r=8.75 mm`
at `z=121 mm`.

## Interpretation

This is an accepted target2 control with the recurring early-window caveat.
Base confidence is moderate, no fallback warning is emitted, and every
diagnostic objective selects the true target2 geometry. Because only
early_high is below cutoff, no source-density escalation is justified.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB and nonblank
figure validation: coordinate_radius_decision_panel.png is 2128x1583 RGB and nonblank
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB and nonblank
figure validation: system_scene_geometry.png is 1768x1065 RGB and nonblank
figure notes: figures/FIGURE_NOTES.md present and reports moderate confidence plus below-cutoff variants
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 378.5 s through the candidate sweep
```

## Next Decision

Continue seed5527939710754757 with target1 at the standard 5-source Tx/Rx=60 mm
control.

# Experiment 754: Seed5527939710754757 Target1 Sources=9 Tx/Rx=60 Ringdown050

## Purpose

Run the established target1 9-source Tx/Rx=60 rescue after the standard
5-source target1 control for seed5527939710754757 remained exact but weak.

## 1217: Coordinate Optimizer Variable-Depth/Radius Seed5527939710754757 Target1 Sources=9 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1217_coordinate_optimizer_variable_depth_radius_seed5527939710754757_target1_sources9_txrx60_ringdown050_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed5527939710754757_target1_sources9_txrx60_ringdown050_objectives
```

## Results

Run 1217 selected the exact target1 geometry and improved over the 5-source
control, but it still did not clear the base moderate-confidence cutoff:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 9
tx_rx_offset_mm: 60.0
absolute radius margin: 4.874569e-04
offset from cutoff: -1.254312e-05
relative margin: 3.118314e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.563207e-02
next radius misfit: 1.611952e-02
elapsed: 687.4 s
```

Diagnostic objective margins:

```text
base       4.874569e-04  below cutoff
highband   6.847261e-04  above cutoff
late       7.245101e-04  above cutoff
late_high  9.346139e-04  above cutoff
veryhigh   6.523762e-04  above cutoff
early_high 5.020206e-04  above cutoff
```

All six objective variants rank the exact target1 geometry first. The closest
base objective distinct-radius competitor is `r=6.25 mm`; the closest
changed-geometry competitor is `x=250 mm`, `z=101 mm`, `r=6.75 mm`.

## Interpretation

The 9-source rescue improves target1 but remains a near-miss weak result.
Unlike the 5-source control, early_high now clears cutoff, and every diagnostic
objective preserves the true geometry. Because the base margin is still below
the strict cutoff, follow the established target1 unresolved-rescue policy and
run an 11-source Tx/Rx=60 escalation before evaluating the branch.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB and nonblank
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB and nonblank
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB and nonblank
figure validation: system_scene_geometry.png is 1769x1065 RGB and nonblank
figure notes: figures/FIGURE_NOTES.md present and reports weak confidence/below-cutoff variants
metadata validation: tx_rx_offset_mm is 60.0; sources=9; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU run completed in 687.4 s through the candidate sweep
```

## Next Decision

Run seed5527939710754757 target1 with 11 sources at Tx/Rx=60 mm, then stop for
a marathon-level evaluation before starting another seed or major goal.

# Experiment 636: Seed53316291173 Target2 Sources=7 Tx/Rx=60 Ringdown050

## Purpose

Test whether a 7-source Tx/Rx=60 source-density bracket strengthens the weak
but exact target2 recovery from run 1101.

## 1102: Coordinate Optimizer Variable-Depth/Radius Seed53316291173 Target2 Sources=7 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1102_coordinate_optimizer_variable_depth_radius_seed53316291173_target2_sources7_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed53316291173:1.1,-50.0,1.1,0.10,53316291173,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed53316291173 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed53316291173_target2_sources7_txrx60_ringdown050_objectives
```

## Results

Run 1102 is exact but still weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 7
tx_rx_offset_mm: 60.0
absolute radius margin: 4.206448e-04
offset from cutoff: -7.935520e-05
relative margin: 2.843163e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.479496e-02
next radius misfit: 1.521561e-02
elapsed: 537.7 s
```

Diagnostic objective margins:

```text
base       4.206448e-04  weak, below cutoff
highband   5.539282e-04  above cutoff
late       6.031470e-04  above cutoff
late_high  6.692926e-04  above cutoff
veryhigh   6.038365e-04  above cutoff
early_high 3.900229e-04  weak, below cutoff
```

All six objective variants rank the true target2 geometry first.

## Interpretation

The 7-source bracket improves the base margin relative to run 1101
(`4.001e-04` to `4.206e-04`) and rescues highband above cutoff, but it does
not rescue the base confidence row. Target2 is still truth-preserving but not
accepted by the current confidence rule. Follow the established target2 ladder
with one 9-source Tx/Rx=60 escalation.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.281952 and unique_colors=233
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.207825 and unique_colors=1067
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.068088 and unique_colors=2990
visual inspection: decision panel shows selected r=8.00 mm, next r=8.75 mm, and base/early_high as below-cutoff objectives
figure notes: figures/FIGURE_NOTES.md present, run-specific, and identifies the decision panel as the primary figure
metadata validation: tx_rx_offset_mm is 60.0; sources=7; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 89%; host RAM stayed about 95 GiB available
```

## Next Decision

Run seed53316291173 target2 with a 9-source Tx/Rx=60 source-density escalation.

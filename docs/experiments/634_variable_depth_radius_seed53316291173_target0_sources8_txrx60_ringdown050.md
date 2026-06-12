# Experiment 634: Seed53316291173 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Start the seed53316291173 Fibonacci-replication branch with the standard
target0 8-source Tx/Rx=60 control after seed32951280099 closed with accepted
target0, rescued target2, and accepted target1 results.

## 1100: Coordinate Optimizer Variable-Depth/Radius Seed53316291173 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1100_coordinate_optimizer_variable_depth_radius_seed53316291173_target0_sources8_txrx60_ringdown050_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed53316291173_target0_sources8_txrx60_ringdown050_objectives
```

## Results

Run 1100 is exact and accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 60.0
absolute radius margin: 5.464607e-04
offset from cutoff: +4.646071e-05
relative margin: 3.434444e-02
confidence label: moderate
fallback warning: none
best misfit: 1.591118e-02
next radius misfit: 1.645765e-02
elapsed: 627.7 s
```

Diagnostic objective margins:

```text
base       5.464607e-04  above cutoff
highband   6.775726e-04  above cutoff
late       4.870432e-04  below cutoff
late_high  4.980174e-04  below cutoff
veryhigh   6.393444e-04  above cutoff
early_high 5.926287e-04  above cutoff
```

All six objective variants rank the true target0 geometry first.

## Interpretation

Seed53316291173 target0 is accepted at the standard 8-source Tx/Rx=60 control.
The recurring target0 late-window caveat appears again because late and
late_high are just below the 5.0e-4 cutoff, but the base confidence row and
four of six diagnostic objectives clear cutoff while every objective ranks the
true geometry first. No target0 rescue run is justified before moving to
target2.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.355702 and unique_colors=338
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.192880 and unique_colors=822
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.067915 and unique_colors=3167
visual inspection: decision panel shows selected r=5.00 mm, next r=5.25 mm, first alternate geometry z=81 mm/r=6.00 mm, and late/late_high as below-cutoff objectives
figure notes: figures/FIGURE_NOTES.md present, run-specific, and identifies the decision panel as the primary figure
metadata validation: tx_rx_offset_mm is 60.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 83-91%; host RAM stayed about 95 GiB available
```

## Next Decision

Continue seed53316291173 with target2 at the standard 5-source Tx/Rx=60
control. This decision is recorded here and in the master plan only; no
separate numbered summary output folder was created.

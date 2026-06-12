# Experiment 641: Seed86267571272 Target2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Evaluate seed86267571272 target2 at the standard 5-source Tx/Rx=60 control
after target0 was accepted with the recurring late-window caveat.

## 1107: Coordinate Optimizer Variable-Depth/Radius Seed86267571272 Target2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1107_coordinate_optimizer_variable_depth_radius_seed86267571272_target2_sources5_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed86267571272:1.1,-50.0,1.1,0.10,86267571272,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed86267571272 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed86267571272_target2_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1107 is exact but weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 4.632626e-04
offset from cutoff: -3.673740e-05
relative margin: 2.758820e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.679206e-02
next radius misfit: 1.725532e-02
elapsed: 399.7 s
```

Diagnostic objective margins:

```text
base       4.632626e-04  weak, below cutoff
highband   5.187241e-04  above cutoff
late       7.022780e-04  above cutoff
late_high  6.697265e-04  above cutoff
veryhigh   5.552807e-04  above cutoff
early_high 3.764974e-04  weak, below cutoff
```

All six objective variants rank the true target2 geometry first. The closest
distinct-radius and changed-geometry competitor is `r=8.75 mm` at `z=121 mm`.

## Interpretation

The control run preserves the true geometry but does not meet the strict base
confidence cutoff. Since highband, late, late_high, and veryhigh already clear
cutoff while base and early_high do not, follow the target2 weak-control
policy with a 7-source Tx/Rx=60 bracket before considering a 9-source
escalation.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3073 and unique_colors=234
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1796 and unique_colors=852
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0681 and unique_colors=2990
visual inspection: decision panel shows selected r=8.00 mm, next r=8.75 mm, base below cutoff, and four objective variants above cutoff
figure notes: figures/FIGURE_NOTES.md present, run-specific, and lists base and early_high below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 87-88%; host RAM stayed about 96 GiB available
```

## Next Decision

Run seed86267571272 target2 at 7 sources and Tx/Rx=60 before considering a
9-source escalation.

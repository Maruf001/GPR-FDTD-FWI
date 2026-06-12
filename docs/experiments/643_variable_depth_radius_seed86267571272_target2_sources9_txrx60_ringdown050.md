# Experiment 643: Seed86267571272 Target2 Sources=9 Tx/Rx=60 Ringdown050

## Purpose

Escalate seed86267571272 target2 from the weak 5-source and 7-source rows to
the standard 9-source Tx/Rx=60 source-density test.

## 1109: Coordinate Optimizer Variable-Depth/Radius Seed86267571272 Target2 Sources=9 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1109_coordinate_optimizer_variable_depth_radius_seed86267571272_target2_sources9_txrx60_ringdown050_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed86267571272_target2_sources9_txrx60_ringdown050_objectives
```

## Results

Run 1109 is exact and a near miss:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 9
tx_rx_offset_mm: 60.0
absolute radius margin: 4.757869e-04
offset from cutoff: -2.421310e-05
relative margin: 3.032056e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.569189e-02
next radius misfit: 1.616768e-02
elapsed: 732.7 s
```

Diagnostic objective margins:

```text
base       4.757869e-04  weak, below cutoff
highband   6.023464e-04  above cutoff
late       7.063803e-04  above cutoff
late_high  7.814149e-04  above cutoff
veryhigh   6.325314e-04  above cutoff
early_high 4.322840e-04  weak, below cutoff
```

All six objective variants rank the true target2 geometry first. The closest
distinct-radius and changed-geometry competitor is `r=8.75 mm` at `z=121 mm`.

## Interpretation

The 9-source escalation improves the base margin relative to 7 sources, but it
remains below the `5.0e-4` cutoff. This is an exact near miss, not a
wrong-geometry failure. Follow the existing target2 near-miss precedent with
one 11-source Tx/Rx=60 closeout run. If that does not rescue the base row, stop
the simple source-density ladder for this target and move to target1.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3146 and unique_colors=235
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1717 and unique_colors=852
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0681 and unique_colors=2990
visual inspection: decision panel shows selected r=8.00 mm, next r=8.75 mm, base just below cutoff, and four objective variants above cutoff
figure notes: figures/FIGURE_NOTES.md present, run-specific, and lists base and early_high below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=9; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 90-91%; host RAM stayed about 96 GiB available
```

## Next Decision

Run one seed86267571272 target2 11-source Tx/Rx=60 closeout test before
moving to target1.

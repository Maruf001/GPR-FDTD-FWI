# Experiment 644: Seed86267571272 Target2 Sources=11 Tx/Rx=60 Ringdown050

## Purpose

Run the one allowed 11-source Tx/Rx=60 closeout for seed86267571272 target2
after the 9-source row was exact but just below the strict base
radius-confidence cutoff.

## 1110: Coordinate Optimizer Variable-Depth/Radius Seed86267571272 Target2 Sources=11 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1110_coordinate_optimizer_variable_depth_radius_seed86267571272_target2_sources11_txrx60_ringdown050_objectives
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 11 \
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
  --run-name coordinate_optimizer_variable_depth_radius_seed86267571272_target2_sources11_txrx60_ringdown050_objectives
```

## Results

Run 1110 is exact but weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 11
tx_rx_offset_mm: 60.0
absolute radius margin: 3.970768e-04
offset from cutoff: -1.029232e-04
relative margin: 2.705033e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.467918e-02
next radius misfit: 1.507626e-02
elapsed: 951.6 s
```

Diagnostic objective margins:

```text
base       3.970768e-04  weak, below cutoff
highband   4.994732e-04  just below cutoff
late       5.376423e-04  above cutoff
late_high  5.887100e-04  above cutoff
veryhigh   5.066393e-04  above cutoff
early_high 3.594493e-04  weak, below cutoff
```

All six objective variants rank the true target2 geometry first. The closest
distinct-radius and changed-geometry competitor is `r=8.75 mm` at `z=121 mm`.

## Interpretation

The 11-source closeout does not rescue target2. It weakens the base margin
relative to the 9-source near miss and pulls highband just below cutoff. This
closes the simple 5/7/9/11 source-density ladder for seed86267571272 target2
as truth-preserving but formally unresolved by the strict base confidence rule.

The best source-count row for this target remains run 1109, where the base
margin was `4.757869e-04`, only `2.421310e-05` below cutoff. No separate
numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.2691 and unique_colors=236
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.2032 and unique_colors=1060
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0681 and unique_colors=2990
visual inspection: decision panel shows selected r=8.00 mm, next r=8.75 mm, base below cutoff, and highband just below cutoff
figure notes: figures/FIGURE_NOTES.md present, run-specific, and lists base, highband, and early_high below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=11; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 90-92%; host RAM stayed about 96 GiB available
```

## Next Decision

Stop escalating target2 source count for this seed and continue seed86267571272
with target1 at the standard 5-source Tx/Rx=60 control.

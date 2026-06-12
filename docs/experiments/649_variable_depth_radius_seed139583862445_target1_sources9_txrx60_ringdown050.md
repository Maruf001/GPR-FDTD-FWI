# Experiment 649: Seed139583862445 Target1 Sources=9 Tx/Rx=60 Ringdown050

## Purpose

Resolve the weak seed139583862445 target1 5-source control by running the
established 9-source Tx/Rx=60 rescue. This is the seed-closing target1 check
after target0 and target2 were already accepted.

## 1115: Coordinate Optimizer Variable-Depth/Radius Seed139583862445 Target1 Sources=9 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1115_coordinate_optimizer_variable_depth_radius_seed139583862445_target1_sources9_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed139583862445:1.1,-50.0,1.1,0.10,139583862445,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed139583862445 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed139583862445_target1_sources9_txrx60_ringdown050_objectives
```

## Results

Run 1115 is exact and accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 9
tx_rx_offset_mm: 60.0
absolute radius margin: 5.083545e-04
offset from cutoff: +8.354504e-06
relative margin: 3.199767e-02
confidence label: moderate
fallback warning: none
best misfit: 1.588724e-02
next radius misfit: 1.639559e-02
elapsed: 722.4 s
```

Diagnostic objective margins:

```text
base       5.083545e-04  above cutoff
highband   6.990412e-04  above cutoff
late       7.569035e-04  above cutoff
late_high  9.232928e-04  above cutoff
veryhigh   6.698133e-04  above cutoff
early_high 5.152678e-04  above cutoff
```

All six objective variants rank the true target1 geometry first. The closest
distinct-radius competitor is `r=6.25 mm`; the closest changed-geometry
competitor is `r=6.75 mm` at `z=101 mm`.

## Interpretation

The 9-source rescue converts the weak 5-source target1 row into an accepted
row without moving the selected geometry. The margin is only slightly above
the strict cutoff, so this is an accepted rescue rather than a strong margin,
but all objective variants agree on the true target1 radius.

This closes seed139583862445 without a separate numbered summary output
folder: target0 accepted at 8-source Tx/Rx=60 with the recurring late-window
caveat, target2 accepted at 5-source Tx/Rx=60 with an early_high caveat, and
target1 accepted by the 9-source rescue.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3308 and unique_colors=338
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1555 and unique_colors=866
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0680 and unique_colors=3017
visual inspection: decision panel shows selected r=6.00 mm, next r=6.25 mm, competing geometry r=6.75 mm at z=101 mm, base above cutoff, and all objective variants above cutoff
figure notes: figures/FIGURE_NOTES.md present, run-specific, and lists no objective variants below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=9; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
```

## Next Decision

Continue the Fibonacci replication chain with seed225851433717 target0 after
confirming the seed is accepted by the active NumPy random generator.

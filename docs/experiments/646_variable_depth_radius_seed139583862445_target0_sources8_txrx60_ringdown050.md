# Experiment 646: Seed139583862445 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Continue the Fibonacci replication chain after closing seed86267571272. This
run validates seed139583862445 target0 at the standard 8-source Tx/Rx=60
control under the ringdown050 source-mismatch/noise condition.

Seed validation:

```text
np.random.default_rng(139583862445) succeeded in the active FNO environment.
```

## 1112: Coordinate Optimizer Variable-Depth/Radius Seed139583862445 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1112_coordinate_optimizer_variable_depth_radius_seed139583862445_target0_sources8_txrx60_ringdown050_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed139583862445_target0_sources8_txrx60_ringdown050_objectives
```

## Results

Run 1112 is exact and accepted with a late-window caveat:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 60.0
absolute radius margin: 6.294438e-04
offset from cutoff: +1.294438e-04
relative margin: 3.966382e-02
confidence label: moderate
fallback warning: none
best misfit: 1.586947e-02
next radius misfit: 1.649891e-02
elapsed: 623.0 s
```

Diagnostic objective margins:

```text
base       6.294438e-04  above cutoff
highband   8.142524e-04  above cutoff
late       4.750643e-04  weak, below cutoff
late_high  5.883205e-04  above cutoff
veryhigh   7.565966e-04  above cutoff
early_high 6.570514e-04  above cutoff
```

All six objective variants rank the true target0 geometry first. The closest
distinct-radius competitor is `r=5.25 mm`; the closest changed-geometry
competitor is `r=6.00 mm` at `z=81 mm`.

## Interpretation

The base confidence rule accepts target0. The recurring target0 late-window
caveat appears again, but only the late objective is below cutoff in this run;
late_high clears. No target0 rescue is justified because the base row is
comfortably above cutoff and the geometry is exact.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.4008 and unique_colors=338
figure validation: coordinate_radius_decision_panel.png is 2128x1583 RGB with nonwhite_fraction=0.1872 and unique_colors=841
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0679 and unique_colors=3171
visual inspection: decision panel shows selected r=5.00 mm, next r=5.25 mm, and only late below cutoff
figure notes: figures/FIGURE_NOTES.md present, run-specific, and lists late below cutoff
metadata validation: tx_rx_offset_mm is 60.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 90-91%; host RAM stayed about 96 GiB available
```

## Next Decision

Continue seed139583862445 with target2 at the standard 5-source Tx/Rx=60
control.

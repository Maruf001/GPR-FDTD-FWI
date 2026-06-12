# Experiment 645: Seed86267571272 Target1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Complete the seed86267571272 target-specific control sequence after target0
was accepted with the recurring late-window caveat and target2 was closed as
truth-preserving but formally unresolved by the strict base confidence rule.
This run checks target1 at the standard 5-source Tx/Rx=60 acquisition.

## 1111: Coordinate Optimizer Variable-Depth/Radius Seed86267571272 Target1 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1111_coordinate_optimizer_variable_depth_radius_seed86267571272_target1_sources5_txrx60_ringdown050_objectives
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
  --target-indices 1 \
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
  --run-name coordinate_optimizer_variable_depth_radius_seed86267571272_target1_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1111 is exact and accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 5.218757e-04
offset from cutoff: +2.187568e-05
relative margin: 3.107872e-02
confidence label: moderate
fallback warning: none
best misfit: 1.679206e-02
next radius misfit: 1.731393e-02
elapsed: 398.1 s
```

Diagnostic objective margins:

```text
base       5.218757e-04  above cutoff
highband   6.977894e-04  above cutoff
late       8.285574e-04  above cutoff
late_high  9.109682e-04  above cutoff
veryhigh   6.583741e-04  above cutoff
early_high 5.189042e-04  above cutoff
```

All six objective variants rank the true target1 geometry first. The closest
distinct-radius competitor is `r=6.25 mm`; the closest changed-geometry
competitor is `r=6.75 mm` at `z=101 mm`.

## Interpretation

Target1 is accepted at the standard 5-source Tx/Rx=60 control. This closes
seed86267571272:

```text
target0: accepted at 8-source Tx/Rx=60 with the recurring late-window caveat
target2: truth-preserving but unresolved; best source-count row is 1109
target1: accepted at 5-source Tx/Rx=60
```

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.3412 and unique_colors=338
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.1674 and unique_colors=867
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.0680 and unique_colors=3016
visual inspection: decision panel shows selected r=6.00 mm, next r=6.25 mm, and all objective-variant rows above cutoff
figure notes: figures/FIGURE_NOTES.md present, run-specific, and reports no below-cutoff objective variants
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 87%; host RAM stayed about 96 GiB available
```

## Next Decision

Continue the Fibonacci replication chain with seed139583862445 target0 after
confirming the seed is accepted by the active NumPy random generator.

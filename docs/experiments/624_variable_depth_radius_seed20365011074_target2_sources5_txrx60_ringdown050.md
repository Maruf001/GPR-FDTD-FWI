# Experiment 624: Seed20365011074 Target2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Continue the seed20365011074 branch after target0 passed the standard
8-source Tx/Rx=60 control with a tight base reserve and a late-window caveat.
This run checks target2 with the standard 5-source Tx/Rx=60
coordinate-objective sweep and the six-objective diagnostic bracket.

## 1090: Coordinate Optimizer Variable-Depth/Radius Seed20365011074 Target2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1090_coordinate_optimizer_variable_depth_radius_seed20365011074_target2_sources5_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed20365011074:1.1,-50.0,1.1,0.10,20365011074,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed20365011074 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed20365011074_target2_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1090 is exact but weak by the base confidence rule:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 2
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 4.964072e-04
offset from cutoff: -3.592760e-06
relative margin: 2.973838e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.669248e-02
next radius misfit: 1.718889e-02
elapsed: 396.5 s
```

Diagnostic objective margins:

```text
base       4.964072e-04  weak, below cutoff
highband   6.166574e-04  above cutoff
late       7.510895e-04  above cutoff
late_high  7.762375e-04  above cutoff
veryhigh   6.593249e-04  above cutoff
early_high 4.836145e-04  weak, below cutoff
```

All six objective variants rank the true target2 geometry first.

## Interpretation

The geometry recovery itself is correct, and the objective-top-candidate table
does not show an alternate geometry outranking the true target2 state. However,
the base margin is narrowly below the `5.0e-4` cutoff and the early_high
diagnostic is also weak. By the current target2 weak-control policy, this is
not an accepted stopping point. The next substantive run should test whether a
7-source Tx/Rx=60 source-density bracket strengthens the same exact target2
geometry before considering the 9-source escalation used in earlier weak
target2 branches.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1804x665 RGB with nonwhite_fraction=0.326682 and unique_colors=233
figure validation: coordinate_radius_decision_panel.png is 2127x1583 RGB with nonwhite_fraction=0.165067 and unique_colors=852
figure validation: coordinate_objective_radius_candidates.png is 2025x1026 RGB with nonwhite_fraction=0.068088 and unique_colors=2990
visual inspection: decision panel shows selected r=8.00 mm, next r=8.75 mm, the tiny below-cutoff base miss, and base/early_high as the below-cutoff objectives
figure notes: figures/FIGURE_NOTES.md present, run-specific, and identifies the decision panel as the primary figure
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 87-88%; host RAM stayed about 94-95 GiB available
```

## Next Decision

Run seed20365011074 target2 with a 7-source Tx/Rx=60 source-density bracket.

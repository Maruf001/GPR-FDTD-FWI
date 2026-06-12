# Experiment 580: Seed102334155 Target1 Sources=5 Tx/Rx=52.5 Ringdown050

## Purpose

Run the seed102334155 target1 acquisition rescue after the standard
5-source Tx/Rx=60 control selected the exact geometry but missed the base
radius-margin cutoff.

## 1046: Coordinate Optimizer Variable-Depth/Radius Seed102334155 Target1 Sources=5 Tx/Rx=52.5 Ringdown050

Output:

```text
outputs/experiments/1046_coordinate_optimizer_variable_depth_radius_seed102334155_target1_sources5_txrx52p5_ringdown050_objectives
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --tx-rx-offset-mm 52.5 \
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
  --replication-cases source_mismatch_ringdown050_noise10_seed102334155:1.1,-50.0,1.1,0.10,102334155,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed102334155 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed102334155_target1_sources5_txrx52p5_ringdown050_objectives
```

## Results

Run 1046 is exact and narrowly accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 5
tx_rx_offset_mm: 52.5
absolute radius margin: 5.043797e-04
offset from cutoff: +4.379659e-06
relative margin: 2.510151e-02
confidence label: moderate
fallback warning: none
best misfit: 2.009360e-02
next radius misfit: 2.059798e-02
elapsed: 362.2 s
```

Diagnostic objective margins:

```text
base       5.043797e-04  above cutoff
highband   6.625751e-04  above cutoff
late       7.383282e-04  above cutoff
late_high  8.348674e-04  above cutoff
veryhigh   6.155887e-04  above cutoff
early_high 4.589043e-04  below cutoff
```

All six objective variants rank the true target1 geometry first.

## Interpretation

The Tx/Rx=52.5 acquisition rescue is enough to accept target1 for
seed102334155, but only narrowly. It improves the base margin over the
Tx/Rx=60 control by about 1.84e-05 and moves the base objective from weak to
moderate. The remaining early_high weakness should be treated as a robustness
caveat, not a geometry failure, because early_high still ranks the true
geometry first.

This closes the seed102334155 branch:

```text
target0: accepted at sources=8, Tx/Rx=60, with late-window caveat
target2: accepted cleanly after sources=9, Tx/Rx=60 source-density rescue
target1: accepted at sources=5, Tx/Rx=52.5 acquisition rescue, with early_high caveat
```

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.234577 and unique_colors=264
visual inspection: confidence figure is readable and shows one moderate target1 row just above the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 52.5; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 88-89%; peak observed temperature was about 73C
```

## Next Decision

Advance to the next Fibonacci seed, 165580141, and begin with the established
target0 control: 8 sources, Tx/Rx=60, ringdown050, and the six-objective
diagnostic bracket.

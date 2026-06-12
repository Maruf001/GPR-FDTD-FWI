# Experiment 612: Seed4807526976 Target1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Complete the seed4807526976 branch after target0 and target2 accepted at their
standard controls. This run checks target1 with the standard 5-source Tx/Rx=60
coordinate-objective sweep and the six-objective diagnostic bracket.

## 1078: Coordinate Optimizer Variable-Depth/Radius Seed4807526976 Target1 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1078_coordinate_optimizer_variable_depth_radius_seed4807526976_target1_sources5_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed4807526976:1.1,-50.0,1.1,0.10,4807526976,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed4807526976 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed4807526976_target1_sources5_txrx60_ringdown050_objectives
```

## Results

Run 1078 is exact and clean:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 5
tx_rx_offset_mm: 60.0
absolute radius margin: 5.466744e-04
offset from cutoff: +4.667439e-05
relative margin: 3.241063e-02
confidence label: moderate
fallback warning: none
best misfit: 1.686713e-02
next radius misfit: 1.741381e-02
elapsed: 398.2 s
```

Diagnostic objective margins:

```text
base       5.466744e-04  above cutoff
highband   7.200740e-04  above cutoff
late       8.679941e-04  above cutoff
late_high  9.547147e-04  above cutoff
veryhigh   6.433443e-04  above cutoff
early_high 5.229251e-04  above cutoff
```

All six objective variants rank the true target1 geometry first.

## Interpretation

Seed4807526976 target1 passes the standard 5-source Tx/Rx=60 control cleanly.
This closes the seed4807526976 branch without a separate numbered summary
output folder:

```text
target0: accepted at 8 sources, Tx/Rx=60, with late-window caveat
target2: accepted at 5 sources, Tx/Rx=60, with early_high caveat
target1: accepted cleanly at 5 sources, Tx/Rx=60
```

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.249082 and unique_colors=264
visual inspection: confidence figure is readable and shows one moderate target1 row above cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 88-89%; host RAM stayed about 94-95 GiB available
```

## Next Decision

Continue the Fibonacci replication chain with seed7778742049 target0 at the
standard 8-source Tx/Rx=60 control.

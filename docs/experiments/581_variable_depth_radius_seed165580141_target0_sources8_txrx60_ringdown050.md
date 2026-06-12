# Experiment 581: Seed165580141 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Begin the seed165580141 branch with the established target0 standard control:
8 sources, Tx/Rx=60, ringdown050 source mismatch, and the six-objective
diagnostic bracket.

## 1047: Coordinate Optimizer Variable-Depth/Radius Seed165580141 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1047_coordinate_optimizer_variable_depth_radius_seed165580141_target0_sources8_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed165580141:1.1,-50.0,1.1,0.10,165580141,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed165580141 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed165580141_target0_sources8_txrx60_ringdown050_objectives
```

## Results

Run 1047 is exact and narrowly accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 60.0
absolute radius margin: 5.049315e-04
offset from cutoff: +4.931517e-06
relative margin: 3.182686e-02
confidence label: moderate
fallback warning: none
best misfit: 1.586495e-02
next radius misfit: 1.636988e-02
elapsed: 568.1 s
```

Diagnostic objective margins:

```text
base       5.049315e-04  above cutoff
highband   6.433472e-04  above cutoff
late       3.969726e-04  below cutoff
late_high  4.612466e-04  below cutoff
veryhigh   6.183416e-04  above cutoff
early_high 5.351229e-04  above cutoff
```

All six objective variants rank the true target0 geometry first.

## Interpretation

Seed165580141 target0 follows the recurring target0 pattern: exact geometry,
base acceptance with little reserve, and late-window diagnostic weakness. The
late and late_high rows remain below cutoff, but both still rank the true
x/z/r candidate first. Treat this as accepted with a late-window caveat rather
than a failed target0 branch.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.234611 and unique_colors=264
visual inspection: confidence figure is readable and shows one moderate target0 row just above the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 91-92%; peak observed temperature was about 75C
```

## Next Decision

Continue the seed165580141 branch with target2 at 5 sources and Tx/Rx=60.

# Experiment 607: Seed2971215073 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Begin the seed2971215073 branch with the established target0 control:
8 sources, Tx/Rx=60, ringdown050, and the six-objective diagnostic bracket.
This is a substantive GPU FDTD coordinate-objective sweep.

## 1073: Coordinate Optimizer Variable-Depth/Radius Seed2971215073 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1073_coordinate_optimizer_variable_depth_radius_seed2971215073_target0_sources8_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed2971215073:1.1,-50.0,1.1,0.10,2971215073,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed2971215073 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed2971215073_target0_sources8_txrx60_ringdown050_objectives
```

## Results

Run 1073 is exact and accepted, but tight:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 60.0
absolute radius margin: 5.144144e-04
offset from cutoff: +1.441437e-05
relative margin: 3.265610e-02
confidence label: moderate
fallback warning: none
best misfit: 1.575247e-02
next radius misfit: 1.626689e-02
elapsed: 631.1 s
```

Diagnostic objective margins:

```text
base       5.144144e-04  above cutoff
highband   7.101775e-04  above cutoff
late       4.336650e-04  weak
late_high  4.927733e-04  weak
veryhigh   6.531632e-04  above cutoff
early_high 5.955115e-04  above cutoff
```

All six objective variants rank the true target0 geometry first.

## Interpretation

Seed2971215073 target0 passes the standard 8-source Tx/Rx=60 control with a
tight base reserve. Late and late_high are weak, matching the recurring target0
late-window caveat, but no target0 rescue is justified because the base margin
clears the cutoff and every diagnostic objective ranks the true `(150, 80, 5)`
geometry first.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.235514 and unique_colors=264
visual inspection: confidence figure is readable and shows one moderate target0 row above cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 90-91%; host RAM stayed about 94-95 GiB available
```

## Next Decision

Continue seed2971215073 with the standard target2 control: 5 sources, Tx/Rx=60,
ringdown050, and the same six-objective diagnostic bracket.

# Experiment 593: Seed433494437 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Begin the seed433494437 full-ringdown target-specific branch with the
established target0 control: 8 sources, Tx/Rx=60, and the six-objective
diagnostic bracket.

## 1059: Coordinate Optimizer Variable-Depth/Radius Seed433494437 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/1059_coordinate_optimizer_variable_depth_radius_seed433494437_target0_sources8_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed433494437:1.1,-50.0,1.1,0.10,433494437,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed433494437 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed433494437_target0_sources8_txrx60_ringdown050_objectives
```

## Results

Run 1059 is exact and accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 60.0
absolute radius margin: 5.408134e-04
offset from cutoff: +4.081344e-05
relative margin: 3.469098e-02
confidence label: moderate
fallback warning: none
best misfit: 1.558946e-02
next radius misfit: 1.613027e-02
elapsed: 565.1 s
```

Diagnostic objective margins:

```text
base       5.408134e-04  above cutoff
highband   7.083631e-04  above cutoff
late       4.565712e-04  below cutoff
late_high  5.407468e-04  above cutoff
veryhigh   6.469933e-04  above cutoff
early_high 5.907636e-04  above cutoff
```

All six objective variants rank the true target0 geometry first.

## Interpretation

Seed433494437 target0 passes the standard 8-source Tx/Rx=60 control. The
late objective remains below cutoff, matching the recurring target0
late-window caveat seen in prior seeds, but the base objective is accepted and
all diagnostic objectives preserve the true geometry. No target0 rescue is
justified before checking the other targets.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.249933 and unique_colors=264
visual inspection: confidence figure is readable and shows one moderate target0 row above the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 60.0; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 91%; peak observed temperature was about 74C; host RAM stayed about 94-95 GiB available
```

## Next Decision

Continue seed433494437 with target2 at the standard 5-source Tx/Rx=60
control.

# Experiment 592: Seed267914296 Target1 Sources=9 Tx/Rx=52.5 Ringdown050

## Purpose

Run the combined acquisition/source-density rescue for seed267914296 target1
after the 5-source Tx/Rx=52.5 acquisition rescue improved all margins but
still missed the base cutoff.

## 1058: Coordinate Optimizer Variable-Depth/Radius Seed267914296 Target1 Sources=9 Tx/Rx=52.5 Ringdown050

Output:

```text
outputs/experiments/1058_coordinate_optimizer_variable_depth_radius_seed267914296_target1_sources9_txrx52p5_ringdown050_objectives
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 9 \
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
  --replication-cases source_mismatch_ringdown050_noise10_seed267914296:1.1,-50.0,1.1,0.10,267914296,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed267914296 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed267914296_target1_sources9_txrx52p5_ringdown050_objectives
```

## Results

Run 1058 is exact and accepted:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 9
tx_rx_offset_mm: 52.5
absolute radius margin: 5.079560e-04
offset from cutoff: +7.956039e-06
relative margin: 2.891099e-02
confidence label: moderate
fallback warning: none
best misfit: 1.756965e-02
next radius misfit: 1.807761e-02
elapsed: 657.3 s
```

Diagnostic objective margins:

```text
base       5.079560e-04  above cutoff
highband   6.913943e-04  above cutoff
late       7.399051e-04  above cutoff
late_high  8.643360e-04  above cutoff
veryhigh   6.420391e-04  above cutoff
early_high 5.001491e-04  above cutoff
```

All six objective variants rank the true target1 geometry first.

## Interpretation

The 9-source Tx/Rx=52.5 combined rescue closes the seed267914296 target1
branch. It improves the base margin by about 1.85e-05 relative to the
5-source Tx/Rx=52.5 run and by about 4.13e-05 relative to the original
5-source Tx/Rx=60 control. The early_high margin is only 1.49e-07 above
cutoff, so this is accepted with a tight early-window/high-band reserve
caveat rather than as a large-margin result.

This closes the seed267914296 branch:

```text
target0: accepted at 9 sources, Tx/Rx=60, with late and late_high caveats
target2: accepted cleanly at 9 sources, Tx/Rx=60
target1: accepted at 9 sources, Tx/Rx=52.5, with tight early_high reserve
```

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.236402 and unique_colors=264
visual inspection: confidence figure is readable and shows one moderate target1 row just above the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 52.5; sources=9; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 91-92%; peak observed temperature was about 75C; host RAM stayed about 95 GiB available
```

## Next Decision

Advance to the next Fibonacci seed, 433494437, and begin with the established
target0 control: 8 sources, Tx/Rx=60, ringdown050, and the six-objective
diagnostic bracket.

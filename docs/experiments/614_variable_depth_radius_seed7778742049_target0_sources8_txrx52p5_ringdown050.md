# Experiment 614: Seed7778742049 Target0 Sources=8 Tx/Rx=52.5 Ringdown050

## Purpose

Run the target0 acquisition-offset probe after seed7778742049 target0 was exact
but weak at the standard 8-source Tx/Rx=60 control.

## 1080: Coordinate Optimizer Variable-Depth/Radius Seed7778742049 Target0 Sources=8 Tx/Rx=52.5 Ringdown050

Output:

```text
outputs/experiments/1080_coordinate_optimizer_variable_depth_radius_seed7778742049_target0_sources8_txrx52p5_ringdown050_objectives
```

Command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 8 \
  --tx-rx-offset-mm 52.5 \
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
  --replication-cases source_mismatch_ringdown050_noise10_seed7778742049:1.1,-50.0,1.1,0.10,7778742049,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed7778742049 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed7778742049_target0_sources8_txrx52p5_ringdown050_objectives
```

## Results

Run 1080 recovers the exact geometry, but the acquisition probe does not
rescue the base margin:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 0
sources: 8
tx_rx_offset_mm: 52.5
absolute radius margin: 4.436426e-04
offset from cutoff: -5.635741e-05
relative margin: 2.439636e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.818479e-02
next radius misfit: 1.862843e-02
elapsed: 618.5 s
```

Diagnostic objective margins:

```text
base       4.436426e-04  weak, below cutoff
highband   5.680446e-04  above cutoff
late       3.194032e-04  weak, below cutoff
late_high  3.076531e-04  weak, below cutoff
veryhigh   5.095716e-04  above cutoff
early_high 4.807441e-04  weak, below cutoff
```

All six objective variants rank the true target0 geometry first.

## Interpretation

Tx/Rx=52.5 does not rescue seed7778742049 target0. It worsens the base margin
relative to run 1079 by about 1.97e-05, and early_high also moves below
cutoff. The correct response is not to sweep more acquisition offsets blindly.
The seed267914296 precedent says to switch mechanism to a 9-source Tx/Rx=60
source-density bracket when the first acquisition probe moves base confidence
in the wrong direction.

No separate numbered summary output folder was created for this decision.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.205776 and unique_colors=264
visual inspection: confidence figure is readable and shows one weak target0 row below cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 52.5; sources=8; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 90-91%; host RAM stayed about 94-95 GiB available
```

## Next Decision

Run seed7778742049 target0 with 9 sources and Tx/Rx=60 as a source-density
bracket. Create output folder 1081 only for that actual GPU solver run.

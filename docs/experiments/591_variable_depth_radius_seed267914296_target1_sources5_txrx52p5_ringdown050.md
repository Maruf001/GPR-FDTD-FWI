# Experiment 591: Seed267914296 Target1 Sources=5 Tx/Rx=52.5 Ringdown050

## Purpose

Run the standard target1 acquisition rescue after the seed267914296
5-source Tx/Rx=60 control selected the exact geometry but missed the base
radius-margin cutoff.

## 1057: Coordinate Optimizer Variable-Depth/Radius Seed267914296 Target1 Sources=5 Tx/Rx=52.5 Ringdown050

Output:

```text
outputs/experiments/1057_coordinate_optimizer_variable_depth_radius_seed267914296_target1_sources5_txrx52p5_ringdown050_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed267914296_target1_sources5_txrx52p5_ringdown050_objectives
```

## Results

Run 1057 is exact and improved over 1056, but still weak:

```text
final x: [150, 250, 350] mm
final z: [80, 100, 120] mm
final r: [5, 6, 8] mm
target: 1
sources: 5
tx_rx_offset_mm: 52.5
absolute radius margin: 4.894693e-04
offset from cutoff: -1.053073e-05
relative margin: 2.496892e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 1.960314e-02
next radius misfit: 2.009261e-02
elapsed: 362.6 s
```

Diagnostic objective margins:

```text
base       4.894693e-04  below cutoff
highband   6.463780e-04  above cutoff
late       7.213157e-04  above cutoff
late_high  8.054550e-04  above cutoff
veryhigh   5.778609e-04  above cutoff
early_high 4.469744e-04  below cutoff
```

All six objective variants rank the true target1 geometry first.

Compared with the Tx/Rx=60 control in run 1056, Tx/Rx=52.5 improves every
diagnostic margin: base by 2.286e-05, highband by 5.379e-05, late by
7.191e-05, late_high by 7.560e-05, veryhigh by 4.631e-05, and early_high by
5.145e-06.

## Interpretation

The Tx/Rx=52.5 acquisition change moves target1 close to acceptance but does
not close the branch. The geometry is stable and truth-ranked under every
objective, so the failure is still radius-confidence reserve rather than a
location error.

The closest prior policy comparison is seed832040 target1: 5-source
Tx/Rx=52.5 stayed weak, 7-source Tx/Rx=52.5 also stayed weak, and 9-source
Tx/Rx=52.5 became cleanly accepted. Because run 1057 is already only
1.053e-05 below cutoff and the user requested avoiding unnecessary output
folders, the next useful escalation is the accepted combined-policy endpoint:
9 sources at Tx/Rx=52.5.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.228288 and unique_colors=264
visual inspection: confidence figure is readable and shows one weak target1 row just below the 5.0e-4 cutoff scale
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: tx_rx_offset_mm is 52.5; sources=5; summary truth_radius_values_mm is [5.0, 6.0, 8.0]
resources: production GPU utilization was about 88-89%; host RAM remained about 95 GiB available
```

## Next Decision

Run seed267914296 target1 with 9 sources and Tx/Rx=52.5. If that clears the
base cutoff while preserving all-objective truth rank, close the
seed267914296 branch with caveats for target0 late-window reserve and the
target-specific source-density requirements.

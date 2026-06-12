# Experiment 382: Seed21 Target-0 Sources=8 Tx/Rx=60 Ringdown0475

## Purpose

Run 848 lowers seed21 target-0 ringdown from 0.5 to 0.475 after the 8-source
ringdown050 near-miss from run 846 and the failed 9-source rescue from run
847. This brackets the target-0 stress threshold.

## 848: Coordinate Optimizer Variable-Depth/Radius Seed21 Target-0 Sources=8 Tx/Rx=60 Ringdown0475

Output:

```text
outputs/experiments/848_coordinate_optimizer_variable_depth_radius_seed21_target0_sources8_txrx60_ringdown0475_objectives
```

Command:

```text
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
  --replication-cases source_mismatch_ringdown0475_noise10_seed21:1.1,-50.0,1.1,0.10,21,0.475,180.0,0.8 \
  --update-case-label source_mismatch_ringdown0475_noise10_seed21 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed21_target0_sources8_txrx60_ringdown0475_objectives
```

## Results

The final recovered coordinate state is exact:

```text
x = [150, 250, 350] mm
z = [80, 100, 120] mm
r = [5, 6, 8] mm
```

Base confidence row:

```text
case: source_mismatch_ringdown0475_noise10_seed21
target: 0
sources: 8
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 5.086877e-04
relative radius margin: 3.143584e-02
confidence label: moderate
fallback warning: none
best misfit: 0.01618177517696752
next radius misfit: 0.016690462891939428
listed competing geometry: x=150 mm, z=81 mm, r=6.0 mm
elapsed: 599.74 s
```

Diagnostic objective rows all preserved the true target-0 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 5.086877e-04 | above cutoff |
| highband | 6.462765e-04 | above cutoff |
| late | 3.249341e-04 | below cutoff, truth-preserving |
| late_high | 4.076114e-04 | below cutoff, truth-preserving |
| veryhigh | 6.066237e-04 | above cutoff |
| early_high | 5.438538e-04 | above cutoff |

## Interpretation

Run 848 passes but is boundary-level. It clears cutoff by `8.688e-06`, improves
over ringdown050 run 846 by `1.118e-05`, and sits `6.457e-06` below the
lower-stress ringdown0459375 pass from run 826. The threshold is therefore
between 0.475 and 0.5.

Late and late_high remain weak while preserving geometry. The next step should
bracket upward at ringdown049375 rather than summarizing prematurely.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.255829 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_mm is target-specific at 5.0 mm
resources: GPU utilization held around 91%; Python RSS stayed about 451-458 MiB; RAM stayed about 98 GiB available
elapsed: 599.74 s
```

## Next Decision

Run seed21 target 0 at ringdown049375 with 8 sources and Tx/Rx=60.

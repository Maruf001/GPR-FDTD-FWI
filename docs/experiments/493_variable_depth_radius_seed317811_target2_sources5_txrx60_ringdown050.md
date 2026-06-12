# Experiment 493: Seed317811 Target2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run 959 tests the seed317811 target2 standard 5-source control after target0
accepted at 8 sources.

## 959: Coordinate Optimizer Variable-Depth/Radius Seed317811 Target2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/959_coordinate_optimizer_variable_depth_radius_seed317811_target2_sources5_txrx60_ringdown050_objectives
```

Command:

```text
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
  --replication-cases source_mismatch_ringdown050_noise10_seed317811:1.1,-50.0,1.1,0.10,317811,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed317811 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed317811_target2_sources5_txrx60_ringdown050_objectives
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
case: source_mismatch_ringdown050_noise10_seed317811
target: 2
sources: 5
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 4.958067e-04
offset from cutoff: -4.193344e-06
relative radius margin: 2.973991e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 0.016671422191882383
next radius misfit: 0.01716722884834735
listed competing geometry: x=350 mm, z=121 mm, r=8.75 mm
elapsed: about 398.6 s
```

Diagnostic objective rows all preserve the true target2 geometry, but base and
early_high are below cutoff:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 4.958067e-04 | below cutoff |
| highband | 6.014405e-04 | above cutoff |
| late | 7.283523e-04 | above cutoff |
| late_high | 7.820381e-04 | above cutoff |
| veryhigh | 5.925397e-04 | above cutoff |
| early_high | 4.163696e-04 | below cutoff |

## Interpretation

Run 959 is rejected at the standard confidence threshold despite an exact
final coordinate state. The base miss is small, and the top-k table shows the
truth geometry at rank 1 for every objective variant. Escalate target2 to 9
sources before moving to target1.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.239574 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one weak row just below the 5.0e-4 cutoff
figure notes: figures/FIGURE_NOTES.md present and flags the weak target2 row
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target2 truth_radius_mm is 8.0 mm
resources: 5-source GPU checks were about 87-88% utilization with about 96-97 GiB RAM available
```

## Next Decision

Run the target2 9-source rescue. That run is underway as experiment 960.

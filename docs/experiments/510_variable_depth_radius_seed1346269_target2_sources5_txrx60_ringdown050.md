# Experiment 510: Seed1346269 Target2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run 976 tests the standard seed1346269 target2 5-source control after target0
required an 11-source rescue.

## 976: Coordinate Optimizer Variable-Depth/Radius Seed1346269 Target2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/976_coordinate_optimizer_variable_depth_radius_seed1346269_target2_sources5_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed1346269:1.1,-50.0,1.1,0.10,1346269,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed1346269 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed1346269_target2_sources5_txrx60_ringdown050_objectives
```

## Results

The final recovered coordinate state is exact, but the base confidence margin
is weak:

```text
x = [150, 250, 350] mm
z = [80, 100, 120] mm
r = [5, 6, 8] mm
```

Base confidence row:

```text
case: source_mismatch_ringdown050_noise10_seed1346269
target: 2
sources: 5
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 4.913760e-04
offset from cutoff: -8.624013e-06
relative radius margin: 2.884685e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 0.017033956638981468
next radius misfit: 0.017525332625767335
listed competing geometry: x=350 mm, z=121 mm, r=8.75 mm
elapsed: about 398.3 s
```

Diagnostic objective rows all preserve the true target2 geometry, but base and
early_high are below cutoff:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 4.913760e-04 | below cutoff |
| highband | 5.412823e-04 | above cutoff |
| late | 7.015553e-04 | above cutoff |
| late_high | 6.729482e-04 | above cutoff |
| veryhigh | 5.929605e-04 | above cutoff |
| early_high | 3.956581e-04 | below cutoff |

## Interpretation

Run 976 is exact but rejected as a weak 5-source target2 control. Run a
9-source rescue before moving to target1.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.235175 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one weak row below the 5.0e-4 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target2 truth_radius_mm is 8.0 mm
resources: 5-source GPU checks were about 87% utilization with about 96 GiB RAM available
```

## Next Decision

Run the seed1346269 target2 9-source rescue. That run is underway as
experiment 977.

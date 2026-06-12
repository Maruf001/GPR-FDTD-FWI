# Experiment 471: Seed28657 Target2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run 937 tests seed28657 target2 at the standard 5-source full-ringdown control
after target0 passed at 8 sources.

## 937: Coordinate Optimizer Variable-Depth/Radius Seed28657 Target2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/937_coordinate_optimizer_variable_depth_radius_seed28657_target2_sources5_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed28657:1.1,-50.0,1.1,0.10,28657,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed28657 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed28657_target2_sources5_txrx60_ringdown050_objectives
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
case: source_mismatch_ringdown050_noise10_seed28657
target: 2
sources: 5
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 5.256723e-04
offset from cutoff: +2.567229e-05
relative radius margin: 3.077430e-02
confidence label: moderate
fallback warning: none
best misfit: 0.017081534815411168
next radius misfit: 0.01760720710702045
listed competing geometry: x=350 mm, z=121 mm, r=8.75 mm
elapsed: about 395.5 s
```

Diagnostic objective rows all preserve the true target2 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 5.256723e-04 | above cutoff |
| highband | 6.509095e-04 | above cutoff |
| late | 7.940133e-04 | above cutoff |
| late_high | 8.557283e-04 | above cutoff |
| veryhigh | 7.020560e-04 | above cutoff |
| early_high | 4.808689e-04 | below cutoff |

## Interpretation

Run 937 is accepted as the seed28657 target2 5-source control. It has a
moderate base row but only modest reserve, and early_high remains slightly
below cutoff. Continue to target1 at 5 sources.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.256064 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one moderate row above the 5.0e-4 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target2 truth_radius_mm is 8.0 mm
resources: GPU utilization held around 87-88%; RAM stayed about 96 GiB available
```

## Next Decision

Continue the seed28657 branch with target1, sources=5, Tx/Rx=60, and
ringdown050.

# Experiment 470: Seed28657 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Run 936 starts the seed28657 Fibonacci replication branch with the standard
8-source target0 full-ringdown production row.

## 936: Coordinate Optimizer Variable-Depth/Radius Seed28657 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/936_coordinate_optimizer_variable_depth_radius_seed28657_target0_sources8_txrx60_ringdown050_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed28657_target0_sources8_txrx60_ringdown050_objectives
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
target: 0
sources: 8
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 5.720267e-04
offset from cutoff: +7.202671e-05
relative radius margin: 3.611612e-02
confidence label: moderate
fallback warning: none
best misfit: 0.015838540905748773
next radius misfit: 0.016410567613523313
listed competing geometry: x=150 mm, z=81 mm, r=6.0 mm
elapsed: about 629.7 s
```

Diagnostic objective rows all preserve the true target0 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 5.720267e-04 | above cutoff |
| highband | 7.533931e-04 | above cutoff |
| late | 4.819107e-04 | below cutoff |
| late_high | 5.892376e-04 | above cutoff |
| veryhigh | 7.154124e-04 | above cutoff |
| early_high | 6.182228e-04 | above cutoff |

## Interpretation

Run 936 is accepted as the seed28657 target0 8-source control. It does not
need a targeted 9-source rescue, although the late objective remains slightly
below cutoff and should be tracked in the branch summary.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.276810 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one moderate row above the 5.0e-4 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target0 truth_radius_mm is 5.0 mm
resources: GPU utilization held around 90-91%; RAM stayed about 96 GiB available
```

## Next Decision

Continue the seed28657 branch with target2, sources=5, Tx/Rx=60, and
ringdown050.

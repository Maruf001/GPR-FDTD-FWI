# Experiment 377: Seed89 Target-2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run 843 tests whether the seed13 ringdown050 target-specific `8/5/5`
source-count policy transfers to seed89 target 2. This is the remaining
seed89 target after seed89 target 1 passed in run 835 and seed89 target 0
passed in run 842.

## 843: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/843_coordinate_optimizer_variable_depth_radius_seed89_target2_sources5_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed89:1.1,-50.0,1.1,0.10,89,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed89 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target2_sources5_txrx60_ringdown050_objectives
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
case: source_mismatch_ringdown050_noise10_seed89
target: 2
sources: 5
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 4.414917e-04
relative radius margin: 2.627526e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 0.016802558924518016
next radius misfit: 0.01724405060827009
listed competing geometry: x=350 mm, z=121 mm, r=8.75 mm
elapsed: 390.85 s
```

Diagnostic objective rows all preserved the true target-2 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 4.414917e-04 | below cutoff, weak |
| highband | 5.139026e-04 | above cutoff |
| late | 6.611415e-04 | above cutoff |
| late_high | 7.058375e-04 | above cutoff |
| veryhigh | 5.335945e-04 | above cutoff |
| early_high | 3.970436e-04 | below cutoff, truth-preserving |

## Interpretation

Run 843 is exact but not production-confident. It is weaker than seed89
target-2 9-source ringdown0459375 run 822 by `1.545e-04` and weaker than
seed13 target-2 5-source ringdown050 run 838 by `1.468e-04`. It is also below
seed89 target 0 run 842 and target 1 run 835 at the same ringdown050 stress.

The result suggests the seed13 `8/5/5` policy does not transfer to seed89
target 2. Because all objective diagnostics preserve truth, the issue is
margin separation rather than wrong-geometry selection. Restore the old
9-source target-2 acquisition at ringdown050 before creating any seed89
all-target summary.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.226969 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one weak row
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_mm is target-specific at 8.0 mm
resources: GPU utilization held around 87-88%; Python RSS stayed about 447-455 MiB; RAM stayed about 98-99 GiB available
elapsed: 390.85 s
```

## Next Decision

Run seed89 target 2 at ringdown050 with 9 sources and Tx/Rx=60. If 9 sources
restore the margin, seed89 should use an `8/5/9` target-specific policy.

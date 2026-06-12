# Experiment 282: Seed89 Target-1 Tx/Rx=50 Ringdown035 Diagnostic

## Purpose

Run 749 starts a new bounded physics stress after the cross-seed summary in run
748. The previous seed21/seed89 package showed that the Tx/Rx=50
fitted-ringdown final-state branch remains exact/moderate, but target 1 is the
only seed89 row with a lower base margin than seed21. This run tests whether a
stronger fitted ringdown tail worsens that center-target sensitivity.

The only intended stress change relative to run 746 is:

```text
ringdown scale: 0.25 -> 0.35
```

## 749: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-1 Tx/Rx=50 Ringdown035 Objectives

Output:

```text
outputs/experiments/749_coordinate_optimizer_variable_depth_radius_seed89_target1_txrx50_ringdown035_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --tx-rx-offset-mm 50 \
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
  --z-offsets-mm=-1:1:1 \
  --radius-offsets-mm=-1:1:0.25 \
  --replication-cases source_mismatch_ringdown035_noise10_seed89:1.1,-50.0,1.1,0.10,89,0.35,180.0,0.8 \
  --update-case-label source_mismatch_ringdown035_noise10_seed89 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 27 \
  --progress-every 5 \
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target1_txrx50_ringdown035_objectives
```

## Parameters

```text
backend: gpu-cpml
grid step: 1.0 mm
sources: 5
Tx/Rx offset: 50 mm
frequency: 1.5 GHz
truth x/z/r: [150,250,350] / [80,100,120] / [5,6,8] mm
initial x/z/r: truth final state
target index: 1
candidate grid: x offset 0, z offsets -1-1 mm, radius offsets -1-1 mm in 0.25 mm steps
candidate count: 27
source stress: frequency scale 1.1, time shift -50 ps, amplitude 1.1, noise 10%, seed 89, ringdown 0.35
ringdown delay/frequency: 180 ps / 0.8
source fit: frequency grid 0.9/1.0/1.1, time shifts -50/0/50 ps, fitted ringdown coefficient
```

## Artifacts

```text
README.md
data/coordinate_confidence_report.csv
data/coordinate_objective_diagnostics.csv
data/coordinate_objective_top_candidates.csv
data/coordinate_state_history.csv
data/coordinate_step_01_target_1_candidates.csv
data/multi_rebar_coordinate_optimizer_summary.json
figures/coordinate_confidence_margins.png
figures/FIGURE_NOTES.md
run_manifest.json
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
case: source_mismatch_ringdown035_noise10_seed89
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 6.280926e-04
relative radius margin: 2.495734e-02
confidence label: moderate
```

Objective diagnostics:

| Objective | Best x/z/r mm | Next radius mm | Margin abs | Ratio to base |
| --- | --- | ---: | ---: | ---: |
| base | 250 / 100 / 6.0 | 6.25 | 6.280926e-04 | 1.000 |
| highband | 250 / 100 / 6.0 | 6.25 | 7.373192e-04 | 1.174 |
| late | 250 / 100 / 6.0 | 6.25 | 8.454549e-04 | 1.346 |
| late_high | 250 / 100 / 6.0 | 6.25 | 9.563583e-04 | 1.523 |
| veryhigh | 250 / 100 / 6.0 | 6.25 | 7.619131e-04 | 1.213 |
| early_high | 250 / 100 / 6.0 | 6.25 | 4.784323e-04 | 0.762 |

Ringdown025 comparison:

```text
run 746 ringdown025 seed89 target 1:
  base margin: 5.982895e-04
  late_high ratio: 1.432x

run 749 ringdown035 seed89 target 1:
  base margin: 6.280926e-04
  late_high ratio: 1.523x
```

## Interpretation

The stronger ringdown035 stress does not create a center-target failure. Base
remains exact/moderate and the margin is slightly stronger than the ringdown025
seed89 target-1 row. Late_high remains the strongest diagnostic and improves
the target-1 radius separation without changing geometry.

This result narrows the target-1 sensitivity from run 748: target 1 is
seed-sensitive across seed21/seed89, but simply increasing the fitted ringdown
scale from 0.25 to 0.35 does not make the seed89 target-1 result worse.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=162, state history=2, candidates=27
figure validation: coordinate_confidence_margins.png is 1549x903, dynamic range 255, nonblank
visual inspection: confidence figure is readable and matches the single moderate row
figure notes: figures/FIGURE_NOTES.md present
resources: GPU utilization reached about 87-88%; RAM stayed healthy with about 100 GiB available after run
```

## Next Decision

Run ringdown035 target 2 next if resources remain healthy. Target 2 is the
strongest late_high case in the ringdown025 evidence, so it is the most useful
second target for deciding whether ringdown035 deserves an all-target package.

# Experiment 307: Seed13 Target-2 Tx/Rx=50.3125 Linear-Receiver Diagnostic

## Purpose

Run 774 adds seed13 as a third target-2 linear receiver-sampling replication.
The branch question is whether the seed89 weak plateau is common or whether
seed13 follows the seed21 moderate plateau.

## 774: Coordinate Optimizer Variable-Depth/Radius Seed13 Target-2 Tx/Rx=50.3125 Linear Receiver Ringdown025

Output:

```text
outputs/experiments/774_coordinate_optimizer_variable_depth_radius_seed13_target2_txrx50p3125_linear_receiver_ringdown025_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --tx-rx-offset-mm 50.3125 \
  --receiver-sampling linear \
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
  --replication-cases source_mismatch_ringdown025_noise10_seed13:1.1,-50.0,1.1,0.10,13,0.25,180.0,0.8 \
  --update-case-label source_mismatch_ringdown025_noise10_seed13 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 4 \
  --run-name coordinate_optimizer_variable_depth_radius_seed13_target2_txrx50p3125_linear_receiver_ringdown025_objectives
```

## Parameters

```text
backend: gpu-cpml
grid step: 1.0 mm
sources: 5
Tx/Rx offset: 50.3125 mm
receiver sampling: linear
frequency: 1.5 GHz
truth x/z/r: [150,250,350] / [80,100,120] / [5,6,8] mm
initial x/z/r: truth final state
target index: 2
candidate grid: x offset 0, z offsets 0-1 mm, radius offsets 0-1.25 mm in 0.25 mm steps
candidate count: 12
source stress: frequency scale 1.1, time shift -50 ps, amplitude 1.1, noise 10%, seed 13, ringdown 0.25
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
data/coordinate_step_01_target_2_candidates.csv
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
case: source_mismatch_ringdown025_noise10_seed13
receiver sampling: linear
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 6.007860e-04
relative radius margin: 2.194724e-02
confidence label: moderate
best misfit: 0.0273740979527174
elapsed: 387.47 s
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 8.0 | 8.75 | 6.007860e-04 | 1.000 |
| highband | 8.0 | 8.75 | 5.912834e-04 | 0.984 |
| late | 8.0 | 8.75 | 8.706661e-04 | 1.449 |
| late_high | 8.0 | 8.75 | 8.594204e-04 | 1.430 |
| veryhigh | 8.0 | 8.75 | 7.320566e-04 | 1.218 |
| early_high | 8.0 | 8.75 | 3.529805e-04 | 0.588 |

Cross-seed midpoint comparison:

| Seed | Tx/Rx=50 baseline | Linear Tx/Rx=50.3125 | Ratio | Linear confidence |
| --- | ---: | ---: | ---: | --- |
| seed13 | 8.105729e-04 | 6.007860e-04 | 0.741 | moderate |
| seed21 | 8.000475e-04 | 5.779376e-04 | 0.722 | moderate |
| seed89 | 9.935884e-04 | 4.769427e-04 | 0.480 | weak |

## Interpretation

Seed13 behaves like seed21: exact geometry, degraded margin, but still moderate
confidence under linear Tx/Rx=50.3125. Seed89 is now the outlier among the
three tested seeds at this offset.

The strongest truth-preserving diagnostic is `late`, not `late_high`, with a
1.449x ratio to base. Keep base as the production update objective.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903, dynamic range 255, grayscale std 68.4033
visual inspection: confidence figure is readable and correctly flags the moderate row
figure notes: figures/FIGURE_NOTES.md present
resources: GPU utilization held about 87-88%; RAM stayed healthy with about 100 GiB available
```

## Next Decision

Regenerate the cross-seed summary with seed13 included. Then stop this branch
unless a fourth seed is needed to estimate weak-plateau frequency.

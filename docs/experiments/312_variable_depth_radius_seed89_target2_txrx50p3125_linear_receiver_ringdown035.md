# Experiment 312: Seed89 Target-2 Tx/Rx=50.3125 Linear Receiver Ringdown035

## Purpose

Run 779 tests whether the seed89 target-2 weak linear-receiver plateau from
ringdown025 persists under the stronger ringdown035 source condition. It uses
linear receiver sampling at Tx/Rx=50.3125 mm and a full 27-candidate local
target-2 z/radius grid.

## 779: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-2 Tx/Rx=50.3125 Linear Receiver Ringdown035

Output:

```text
outputs/experiments/779_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50p3125_linear_receiver_ringdown035_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50p3125_linear_receiver_ringdown035_objectives
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
candidate grid: x offset 0, z offsets -1/0/+1 mm, radius offsets -1 to +1 mm in 0.25 mm steps
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
case: source_mismatch_ringdown035_noise10_seed89
receiver sampling: linear
target: 2
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm at z=121 mm
absolute radius margin: 4.945264e-04
relative radius margin: 1.978402e-02
confidence label: weak
best misfit: 0.0249962553440002
elapsed: 899.88 s
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 8.0 | 8.75 | 4.945264e-04 | 1.000 |
| highband | 8.0 | 8.75 | 5.274594e-04 | 1.067 |
| late | 8.0 | 8.75 | 7.554792e-04 | 1.528 |
| late_high | 8.0 | 8.75 | 8.350227e-04 | 1.689 |
| veryhigh | 8.0 | 8.75 | 5.854490e-04 | 1.184 |
| early_high | 8.0 | 8.75 | 3.308095e-04 | 0.669 |

Condition comparison:

| Condition | Run | Base margin | Ratio to reference | Confidence |
| --- | ---: | ---: | ---: | --- |
| ringdown035 nearest Tx/Rx=50 | 750 | 1.038879e-03 | 1.000 | strong |
| ringdown035 linear Tx/Rx=50.3125 | 779 | 4.945264e-04 | 0.476 | weak |
| ringdown025 linear Tx/Rx=50.3125 | 765 | 4.769427e-04 | 1.037 vs run 765 | weak |

## Interpretation

Run 779 shows that stronger ringdown035 source stress does not rescue the
seed89 target-2 linear-receiver weak plateau. The best candidate remains the
exact truth, but the margin is only 0.476x the nearest-sampled ringdown035
baseline from run 750. The closest competitor is the coupled `z=121 mm,
r=8.75 mm` geometry, matching the ambiguity pattern seen under ringdown025
linear sampling.

Against run 765, the margin is slightly larger at 1.037x and the best misfit is
lower, but the classification remains weak. This means the exact inversion is
stable while the radius/depth confidence remains too narrow for a point-radius
claim under this acquisition/source condition.

Late_high is again the strongest truth-preserving diagnostic at 1.689x base.
It should be retained as a diagnostic metric, but it is not enough to reclassify
the base objective result.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=162, state history=2, candidates=27
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with full RGB dynamic range
visual inspection: confidence figure is readable and correctly flags the weak row
figure notes: figures/FIGURE_NOTES.md present
resources: GPU utilization held about 86-88%; Python RSS stayed about 450 MiB; RAM stayed about 99 GiB available
```

## Next Decision

Do not spend the next GPU run on another tiny Tx/Rx bisection. The useful next
step is either a compact cross-ringdown linear target-2 summary for reporting,
or a more substantial acquisition change for target 2 that can test whether the
radius/depth ambiguity is geometry-driven rather than only receiver-sampling
driven.

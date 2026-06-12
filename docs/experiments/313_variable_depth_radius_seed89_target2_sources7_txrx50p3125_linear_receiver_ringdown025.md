# Experiment 313: Seed89 Target-2 Sources=7 Linear Receiver Ringdown025

## Purpose

Run 780 tests whether source-count acquisition density resolves the seed89
target-2 linear-receiver radius/depth ambiguity. It repeats the Tx/Rx=50.3125
mm linear receiver condition from run 765 with the same ringdown025 source
stress, but increases the scan from 5 to 7 sources and uses a full 27-candidate
local target-2 z/radius grid.

## 780: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-2 Sources=7 Tx/Rx=50.3125 Linear Receiver Ringdown025

Output:

```text
outputs/experiments/780_coordinate_optimizer_variable_depth_radius_seed89_target2_sources7_txrx50p3125_linear_receiver_ringdown025_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 7 \
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
  --replication-cases source_mismatch_ringdown025_noise10_seed89:1.1,-50.0,1.1,0.10,89,0.25,180.0,0.8 \
  --update-case-label source_mismatch_ringdown025_noise10_seed89 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 27 \
  --progress-every 5 \
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target2_sources7_txrx50p3125_linear_receiver_ringdown025_objectives
```

## Parameters

```text
backend: gpu-cpml
grid step: 1.0 mm
sources: 7
scan x positions: [50, 114, 178, 250, 314, 378, 450] mm
Tx/Rx offset: 50.3125 mm
receiver sampling: linear
frequency: 1.5 GHz
truth x/z/r: [150,250,350] / [80,100,120] / [5,6,8] mm
initial x/z/r: truth final state
target index: 2
candidate grid: x offset 0, z offsets -1/0/+1 mm, radius offsets -1 to +1 mm in 0.25 mm steps
candidate count: 27
source stress: frequency scale 1.1, time shift -50 ps, amplitude 1.1, noise 10%, seed 89, ringdown 0.25
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
case: source_mismatch_ringdown025_noise10_seed89
receiver sampling: linear
target: 2
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm at z=121 mm
absolute radius margin: 6.453160e-04
relative radius margin: 2.311679e-02
confidence label: moderate
best misfit: 0.0279154676106773
elapsed: 1215.84 s
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 8.0 | 8.75 | 6.453160e-04 | 1.000 |
| highband | 8.0 | 8.75 | 7.341617e-04 | 1.138 |
| late | 8.0 | 8.75 | 8.875440e-04 | 1.375 |
| late_high | 8.0 | 8.75 | 1.078086e-03 | 1.671 |
| veryhigh | 8.0 | 8.75 | 8.027198e-04 | 1.244 |
| early_high | 8.0 | 8.75 | 3.456971e-04 | 0.536 |

Acquisition-density comparison:

| Condition | Run | Base margin | Ratio | Confidence |
| --- | ---: | ---: | ---: | --- |
| 5 sources, linear Tx/Rx=50.3125 | 765 | 4.769427e-04 | 1.000 | weak |
| 7 sources, linear Tx/Rx=50.3125 | 780 | 6.453160e-04 | 1.353 vs run 765 | moderate |
| 5 sources, nearest Tx/Rx=50 | 745 | 9.935884e-04 | 0.649 vs run 745 | moderate |

## Interpretation

Run 780 shows a real source-density rescue for the seed89 target-2
linear-receiver condition. The recovered geometry remains exact, and the same
coupled `z=121 mm, r=8.75 mm` candidate remains the next-radius competitor,
but the base margin increases by 35.3% over the 5-source linear baseline and
crosses from weak to moderate.

This is not a full recovery to nearest-grid Tx/Rx=50 behavior. The 7-source
linear row is still only 0.649x the run 745 nearest-grid margin. The careful
claim is that added scan density mitigates the linear receiver ambiguity; it
does not eliminate it.

Late_high remains the strongest truth-preserving diagnostic at 1.671x base.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=162, state history=2, candidates=27
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with full RGB dynamic range
visual inspection: confidence figure is readable and correctly flags the moderate row
figure notes: figures/FIGURE_NOTES.md present
resources: GPU utilization held about 89-90%; Python RSS stayed about 455-459 MiB; RAM stayed about 99-100 GiB available
```

## Next Decision

Run the same target-2 condition with 9 sources once if the goal is to map the
source-density trend. If 9 sources keeps improving the margin, report source
density as the leading mitigation for target-2 linear receiver ambiguity. If it
plateaus near run 780, treat 7 sources as the practical acquisition-density
fix.

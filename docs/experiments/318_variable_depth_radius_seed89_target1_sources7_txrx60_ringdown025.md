# Experiment 318: Seed89 Target-1 Sources=7 Tx/Rx=60 Ringdown025

## Purpose

Run 785 completes the all-target Tx/Rx=60 source-density check. It repeats run
754's target-1 Tx/Rx=60 ringdown025 setup, changing only the scan from 5 to 7
sources while keeping the same 12-candidate local z/radius grid used by runs
783 and 784.

## 785: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-1 Sources=7 Tx/Rx=60 Ringdown025

Output:

```text
outputs/experiments/785_coordinate_optimizer_variable_depth_radius_seed89_target1_sources7_txrx60_ringdown025_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 7 \
  --tx-rx-offset-mm 60 \
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
  --z-offsets-mm=0:1:1 \
  --radius-offsets-mm=0:1.25:0.25 \
  --replication-cases source_mismatch_ringdown025_noise10_seed89:1.1,-50.0,1.1,0.10,89,0.25,180.0,0.8 \
  --update-case-label source_mismatch_ringdown025_noise10_seed89 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 4 \
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target1_sources7_txrx60_ringdown025_objectives
```

## Parameters

```text
backend: gpu-cpml
grid step: 1.0 mm
sources: 7
scan x positions: [50, 114, 178, 250, 314, 378, 450] mm
Tx/Rx offset: 60 mm
receiver sampling: nearest
frequency: 1.5 GHz
truth x/z/r: [150,250,350] / [80,100,120] / [5,6,8] mm
initial x/z/r: truth final state
target index: 1
candidate grid: x offset 0, z offsets 0/+1 mm, radius offsets 0 to +1.25 mm in 0.25 mm steps
candidate count: 12
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
case: source_mismatch_ringdown025_noise10_seed89
receiver sampling: nearest
target: 1
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 3.489046e-04
relative radius margin: 1.913028e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 0.01823834441114069
elapsed: 520.54 s
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 6.0 | 6.25 | 3.489046e-04 | 1.000 |
| highband | 6.0 | 6.25 | 3.480306e-04 | 0.997 |
| late | 6.0 | 6.25 | 4.208206e-04 | 1.206 |
| late_high | 6.0 | 6.25 | 4.172134e-04 | 1.196 |
| veryhigh | 6.0 | 6.25 | 2.885269e-04 | 0.827 |
| early_high | 6.0 | 6.25 | 2.359897e-04 | 0.676 |

Target/source-density comparison:

| Condition | Run | Base margin | Ratio | Confidence |
| --- | ---: | ---: | ---: | --- |
| target 1, Tx/Rx=60, 5 sources | 754 | 5.319351e-04 | 1.000 | moderate |
| target 1, Tx/Rx=60, 7 sources | 785 | 3.489046e-04 | 0.656 vs run 754 | weak |
| target 0, Tx/Rx=60, 7 sources | 784 | 5.677174e-04 | 1.627 vs run 785 | moderate |
| target 2, Tx/Rx=60, 7 sources | 783 | 5.100529e-04 | 1.462 vs run 785 | moderate |

## Interpretation

Run 785 is a negative transfer result for the center target. The geometry stays
exact, but the 7-source Tx/Rx=60 setup reduces the target-1 base margin to
65.6% of the 5-source target-1 baseline from run 754 and changes the confidence
label from moderate to weak.

Together with runs 783 and 784, the Tx/Rx=60 source-density branch is mixed.
The same 7-source aperture rescues target 2 from weak to moderate and mildly
improves already-moderate target 0, but it degrades target 1. Therefore the
source-density effect is target dependent and likely tied to aperture/source
placement rather than a monotonic "more sources is better" rule.

The late and late_high diagnostic windows improve the target-1 radius margin
relative to base while preserving the true radius, but they still do not justify
claiming robust 7-source recovery without another aperture/source-count check.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with full RGB dynamic range
visual inspection: confidence figure is readable and correctly flags the weak row
figure notes: figures/FIGURE_NOTES.md present
resources: GPU utilization held about 89-90%; Python RSS stayed about 453 MiB; RAM stayed about 99 GiB available
```

## Next Decision

Run a bounded target-1 Tx/Rx=60 source-count follow-up before summarizing this
branch. A 9-source target-1 sweep using the same 12-candidate grid is the most
direct check of whether the weak 7-source row is an aperture-placement issue or
a broader degradation from adding sources at Tx/Rx=60.

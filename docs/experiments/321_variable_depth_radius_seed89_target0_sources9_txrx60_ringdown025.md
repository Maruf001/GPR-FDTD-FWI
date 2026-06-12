# Experiment 321: Seed89 Target-0 Sources=9 Tx/Rx=60 Ringdown025

## Purpose

Run 788 completes the all-target 9-source Tx/Rx=60 comparison. It repeats the
target-0 Tx/Rx=60 ringdown025 setup with the same 12-candidate local z/radius
grid, changing the scan from 7 to 9 sources.

## 788: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-0 Sources=9 Tx/Rx=60 Ringdown025

Output:

```text
outputs/experiments/788_coordinate_optimizer_variable_depth_radius_seed89_target0_sources9_txrx60_ringdown025_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 9 \
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
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target0_sources9_txrx60_ringdown025_objectives
```

## Parameters

```text
backend: gpu-cpml
grid step: 1.0 mm
sources: 9
scan x positions: [50, 98, 146, 194, 250, 298, 346, 394, 450] mm
Tx/Rx offset: 60 mm
receiver sampling: nearest
frequency: 1.5 GHz
truth x/z/r: [150,250,350] / [80,100,120] / [5,6,8] mm
initial x/z/r: truth final state
target index: 0
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
data/coordinate_step_01_target_0_candidates.csv
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
target: 0
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 4.631165e-04
relative radius margin: 2.488450e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 0.018610643669095112
next radius misfit: 0.019073760208331667
competing geometry: x=150 mm, z=81 mm, r=6.0 mm
elapsed: 726.35 s
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 5.0 | 5.25 | 4.631165e-04 | 1.000 |
| highband | 5.0 | 5.25 | 5.022170e-04 | 1.084 |
| late | 5.0 | 5.25 | 3.211869e-04 | 0.694 |
| late_high | 5.0 | 5.25 | 3.347836e-04 | 0.723 |
| veryhigh | 5.0 | 5.25 | 6.091996e-04 | 1.315 |
| early_high | 5.0 | 5.25 | 4.013461e-04 | 0.867 |

Target-0 source-count comparison:

| Condition | Run | Base margin | Ratio | Confidence |
| --- | ---: | ---: | ---: | --- |
| target 0, Tx/Rx=60, 5 sources | 756 | 5.193087e-04 | 1.000 | moderate |
| target 0, Tx/Rx=60, 7 sources | 784 | 5.677174e-04 | 1.093 vs run 756 | moderate |
| target 0, Tx/Rx=60, 9 sources | 788 | 4.631165e-04 | 0.892 vs run 756 | weak |
| target 0, 9 sources vs 7 sources | 788/784 | 4.631165e-04 | 0.816 | weak |

All-target 9-source context:

| Condition | Run | Base margin | Confidence |
| --- | ---: | ---: | --- |
| target 0, Tx/Rx=60, 9 sources | 788 | 4.631165e-04 | weak |
| target 1, Tx/Rx=60, 9 sources | 786 | 5.181917e-04 | moderate |
| target 2, Tx/Rx=60, 9 sources | 787 | 5.780025e-04 | moderate |

## Interpretation

Run 788 is a negative target-0 source-density result. The coordinate state
remains exact, but the 9-source base margin falls below both the 5-source and
7-source target-0 baselines and changes the confidence label to weak.

Together with runs 786 and 787, the all-target 9-source Tx/Rx=60 branch is
mixed. Nine sources recover target 1 from the weak 7-source row and further
improve target 2 over its 7-source rescue, but nine sources degrade the shallow
target 0. The correct conclusion is source-count and aperture sensitivity by
target, not a monotonic source-density rule.

The veryhigh diagnostic is the strongest truth-preserving target-0 variant in
this run, raising the margin to 1.315x base. Base confidence remains weak,
however, so the point radius should still be treated cautiously under the
9-source aperture.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with full RGB dynamic range
visual inspection: confidence figure is readable and correctly flags the weak row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 5.0 mm after the metadata fix
resources: GPU utilization held about 91%; Python RSS stayed about 453-461 MiB; RAM stayed about 99 GiB available
```

## Next Decision

Do not increase source count blindly. If the branch needs one more GPU run,
test target 0 with an intermediate 8-source aperture to see whether the weak
row appears only at the 9-source layout or begins immediately above 7 sources.
Otherwise, write a compact source-density decision table in documentation only,
without allocating a summary-only output folder.

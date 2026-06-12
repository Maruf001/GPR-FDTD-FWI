# Experiment 320: Seed89 Target-2 Sources=9 Tx/Rx=60 Ringdown025

## Purpose

Run 787 tests whether the target-2 Tx/Rx=60 source-density rescue from run 783
continues with 9 sources or becomes nonmonotonic, as seen in the separate
linear-receiver source-density branch. It repeats the target-2 Tx/Rx=60
ringdown025 setup with the same 12-candidate local z/radius grid, changing the
scan from 7 to 9 sources.

## 787: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-2 Sources=9 Tx/Rx=60 Ringdown025

Output:

```text
outputs/experiments/787_coordinate_optimizer_variable_depth_radius_seed89_target2_sources9_txrx60_ringdown025_objectives
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
  --target-indices 2 \
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
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target2_sources9_txrx60_ringdown025_objectives
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
target index: 2
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
receiver sampling: nearest
target: 2
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm at z=121 mm
absolute radius margin: 5.780025e-04
relative radius margin: 3.105763e-02
confidence label: moderate
best misfit: 0.018610643669095112
next radius misfit: 0.019188646149224928
elapsed: 721.71 s
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 8.0 | 8.75 | 5.780025e-04 | 1.000 |
| highband | 8.0 | 8.75 | 5.880514e-04 | 1.017 |
| late | 8.0 | 8.75 | 8.370708e-04 | 1.448 |
| late_high | 8.0 | 8.75 | 8.463791e-04 | 1.464 |
| veryhigh | 8.0 | 8.75 | 7.480872e-04 | 1.294 |
| early_high | 8.0 | 8.75 | 4.033512e-04 | 0.698 |

Target-2 source-count comparison:

| Condition | Run | Base margin | Ratio | Confidence |
| --- | ---: | ---: | ---: | --- |
| target 2, Tx/Rx=60, 5 sources | 755 | 4.318875e-04 | 1.000 | weak |
| target 2, Tx/Rx=60, 7 sources | 783 | 5.100529e-04 | 1.181 vs run 755 | moderate |
| target 2, Tx/Rx=60, 9 sources | 787 | 5.780025e-04 | 1.339 vs run 755 | moderate |
| target 2, 9 sources vs 7 sources | 787/783 | 5.780025e-04 | 1.133 | moderate |
| target 2, Tx/Rx=50, 5 sources | 745 | 9.935884e-04 | 0.581 for run 787 vs run 745 | moderate |

All-target source-density context:

| Condition | Run | Base margin | Confidence |
| --- | ---: | ---: | --- |
| target 0, Tx/Rx=60, 7 sources | 784 | 5.677174e-04 | moderate |
| target 1, Tx/Rx=60, 9 sources | 786 | 5.181917e-04 | moderate |
| target 2, Tx/Rx=60, 9 sources | 787 | 5.780025e-04 | moderate |

## Interpretation

Run 787 shows that the target-2 Tx/Rx=60 source-density rescue continues from
7 to 9 sources. The base margin rises from 4.319e-04 with 5 sources to
5.101e-04 with 7 sources and 5.780e-04 with 9 sources. This differs from the
linear-receiver branch, where target-2 at Tx/Rx=50.3125 improved at 7 sources
but dropped at 9 sources.

The recovery is still incomplete relative to the original Tx/Rx=50 target-2
baseline: run 787 is only 0.581x run 745's base margin. The correct claim is
therefore bounded. More source coverage can mitigate the Tx/Rx=60 weak target-2
condition, but it does not fully restore the strongest nearest-grid acquisition.

Late_high is again the strongest truth-preserving diagnostic, only slightly
ahead of late. Both improve the target-2 margin substantially over base.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with full RGB dynamic range
visual inspection: confidence figure is readable and correctly flags the moderate row
figure notes: figures/FIGURE_NOTES.md present
resources: GPU utilization held about 90-91%; Python RSS stayed about 455-463 MiB; RAM stayed about 99-100 GiB available
metadata note: this run was generated before the coordinate-optimizer scalar truth_radius_mm fix; truth_radius_values_mm, the final state, candidate rows, and confidence CSV correctly record target 2 at r=8 mm
```

## Next Decision

The summary metadata scalar is now fixed for future single-target optimizer
runs. Use one more substantive run only if needed: target 0 with 9 sources would
make the Tx/Rx=60 9-source all-target comparison complete. Otherwise, create a
single compact source-density decision table from runs 754-756 and 783-787
without allocating a new summary-only experiment folder.

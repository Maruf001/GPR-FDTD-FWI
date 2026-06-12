# Experiment 319: Seed89 Target-1 Sources=9 Tx/Rx=60 Ringdown025

## Purpose

Run 786 tests whether the weak target-1 result from run 785 is a 7-source
aperture placement effect or a broader degradation from adding sources at
Tx/Rx=60. It repeats the target-1 Tx/Rx=60 ringdown025 setup with the same
12-candidate local z/radius grid, changing the scan from 7 to 9 sources.

## 786: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-1 Sources=9 Tx/Rx=60 Ringdown025

Output:

```text
outputs/experiments/786_coordinate_optimizer_variable_depth_radius_seed89_target1_sources9_txrx60_ringdown025_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target1_sources9_txrx60_ringdown025_objectives
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
absolute radius margin: 5.181917e-04
relative radius margin: 2.784383e-02
confidence label: moderate
best misfit: 0.018610643669095112
next radius misfit: 0.0191288353493136
competing geometry: x=250 mm, z=101 mm, r=6.75 mm
elapsed: 730.49 s
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 6.0 | 6.25 | 5.181917e-04 | 1.000 |
| highband | 6.0 | 6.25 | 5.675606e-04 | 1.095 |
| late | 6.0 | 6.25 | 7.300614e-04 | 1.409 |
| late_high | 6.0 | 6.25 | 8.553740e-04 | 1.651 |
| veryhigh | 6.0 | 6.25 | 6.053259e-04 | 1.168 |
| early_high | 6.0 | 6.25 | 3.870808e-04 | 0.747 |

Source-count comparison:

| Condition | Run | Base margin | Ratio | Confidence |
| --- | ---: | ---: | ---: | --- |
| target 1, Tx/Rx=60, 5 sources | 754 | 5.319351e-04 | 1.000 | moderate |
| target 1, Tx/Rx=60, 7 sources | 785 | 3.489046e-04 | 0.656 vs run 754 | weak |
| target 1, Tx/Rx=60, 9 sources | 786 | 5.181917e-04 | 0.974 vs run 754 | moderate |
| target 1, 9 sources vs 7 sources | 786/785 | 5.181917e-04 | 1.485 | moderate |

All-target 7/9-source context:

| Condition | Run | Base margin | Confidence |
| --- | ---: | ---: | --- |
| target 0, Tx/Rx=60, 7 sources | 784 | 5.677174e-04 | moderate |
| target 1, Tx/Rx=60, 9 sources | 786 | 5.181917e-04 | moderate |
| target 2, Tx/Rx=60, 7 sources | 783 | 5.100529e-04 | moderate |

## Interpretation

Run 786 shows that the weak target-1 row in run 785 is not a general penalty
from increasing source count. With 9 sources, target 1 returns to moderate
confidence and nearly matches the original 5-source target-1 baseline, while
improving 1.485x over the 7-source aperture.

The result points to aperture/source placement sensitivity. The 7-source scan
contains a source directly over x=250 mm but has wider neighboring source
spacing; the 9-source scan also includes x=250 mm but adds denser flanking
coverage around the center target. Under Tx/Rx=60, that denser aperture appears
to restore the center-target radius separation.

The strongest truth-preserving diagnostic is late_high, with a 1.651x margin
relative to base. That supports keeping late_high in the diagnostic matrix, but
the base row alone is already moderate in this run.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with full RGB dynamic range
visual inspection: confidence figure is readable and correctly flags the moderate row
figure notes: figures/FIGURE_NOTES.md present
resources: GPU utilization held about 91%; Python RSS stayed about 457 MiB; RAM stayed about 99 GiB available
```

## Next Decision

Run target 0 or target 2 at Tx/Rx=60 with 9 sources only if a full all-target
9-source comparison is needed. Otherwise, create one compact decision summary
from runs 754-756 and 783-786, because the key branch conclusion is now
specific: source density helps, hurts, or recovers depending on target and
aperture placement.

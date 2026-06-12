# Experiment 326: Seed89 Target-1 Custom 8+Center Tx/Rx=60 Ringdown025

## Purpose

Run 792 tests the first custom-aperture hypothesis from the completed Tx/Rx=60
source-density synthesis. The aperture keeps the 8-source layout that worked
best for target 0 and adds an exact center shot at x=250 mm to test whether
target 1's borderline weak 8-source row can be rescued without using the
uniform 9-source layout.

## 792: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-1 Custom 8+Center Tx/Rx=60 Ringdown025

Output:

```text
outputs/experiments/792_coordinate_optimizer_variable_depth_radius_seed89_target1_custom8pluscenter_txrx60_ringdown025_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 9 \
  --scan-x-values-mm 50,106,162,218,250,274,330,386,450 \
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
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target1_custom8pluscenter_txrx60_ringdown025_objectives
```

## Parameters

```text
backend: gpu-cpml
grid step: 1.0 mm
sources recorded: 9
custom scan x positions: [50, 106, 162, 218, 250, 274, 330, 386, 450] mm
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
absolute radius margin: 4.847434e-04
relative radius margin: 2.606509e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 0.01859742131503284
next radius misfit: 0.019082164706094962
competing geometry: x=250 mm, z=101 mm, r=6.75 mm
elapsed: 718.18 s
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 6.0 | 6.25 | 4.847434e-04 | 1.000 |
| highband | 6.0 | 6.25 | 5.176579e-04 | 1.068 |
| late | 6.0 | 6.25 | 5.797876e-04 | 1.196 |
| late_high | 6.0 | 6.25 | 6.277414e-04 | 1.295 |
| veryhigh | 6.0 | 6.25 | 4.857167e-04 | 1.002 |
| early_high | 6.0 | 6.25 | 3.434744e-04 | 0.709 |

Target-1 aperture comparison:

| Condition | Run | Base margin | Ratio | Confidence |
| --- | ---: | ---: | ---: | --- |
| uniform 5 sources | 754 | 5.319351e-04 | 1.000 | moderate |
| uniform 7 sources | 785 | 3.489046e-04 | 0.656 vs run 754 | weak |
| uniform 8 sources | 790 | 4.999206e-04 | 0.940 vs run 754 | weak |
| uniform 9 sources | 786 | 5.181917e-04 | 0.974 vs run 754 | moderate |
| custom 8+center | 792 | 4.847434e-04 | 0.911 vs run 754 | weak |
| custom 8+center vs uniform 8 | 792/790 | 4.847434e-04 | 0.970 | weak |
| custom 8+center vs uniform 9 | 792/786 | 4.847434e-04 | 0.935 | weak |

## Interpretation

Run 792 is a negative custom-aperture result. Adding the exact x=250 mm center
shot to the otherwise strong 8-source layout does not rescue target 1. The
geometry remains exact, but the base margin is weak and is slightly below the
plain 8-source target-1 row from run 790.

This rejects the simple explanation that the 8-source target-1 weakness was
caused only by missing a source at the target-center x coordinate. The full
uniform 9-source layout still performs better for target 1, so the useful
information appears to come from the broader 9-source aperture pattern rather
than just the center sample.

Late_high remains truth-preserving and improves the margin to 1.295x base, but
this is weaker than the late_high lift in the plain 8-source target-1 row
(1.492x base). Do not spend target-0/target-2 GPU runs on this exact custom
aperture until a stronger design reason is identified.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.247 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly flags the weak row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 6.0 mm
resources: GPU utilization held mostly about 90-91%; Python RSS stayed about 431-459 MiB; RAM stayed about 99-100 GiB available
tests before run: focused helper tests 34 passed; full suite 300 passed
```

## Next Decision

Do not continue this custom 8+center aperture to target 0 or target 2. The next
source-layout experiment should either isolate which uniform 9-source flank
positions help target 1 or transfer the best existing uniform settings to a
different stress condition. A bounded next candidate is a target-1 custom
aperture that keeps the uniform 9-source center and inner flank positions while
removing the target-0/target-2 near-flank positions suspected in the target-0
9-source dip.

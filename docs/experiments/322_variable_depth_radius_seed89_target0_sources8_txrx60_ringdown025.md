# Experiment 322: Seed89 Target-0 Sources=8 Tx/Rx=60 Ringdown025

## Purpose

Run 789 checks whether the weak target-0 9-source result from run 788 begins
immediately above 7 sources or is specific to the 9-source aperture layout. It
uses the same Tx/Rx=60 ringdown025 setup and 12-candidate local z/radius grid,
changing only the scan to 8 sources.

## 789: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-0 Sources=8 Tx/Rx=60 Ringdown025

Output:

```text
outputs/experiments/789_coordinate_optimizer_variable_depth_radius_seed89_target0_sources8_txrx60_ringdown025_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 8 \
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
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target0_sources8_txrx60_ringdown025_objectives
```

## Parameters

```text
backend: gpu-cpml
grid step: 1.0 mm
sources: 8
scan x positions: [50, 106, 162, 218, 274, 330, 386, 450] mm
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
absolute radius margin: 5.899921e-04
relative radius margin: 2.922561e-02
confidence label: moderate
best misfit: 0.020187501415122554
next radius misfit: 0.020777493482340818
competing geometry: x=150 mm, z=81 mm, r=6.0 mm
elapsed: 620.43 s
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 5.0 | 5.25 | 5.899921e-04 | 1.000 |
| highband | 5.0 | 5.25 | 5.935681e-04 | 1.006 |
| late | 5.0 | 5.25 | 3.990265e-04 | 0.676 |
| late_high | 5.0 | 5.25 | 4.199406e-04 | 0.712 |
| veryhigh | 5.0 | 5.25 | 5.951839e-04 | 1.009 |
| early_high | 5.0 | 5.25 | 4.138234e-04 | 0.701 |

Target-0 source-count comparison:

| Condition | Run | Base margin | Ratio | Confidence |
| --- | ---: | ---: | ---: | --- |
| target 0, Tx/Rx=60, 5 sources | 756 | 5.193087e-04 | 1.000 | moderate |
| target 0, Tx/Rx=60, 7 sources | 784 | 5.677174e-04 | 1.093 vs run 756 | moderate |
| target 0, Tx/Rx=60, 8 sources | 789 | 5.899921e-04 | 1.136 vs run 756 | moderate |
| target 0, Tx/Rx=60, 9 sources | 788 | 4.631165e-04 | 0.892 vs run 756 | weak |
| target 0, 8 sources vs 9 sources | 789/788 | 5.899921e-04 | 1.274 | moderate |

## Interpretation

Run 789 shows that target 0's weak 9-source row is not an immediate penalty
above 7 sources. The 8-source aperture is exact/moderate and has the largest
target-0 base margin of the tested 5/7/8/9-source Tx/Rx=60 settings.

The target-0 source-density behavior is therefore nonmonotonic and
aperture-layout sensitive. Eight sources helps, nine sources hurts. This is
consistent with the broader branch conclusion that source count cannot be used
as a monotonic quality control by itself.

Unlike run 788, highband and veryhigh only slightly improve the target-0 margin
over base. The base row is already moderate, so no diagnostic rescue is needed.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with full RGB dynamic range
visual inspection: confidence figure is readable and correctly flags the moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 5.0 mm after the metadata fix
resources: GPU utilization held about 90-91%; Python RSS stayed about 451-459 MiB; RAM stayed about 99 GiB available
```

## Next Decision

Run target 1 at 8 sources and Tx/Rx=60 if the branch needs the corresponding
intermediate check. Target 1 was weak at 7 sources and moderate at 9 sources,
so 8 sources will determine whether the center-target recovery begins at 8 or
requires the 9-source aperture.

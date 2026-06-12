# Experiment 324: Seed89 Target-2 Sources=8 Tx/Rx=60 Ringdown025

## Purpose

Run 791 completes the all-target 8-source Tx/Rx=60 ringdown025 aperture check.
Target 2 was moderate at 7 and 9 sources, so this run tests whether the
intermediate aperture follows a smooth source-density trend or behaves like
the aperture-sensitive target-0 and target-1 branches.

## 791: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-2 Sources=8 Tx/Rx=60 Ringdown025

Output:

```text
outputs/experiments/791_coordinate_optimizer_variable_depth_radius_seed89_target2_sources8_txrx60_ringdown025_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target2_sources8_txrx60_ringdown025_objectives
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
next radius: 8.75 mm
absolute radius margin: 5.243427e-04
relative radius margin: 2.597363e-02
confidence label: moderate
best misfit: 0.020187501415122554
next radius misfit: 0.020711844112627522
competing geometry: x=350 mm, z=121 mm, r=8.75 mm
elapsed: 627.78 s
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 8.0 | 8.75 | 5.243427e-04 | 1.000 |
| highband | 8.0 | 8.75 | 5.770957e-04 | 1.101 |
| late | 8.0 | 8.75 | 7.865320e-04 | 1.500 |
| late_high | 8.0 | 8.75 | 8.688188e-04 | 1.657 |
| veryhigh | 8.0 | 8.75 | 5.853168e-04 | 1.116 |
| early_high | 8.0 | 8.75 | 3.329803e-04 | 0.635 |

Target-2 source-count comparison:

| Condition | Run | Base margin | Ratio | Confidence |
| --- | ---: | ---: | ---: | --- |
| target 2, Tx/Rx=60, 5 sources | 755 | 4.318875e-04 | 1.000 | weak |
| target 2, Tx/Rx=60, 7 sources | 783 | 5.100529e-04 | 1.181 vs run 755 | moderate |
| target 2, Tx/Rx=60, 8 sources | 791 | 5.243427e-04 | 1.214 vs run 755 | moderate |
| target 2, Tx/Rx=60, 9 sources | 787 | 5.780025e-04 | 1.339 vs run 755 | moderate |
| target 2, 8 sources vs 7 sources | 791/783 | 5.243427e-04 | 1.028 | moderate |
| target 2, 8 sources vs 9 sources | 791/787 | 5.243427e-04 | 0.907 | moderate |

## Interpretation

Run 791 completes the all-target 8-source Tx/Rx=60 comparison. Target 2
remains exact and moderate at 8 sources, with a base margin slightly above the
7-source row and below the 9-source row. Unlike target 0, it does not show a
9-source dip; unlike target 1, it does not stay weak at 8 sources.

The target-2 source-density trend is therefore the smoothest of the three
targets under Tx/Rx=60 ringdown025. The 5-source row is weak, and 7, 8, and 9
sources are all moderate. The recovery is still incomplete relative to the
best Tx/Rx=50 baseline from the broader branch, but within the Tx/Rx=60 source
count sweep, target 2 benefits consistently from increased source density.

Late_high is again the strongest truth-preserving diagnostic, improving the
margin to 1.657x base. This supports the same diagnostic direction seen in the
target-1 8-source row, but the base row is already moderate and does not need a
diagnostic rescue.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.265 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly flags the moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 8.0 mm after the metadata fix
resources: GPU utilization held about 90-91%; Python RSS stayed about 451-460 MiB; RAM stayed about 99 GiB available
```

## Next Decision

Close the target-specific 8-source Tx/Rx=60 sweep and create a compact
source-density decision synthesis from runs 754-756, 783-791 before launching
more GPU runs. The synthesis should emphasize aperture sensitivity rather than
a monotonic source-count rule.

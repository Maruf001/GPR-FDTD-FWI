# Experiment 330: Seed89 Target-2 Sources=9 Tx/Rx=60 Ringdown035

## Purpose

Run 796 completes the best-source-count ringdown035 transfer set. Target 2
improved smoothly from 5 to 7 to 8 to 9 sources under ringdown025, so this run
tests whether its strongest tested Tx/Rx=60 source count remains stable under
the stronger ringdown035 source stress.

## 796: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-2 Sources=9 Tx/Rx=60 Ringdown035

Output:

```text
outputs/experiments/796_coordinate_optimizer_variable_depth_radius_seed89_target2_sources9_txrx60_ringdown035_objectives
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
  --replication-cases source_mismatch_ringdown035_noise10_seed89:1.1,-50.0,1.1,0.10,89,0.35,180.0,0.8 \
  --update-case-label source_mismatch_ringdown035_noise10_seed89 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 4 \
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target2_sources9_txrx60_ringdown035_objectives
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
receiver sampling: nearest
target: 2
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 6.058657e-04
relative radius margin: 3.401139e-02
confidence label: moderate
best misfit: 0.017813609736609577
next radius misfit: 0.01841947542294253
competing geometry: x=350 mm, z=121 mm, r=8.75 mm
elapsed: 709.95 s
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 8.0 | 8.75 | 6.058657e-04 | 1.000 |
| highband | 8.0 | 8.75 | 6.669764e-04 | 1.101 |
| late | 8.0 | 8.75 | 8.848231e-04 | 1.460 |
| late_high | 8.0 | 8.75 | 9.234238e-04 | 1.524 |
| veryhigh | 8.0 | 8.75 | 7.718416e-04 | 1.274 |
| early_high | 8.0 | 8.75 | 4.693684e-04 | 0.775 |

Target-2 transfer comparison:

| Condition | Run | Base margin | Ratio | Confidence |
| --- | ---: | ---: | ---: | --- |
| uniform 5 sources, ringdown025 | 755 | 4.318875e-04 | 1.000 | weak |
| uniform 7 sources, ringdown025 | 783 | 5.100529e-04 | 1.181 vs run 755 | moderate |
| uniform 8 sources, ringdown025 | 791 | 5.243427e-04 | 1.214 vs run 755 | moderate |
| uniform 9 sources, ringdown025 | 787 | 5.780025e-04 | 1.339 vs run 755 | moderate |
| uniform 9 sources, ringdown035 | 796 | 6.058657e-04 | 1.403 vs run 755 | moderate |
| ringdown035 9 sources vs ringdown025 9 sources | 796/787 | 6.058657e-04 | 1.048 | moderate |
| ringdown035 9 sources vs ringdown025 8 sources | 796/791 | 6.058657e-04 | 1.155 | moderate |

## Interpretation

Run 796 is a positive target-2 transfer result. The 9-source aperture remains
exact and moderate under ringdown035, and the base margin is 1.048x the
ringdown025 9-source row from run 787. This completes the target-specific
best-source-count transfer set: target 0 at 8 sources, target 1 at 9 sources,
and target 2 at 9 sources all transfer positively to ringdown035.

Target 2 continues to show the smoothest source-density behavior in this
Tx/Rx=60 branch. The 5-source row was weak, while 7, 8, 9, and now 9-source
ringdown035 rows are all moderate.

Late_high is the strongest diagnostic at 1.524x base, with late also strong at
1.460x base. Since the base row is already moderate, these diagnostics support
the decision but are not needed to rescue the result.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.302 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly flags the moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 8.0 mm
resources: GPU utilization held mostly about 91%; Python RSS stayed about 441-459 MiB; RAM stayed about 99 GiB available
```

## Next Decision

Run target 0 at 9 sources under ringdown035 if the next question is whether a
single uniform 9-source aperture becomes viable for all targets under stronger
ringdown. Target 1 and target 2 are now moderate at 9 sources under
ringdown035; target 0 is the remaining unknown because its ringdown025
9-source row was weak.

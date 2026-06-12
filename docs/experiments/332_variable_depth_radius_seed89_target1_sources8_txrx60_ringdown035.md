# Experiment 332: Seed89 Target-1 Sources=8 Tx/Rx=60 Ringdown035

## Purpose

Run 798 tests whether uniform 8 sources can become an all-target Tx/Rx=60
setting under the stronger ringdown035 source stress. Target 0 is already
moderate at 8 sources under ringdown035 from run 795, while target 1 was the
weak row at 8 sources under ringdown025.

## 798: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-1 Sources=8 Tx/Rx=60 Ringdown035

Output:

```text
outputs/experiments/798_coordinate_optimizer_variable_depth_radius_seed89_target1_sources8_txrx60_ringdown035_objectives
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
  --target-indices 1 \
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
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target1_sources8_txrx60_ringdown035_objectives
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
target index: 1
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
case: source_mismatch_ringdown035_noise10_seed89
receiver sampling: nearest
target: 1
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 4.925235e-04
relative radius margin: 2.634666e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 0.018693962248696704
next radius misfit: 0.019186485708495196
competing geometry: x=250 mm, z=101 mm, r=6.75 mm
elapsed: 618.22 s
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 6.0 | 6.25 | 4.925235e-04 | 1.000 |
| highband | 6.0 | 6.25 | 5.802090e-04 | 1.178 |
| late | 6.0 | 6.25 | 6.622489e-04 | 1.345 |
| late_high | 6.0 | 6.25 | 7.614154e-04 | 1.546 |
| veryhigh | 6.0 | 6.25 | 5.354026e-04 | 1.087 |
| early_high | 6.0 | 6.25 | 3.861053e-04 | 0.784 |

Target-1 8/9-source comparison:

| Condition | Run | Base margin | Ratio | Confidence |
| --- | ---: | ---: | ---: | --- |
| uniform 5 sources, ringdown025 | 754 | 5.319351e-04 | 1.000 | moderate |
| uniform 8 sources, ringdown025 | 790 | 4.999206e-04 | 0.940 vs run 754 | weak |
| uniform 9 sources, ringdown025 | 786 | 5.181917e-04 | 0.974 vs run 754 | moderate |
| uniform 9 sources, ringdown035 | 794 | 5.424900e-04 | 1.020 vs run 754 | moderate |
| uniform 8 sources, ringdown035 | 798 | 4.925235e-04 | 0.926 vs run 754 | weak |
| ringdown035 8 sources vs ringdown025 8 sources | 798/790 | 4.925235e-04 | 0.985 | weak |
| ringdown035 8 sources vs ringdown035 9 sources | 798/794 | 4.925235e-04 | 0.908 | weak |

Uniform 8 ringdown035 status:

| Target | Run | Base margin | Confidence |
| ---: | ---: | ---: | --- |
| 0 | 795 | 5.954728e-04 | moderate |
| 1 | 798 | 4.925235e-04 | weak |
| 2 | not run | not recorded | unknown |

## Interpretation

Run 798 is a boundary negative result for uniform 8 sources under ringdown035.
Target 1 remains exact, but the base margin is below the moderate cutoff and
is essentially unchanged from the ringdown025 8-source row. Therefore stronger
ringdown does not rescue target 1 at 8 sources.

Together with run 797, this closes the simple all-target uniform-aperture
hypotheses under ringdown035: uniform 9 fails target 0, and uniform 8 fails
target 1. The target-specific best counts remain 8 sources for target 0 and 9
sources for targets 1 and 2.

Late_high is strongly truth-preserving at 1.546x base, similar to earlier
target-1 rows, but the base confidence policy still labels the row weak.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.251 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly flags the weak row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 6.0 mm
resources: GPU utilization held mostly about 90-91%; Python RSS stayed about 441-458 MiB; RAM stayed about 99 GiB available
```

## Next Decision

Stop the simple uniform 8/9 all-target source-count search for ringdown035.
The evidence supports target-specific source counts, not one global uniform
count. The next substantive branch should either test a principled
multi-objective aperture-design method or move to a different acquisition
factor.

# Experiment 323: Seed89 Target-1 Sources=8 Tx/Rx=60 Ringdown025

## Purpose

Run 790 tests whether the center-target Tx/Rx=60 recovery begins at 8 sources
or requires the 9-source aperture. It uses the same 12-candidate local
z/radius grid as the 7-source and 9-source target-1 runs.

## 790: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-1 Sources=8 Tx/Rx=60 Ringdown025

Output:

```text
outputs/experiments/790_coordinate_optimizer_variable_depth_radius_seed89_target1_sources8_txrx60_ringdown025_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target1_sources8_txrx60_ringdown025_objectives
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
absolute radius margin: 4.999206e-04
relative radius margin: 2.476387e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 0.020187501415122554
next radius misfit: 0.020687422043947197
competing geometry: x=250 mm, z=101 mm, r=6.75 mm
elapsed: 628.15 s
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 6.0 | 6.25 | 4.999206e-04 | 1.000 |
| highband | 6.0 | 6.25 | 5.444519e-04 | 1.089 |
| late | 6.0 | 6.25 | 6.680348e-04 | 1.336 |
| late_high | 6.0 | 6.25 | 7.460789e-04 | 1.492 |
| veryhigh | 6.0 | 6.25 | 5.292651e-04 | 1.059 |
| early_high | 6.0 | 6.25 | 3.429602e-04 | 0.686 |

Target-1 source-count comparison:

| Condition | Run | Base margin | Ratio | Confidence |
| --- | ---: | ---: | ---: | --- |
| target 1, Tx/Rx=60, 5 sources | 754 | 5.319351e-04 | 1.000 | moderate |
| target 1, Tx/Rx=60, 7 sources | 785 | 3.489046e-04 | 0.656 vs run 754 | weak |
| target 1, Tx/Rx=60, 8 sources | 790 | 4.999206e-04 | 0.940 vs run 754 | weak |
| target 1, Tx/Rx=60, 9 sources | 786 | 5.181917e-04 | 0.974 vs run 754 | moderate |
| target 1, 8 sources vs 7 sources | 790/785 | 4.999206e-04 | 1.433 | weak |
| target 1, 8 sources vs 9 sources | 790/786 | 4.999206e-04 | 0.965 | weak |

## Interpretation

Run 790 is a borderline weak target-1 result. It is much stronger than the
7-source aperture and nearly recovers the 5-source baseline, but it remains
just below the base moderate threshold and therefore retains the weak label.

This narrows the center-target source-count transition. Seven sources is weak,
eight sources is borderline weak, and nine sources is moderate. The center
target therefore requires the 9-source aperture among the tested Tx/Rx=60
layouts.

Late_high is the strongest truth-preserving diagnostic at 1.492x base. The
diagnostic row suggests recoverable signal separation, but the base confidence
policy still treats the 8-source point radius cautiously.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with full RGB dynamic range
visual inspection: confidence figure is readable and correctly flags the weak row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 6.0 mm after the metadata fix
resources: GPU utilization held about 90-91%; Python RSS stayed about 451-459 MiB; RAM stayed about 99 GiB available
```

## Next Decision

Run target 2 at 8 sources if the branch needs the complete all-target
8-source set. Target 2 was moderate at both 7 and 9 sources; the 8-source row
will show whether its Tx/Rx=60 improvement is smooth between those apertures or
also aperture-sensitive.

# Experiment 328: Seed89 Target-1 Sources=9 Tx/Rx=60 Ringdown035

## Purpose

Run 794 transfers the best target-1 uniform Tx/Rx=60 source count from the
ringdown025 source-density branch to a stronger ringdown035 stress. It follows
the failed custom-aperture runs 792 and 793 by returning to the uniform
9-source aperture that previously gave target 1 a moderate row in run 786.

## 794: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-1 Sources=9 Tx/Rx=60 Ringdown035

Output:

```text
outputs/experiments/794_coordinate_optimizer_variable_depth_radius_seed89_target1_sources9_txrx60_ringdown035_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target1_sources9_txrx60_ringdown035_objectives
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
absolute radius margin: 5.424900e-04
relative radius margin: 3.045368e-02
confidence label: moderate
best misfit: 0.017813609736609577
next radius misfit: 0.018356099713112157
competing geometry: x=250 mm, z=101 mm, r=6.75 mm
elapsed: 715.74 s
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 6.0 | 6.25 | 5.424900e-04 | 1.000 |
| highband | 6.0 | 6.25 | 6.550960e-04 | 1.208 |
| late | 6.0 | 6.25 | 7.672781e-04 | 1.414 |
| late_high | 6.0 | 6.25 | 9.417537e-04 | 1.736 |
| veryhigh | 6.0 | 6.25 | 6.440164e-04 | 1.187 |
| early_high | 6.0 | 6.25 | 4.589039e-04 | 0.846 |

Target-1 transfer comparison:

| Condition | Run | Base margin | Ratio | Confidence |
| --- | ---: | ---: | ---: | --- |
| uniform 5 sources, ringdown025 | 754 | 5.319351e-04 | 1.000 | moderate |
| uniform 8 sources, ringdown025 | 790 | 4.999206e-04 | 0.940 vs run 754 | weak |
| uniform 9 sources, ringdown025 | 786 | 5.181917e-04 | 0.974 vs run 754 | moderate |
| custom 8+center, ringdown025 | 792 | 4.847434e-04 | 0.911 vs run 754 | weak |
| custom wide-center, ringdown025 | 793 | 4.841472e-04 | 0.910 vs run 754 | weak |
| uniform 9 sources, ringdown035 | 794 | 5.424900e-04 | 1.020 vs run 754 | moderate |
| ringdown035 uniform 9 vs ringdown025 uniform 9 | 794/786 | 5.424900e-04 | 1.047 | moderate |
| ringdown035 uniform 9 vs custom 8+center | 794/792 | 5.424900e-04 | 1.119 | moderate |
| ringdown035 uniform 9 vs custom wide-center | 794/793 | 5.424900e-04 | 1.121 | moderate |

## Interpretation

Run 794 is a positive transfer result. The uniform 9-source aperture remains
exact and moderate under the stronger ringdown035 stress, and the base margin
is 1.047x the corresponding ringdown025 uniform 9-source row from run 786.

This reinforces the conclusion from runs 792 and 793: target 1 benefits from
the full uniform 9-source aperture pattern, not merely from adding a center
shot or a pair of wider center flanks to the 8-source layout. The stronger
ringdown stress also does not destabilize the fitted source-profile solution;
the recovered ringdown scale is 0.3507 and the fitted ringdown coefficient is
0.3857.

Late_high is the strongest truth-preserving diagnostic at 1.736x base. Since
the base row is already moderate, this is supporting evidence rather than a
rescue condition.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.274 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly flags the moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 6.0 mm
resources: GPU utilization held mostly about 91%; Python RSS stayed about 431-461 MiB; RAM stayed about 99 GiB available
```

## Next Decision

Continue the ringdown035 transfer branch with target 0 at its best ringdown025
uniform source count: 8 sources. This tests whether the target-0 8-source
advantage is stable under stronger ringdown or whether source-density
nonmonotonicity changes with the source stress.

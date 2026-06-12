# Experiment 359: Seed21 Target-2 Sources=9 Tx/Rx=60 Ringdown0459375

## Purpose

Run 825 extends the seed21 all-target ringdown0459375 transfer branch beyond
target 1. It tests target 2 with 9 sources and Tx/Rx=60 at the strongest
passing seed13 target-1 stress level.

## 825: Coordinate Optimizer Variable-Depth/Radius Seed21 Target-2 Sources=9 Tx/Rx=60 Ringdown0459375

Output:

```text
outputs/experiments/825_coordinate_optimizer_variable_depth_radius_seed21_target2_sources9_txrx60_ringdown0459375_objectives
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
  --replication-cases source_mismatch_ringdown0459375_noise10_seed21:1.1,-50.0,1.1,0.10,21,0.459375,180.0,0.8 \
  --update-case-label source_mismatch_ringdown0459375_noise10_seed21 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed21_target2_sources9_txrx60_ringdown0459375_objectives
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
case: source_mismatch_ringdown0459375_noise10_seed21
target: 2
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 5.252174e-04
relative radius margin: 3.227870e-02
confidence label: moderate
fallback warning: none
best misfit: 0.01627133295985389
next radius misfit: 0.016796550409482563
competing geometry: x=350 mm, z=121 mm, r=8.75 mm
elapsed: 689.98 s
```

Diagnostic objective rows all preserved the true target-2 geometry:

| Objective | Margin | Ratio vs base | Best misfit |
| --- | ---: | ---: | ---: |
| base | 5.252174e-04 | 1.000 | 1.627133e-02 |
| highband | 6.782748e-04 | 1.291 | 2.235872e-04 |
| late | 7.549030e-04 | 1.437 | 1.947813e-02 |
| late_high | 9.014727e-04 | 1.716 | 2.392419e-04 |
| veryhigh | 7.026718e-04 | 1.338 | 2.630528e-04 |
| early_high | 4.929564e-04 | 0.939 | 6.836619e-05 |

## Interpretation

Seed21 target 2 transfers successfully at ringdown0459375. The base row is
exact/moderate and retains 0.984x of the seed21 target-2 ringdown035 baseline
from run 804. Its `5.252174e-04` margin is only `2.522e-05` above the cutoff,
so target 2 is currently the seed21 limiting row.

The early_high diagnostic falls below the production cutoff but preserves the
true geometry. This should be reported as a diagnostic weak-margin row in the
seed21 all-target summary rather than as a failed target-2 transfer.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.253 and full 0-255 RGB-converted dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 8.0 mm
resources: GPU utilization held mostly about 91%; Python RSS stayed about 441-463 MiB; RAM stayed about 98 GiB available
elapsed: 689.98 s
```

## Next Decision

Complete seed21 all-target ringdown0459375 transfer with target 0 at 8 sources
and Tx/Rx=60, then summarize runs 820, 825, and the target-0 run.

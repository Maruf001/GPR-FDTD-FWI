# Experiment 354: Seed21 Target-1 Sources=9 Tx/Rx=60 Ringdown0459375

## Purpose

Run 820 completes the target-1 cross-seed transfer check at the highest passing
seed13 target-1 stress level. It tests seed21 target 1 with 9 sources and
Tx/Rx=60 at ringdown0459375.

## 820: Coordinate Optimizer Variable-Depth/Radius Seed21 Target-1 Sources=9 Tx/Rx=60 Ringdown0459375

Output:

```text
outputs/experiments/820_coordinate_optimizer_variable_depth_radius_seed21_target1_sources9_txrx60_ringdown0459375_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed21_target1_sources9_txrx60_ringdown0459375_objectives
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
target: 1
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 5.560564e-04
relative radius margin: 3.417399e-02
confidence label: moderate
fallback warning: none
best misfit: 0.01627133295985389
next radius misfit: 0.016827389369848896
competing geometry: x=250 mm, z=101 mm, r=6.75 mm
elapsed: 698.91 s
```

Diagnostic objective rows all preserved the true target-1 geometry:

| Objective | Margin | Ratio vs base | Best misfit |
| --- | ---: | ---: | ---: |
| base | 5.560564e-04 | 1.000 | 1.627133e-02 |
| highband | 7.325334e-04 | 1.317 | 2.235872e-04 |
| late | 8.452108e-04 | 1.520 | 1.947813e-02 |
| late_high | 9.998349e-04 | 1.798 | 2.392419e-04 |
| veryhigh | 6.712160e-04 | 1.207 | 2.630528e-04 |
| early_high | 5.250274e-04 | 0.944 | 6.836619e-05 |

## Interpretation

Seed21 target 1 transfers successfully at ringdown0459375. The production base
row remains exact/moderate with a `5.561e-04` margin, which is `5.606e-05`
above the cutoff. Compared with its own ringdown035 baseline from run 803,
seed21 keeps 0.978x of the margin. Compared with seed13 and seed89 at the same
stress, seed21 is 1.111x and 1.046x stronger.

Runs 814, 819, and 820 now provide the complete three-seed target-1 transfer
set at ringdown0459375.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.267 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 6.0 mm
resources: GPU utilization held mostly about 91%; Python RSS stayed about 453-463 MiB; RAM stayed about 98-99 GiB available
elapsed: 698.91 s
```

## Next Decision

Create a three-seed target-1 ringdown0459375 transfer summary from runs 814,
819, and 820.


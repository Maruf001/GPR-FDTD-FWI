# Experiment 368: Seed13 Target-1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run 834 tests the direct prediction from the 5-source acquisition-boundary
summary: if the 5-source acquisition adds a stable `~4.2e-05` target-1 margin,
then the old 9-source ringdown050 weak row should become a moderate pass.

## 834: Coordinate Optimizer Variable-Depth/Radius Seed13 Target-1 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/834_coordinate_optimizer_variable_depth_radius_seed13_target1_sources5_txrx60_ringdown050_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
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
  --replication-cases source_mismatch_ringdown050_noise10_seed13:1.1,-50.0,1.1,0.10,13,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed13 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed13_target1_sources5_txrx60_ringdown050_objectives
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
case: source_mismatch_ringdown050_noise10_seed13
target: 1
sources: 5
scan x positions: [50, 146, 250, 346, 450] mm
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 5.293926e-04
relative radius margin: 3.062064e-02
confidence label: moderate
fallback warning: none
best misfit: 0.017288749596645378
next radius misfit: 0.01781814220474888
listed competing geometry: x=250 mm, z=101 mm, r=6.75 mm
elapsed: 383.81 s
```

Diagnostic objective rows all preserved the true target-1 geometry:

| Objective | Margin | Ratio vs base | Best misfit |
| --- | ---: | ---: | ---: |
| base | 5.293926e-04 | 1.000 | 1.728875e-02 |
| highband | 6.861861e-04 | 1.296 | 2.617388e-04 |
| late | 7.607571e-04 | 1.437 | 2.089346e-02 |
| late_high | 8.547865e-04 | 1.615 | 2.596133e-04 |
| veryhigh | 6.435775e-04 | 1.216 | 3.264007e-04 |
| early_high | 5.177570e-04 | 0.978 | 9.097209e-05 |

## Interpretation

Run 834 confirms the predicted 5-source ringdown050 rescue. The old 9-source
ringdown050 row, run 810, was weak with a `4.879320e-04` margin. Under the
5-source aperture, run 834 is exact/moderate with a `5.293926e-04` margin,
improving by `4.146e-05` and preserving the same about-1.085x matched-stress
ratio seen in the lower stress summary.

The margin is lower than run 832 at ringdown0475 by `8.811e-06`, but it still
clears cutoff by `2.939e-05`. All objective diagnostics preserve truth and all
are above cutoff, including early_high at `5.178e-04`.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.267615 and full 0-255 RGB-converted dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 6.0 mm
resources: GPU utilization held mostly about 87-88%; Python RSS stayed about 447-454 MiB; RAM stayed about 98-99 GiB available
elapsed: 383.81 s
```

## Next Decision

Start cross-seed transfer of the 5-source ringdown050 target-1 policy with
seed89 target 1 at the same Tx/Rx=60 acquisition and diagnostic objective
suite.

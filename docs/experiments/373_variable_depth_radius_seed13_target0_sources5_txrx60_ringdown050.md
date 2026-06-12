# Experiment 373: Seed13 Target-0 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run 839 tests seed13 target 0 under the same fixed 5-source ringdown050 policy
that passed target 1 and target 2. This completes the seed13 all-target check
for the fixed 5-source acquisition, while also testing whether target 0 needs
the old higher source count.

## 839: Coordinate Optimizer Variable-Depth/Radius Seed13 Target-0 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/839_coordinate_optimizer_variable_depth_radius_seed13_target0_sources5_txrx60_ringdown050_objectives
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
  --target-indices 0 \
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
  --run-name coordinate_optimizer_variable_depth_radius_seed13_target0_sources5_txrx60_ringdown050_objectives
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
target: 0
sources: 5
scan x positions: [50, 146, 250, 346, 450] mm
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 5.081346e-04
relative radius margin: 2.939105e-02
confidence label: moderate
fallback warning: none
best misfit: 0.017288749596645378
next radius misfit: 0.017796884164174846
listed competing geometry: x=150 mm, z=81 mm, r=6.0 mm
elapsed: 384.75 s
```

Diagnostic objective rows all preserved the true target-0 geometry:

| Objective | Margin | Ratio vs base | Status |
| --- | ---: | ---: | --- |
| base | 5.081346e-04 | 1.000 | above cutoff |
| highband | 6.400635e-04 | 1.260 | above cutoff |
| late | 4.475087e-04 | 0.881 | below cutoff, truth-preserving |
| late_high | 4.905356e-04 | 0.965 | below cutoff, truth-preserving |
| veryhigh | 6.779849e-04 | 1.334 | above cutoff |
| early_high | 5.311137e-04 | 1.045 | above cutoff |

## Interpretation

Run 839 is a target-0 pass, but a boundary-level one. The production base row
is exact/moderate and clears cutoff by only `8.135e-06`. The late and
late_high diagnostics fall below cutoff while preserving the true target-0
geometry.

Target 0 is much weaker under the fixed 5-source policy than target 1 or
target 2. It is `2.126e-05` below seed13 target-1 run 834 and `8.015e-05`
below seed13 target-2 run 838 at the same ringdown050 stress. It is also
`7.231e-05` below the old 8-source ringdown0459375 target-0 transfer row from
run 817.

This suggests the ringdown050 policy should be target-specific rather than
fixed 5-source for all targets. The next test should restore the old target-0
source density while keeping ringdown050.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.257720 and full 0-255 RGB-converted dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 5.0 mm
resources: GPU utilization held mostly about 88%; Python RSS stayed about 449-456 MiB; RAM stayed about 98-99 GiB available
elapsed: 384.75 s
```

## Next Decision

Run seed13 target 0 at ringdown050 with 8 sources and Tx/Rx=60. If it
strengthens target 0, the ringdown050 seed13 policy should become
target-specific, likely 8/5/5 rather than fixed 5/5/5.

# Experiment 388: Seed21 Target-0 Sources=8 Tx/Rx=60 Ringdown049453125

## Purpose

Run 854 tests the lower midpoint after ringdown04953125 failed in run 853.
The purpose is to refine the seed21 target-0 threshold around the production
cutoff without changing acquisition geometry.

## 854: Coordinate Optimizer Variable-Depth/Radius Seed21 Target-0 Sources=8 Tx/Rx=60 Ringdown049453125

Output:

```text
outputs/experiments/854_coordinate_optimizer_variable_depth_radius_seed21_target0_sources8_txrx60_ringdown049453125_objectives
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
  --replication-cases source_mismatch_ringdown049453125_noise10_seed21:1.1,-50.0,1.1,0.10,21,0.49453125,180.0,0.8 \
  --update-case-label source_mismatch_ringdown049453125_noise10_seed21 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed21_target0_sources8_txrx60_ringdown049453125_objectives
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
case: source_mismatch_ringdown049453125_noise10_seed21
target: 0
sources: 8
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 5.000315e-04
relative radius margin: 3.169134e-02
confidence label: moderate
fallback warning: none
best misfit: 0.01577554864504403
next radius misfit: 0.01627558012842073
elapsed: 605.4 s
```

Diagnostic objective rows all preserved the true target-0 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 5.000315e-04 | above cutoff |
| highband | 6.454569e-04 | above cutoff |
| late | 3.289704e-04 | below cutoff, truth-preserving |
| late_high | 4.122925e-04 | below cutoff, truth-preserving |
| veryhigh | 6.085930e-04 | above cutoff |
| early_high | 5.504875e-04 | above cutoff |

## Interpretation

Run 854 passes by only `3.148e-08`, so it is accepted but not robust. This is
a threshold point, not a reserve point. It narrows the accepted/failed seed21
target-0 interval to `[0.49453125, 0.4953125)`.

The late and late_high diagnostic objectives remain below cutoff while
preserving the true target-0 geometry. That matches the shallow-target pattern
seen throughout this stress branch.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.236320 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_mm is target-specific at 5.0 mm
resources: GPU utilization held around 91%; RAM stayed about 98 GiB available
elapsed: 605.4 s
```

## Next Decision

Run seed21 target 0 at ringdown0494921875 with the same 8-source Tx/Rx=60
configuration. This tests the upper midpoint between accepted run 854 and
failed run 853.

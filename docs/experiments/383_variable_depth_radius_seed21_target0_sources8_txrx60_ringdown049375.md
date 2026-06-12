# Experiment 383: Seed21 Target-0 Sources=8 Tx/Rx=60 Ringdown049375

## Purpose

Run 849 tests the upper side of the seed21 target-0 ringdown bracket after
ringdown0475 passed in run 848 and ringdown050 missed in run 846.

## 849: Coordinate Optimizer Variable-Depth/Radius Seed21 Target-0 Sources=8 Tx/Rx=60 Ringdown049375

Output:

```text
outputs/experiments/849_coordinate_optimizer_variable_depth_radius_seed21_target0_sources8_txrx60_ringdown049375_objectives
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
  --replication-cases source_mismatch_ringdown049375_noise10_seed21:1.1,-50.0,1.1,0.10,21,0.49375,180.0,0.8 \
  --update-case-label source_mismatch_ringdown049375_noise10_seed21 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed21_target0_sources8_txrx60_ringdown049375_objectives
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
case: source_mismatch_ringdown049375_noise10_seed21
target: 0
sources: 8
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 5.003891e-04
relative radius margin: 3.168683e-02
confidence label: moderate
fallback warning: none
best misfit: 0.015791706591648455
next radius misfit: 0.0162920956418347
listed competing geometry: x=150 mm, z=81 mm, r=6.0 mm
elapsed: 605.34 s
```

Diagnostic objective rows all preserved the true target-0 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 5.003891e-04 | above cutoff |
| highband | 6.455179e-04 | above cutoff |
| late | 3.288128e-04 | below cutoff, truth-preserving |
| late_high | 4.121153e-04 | below cutoff, truth-preserving |
| veryhigh | 6.085196e-04 | above cutoff |
| early_high | 5.502444e-04 | above cutoff |

## Interpretation

Run 849 is a pass, but only barely. It clears cutoff by `3.891e-07`, so it
should be treated as the seed21 target-0 upper practical stress boundary, not
as a robust margin. Ringdown050 remains rejected for seed21 target 0 under the
current source/objective policy.

The next seed21 target-transfer run should use the same ringdown049375 stress
for target 2, with 9 sources because seed89 target 2 needed the 9-source
rescue.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.246042 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_mm is target-specific at 5.0 mm
resources: GPU utilization held around 90-91%; Python RSS stayed about 451-461 MiB; RAM stayed about 98 GiB available
elapsed: 605.34 s
```

## Next Decision

Run seed21 target 2 at ringdown049375 with 9 sources and Tx/Rx=60.

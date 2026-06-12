# Experiment 462: Seed10946 Target2 Sources=9 Tx/Rx=60 Ringdown050

## Purpose

Run 928 tests the targeted 9-source rescue after seed10946 target2 was exact
but weak at the 5-source control.

## 928: Coordinate Optimizer Variable-Depth/Radius Seed10946 Target2 Sources=9 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/928_coordinate_optimizer_variable_depth_radius_seed10946_target2_sources9_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed10946:1.1,-50.0,1.1,0.10,10946,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed10946 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed10946_target2_sources9_txrx60_ringdown050_objectives
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
case: source_mismatch_ringdown050_noise10_seed10946
target: 2
sources: 9
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 5.592681e-04
offset from cutoff: +5.926810e-05
relative radius margin: 3.576983e-02
confidence label: moderate
fallback warning: none
best misfit: 0.015635188910180727
next radius misfit: 0.016194457008067296
listed competing geometry: x=350 mm, z=121 mm, r=8.75 mm
elapsed: about 717.9 s
```

Diagnostic objective rows all preserve the true target2 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 5.592681e-04 | above cutoff |
| highband | 6.989243e-04 | above cutoff |
| late | 8.540429e-04 | above cutoff |
| late_high | 8.939400e-04 | above cutoff |
| veryhigh | 7.360320e-04 | above cutoff |
| early_high | 4.888483e-04 | below cutoff |

## Interpretation

Run 928 rescues seed10946 target2 with moderate base reserve. It is accepted,
though early_high remains slightly below cutoff. Continue to target1 at the
standard 5-source control.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.271399 and full dynamic range
visual inspection: confidence figure is readable and shows one moderate row above the 5.0e-4 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target2 truth_radius_mm is 8.0 mm
resources: GPU utilization held around 91%; RAM stayed about 96 GiB available
```

## Next Decision

Continue the seed10946 branch with target1, sources=5, Tx/Rx=60, and
ringdown050.

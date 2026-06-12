# Experiment 389: Seed21 Target-0 Sources=8 Tx/Rx=60 Ringdown0494921875

## Purpose

Run 855 tests the upper midpoint between accepted run 854 and rejected run
853 for the seed21 target-0 threshold branch.

## 855: Coordinate Optimizer Variable-Depth/Radius Seed21 Target-0 Sources=8 Tx/Rx=60 Ringdown0494921875

Output:

```text
outputs/experiments/855_coordinate_optimizer_variable_depth_radius_seed21_target0_sources8_txrx60_ringdown0494921875_objectives
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
  --replication-cases source_mismatch_ringdown0494921875_noise10_seed21:1.1,-50.0,1.1,0.10,21,0.494921875,180.0,0.8 \
  --update-case-label source_mismatch_ringdown0494921875_noise10_seed21 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed21_target0_sources8_txrx60_ringdown0494921875_objectives
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
case: source_mismatch_ringdown0494921875_noise10_seed21
target: 0
sources: 8
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 4.998524e-04
relative radius margin: 3.170039e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 0.015767473094228403
next radius misfit: 0.016267325461848253
elapsed: 605.4 s
```

Diagnostic objective rows all preserved the true target-0 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 4.998524e-04 | below cutoff, weak |
| highband | 6.454254e-04 | above cutoff |
| late | 3.290491e-04 | below cutoff, truth-preserving |
| late_high | 4.123808e-04 | below cutoff, truth-preserving |
| veryhigh | 6.086295e-04 | above cutoff |
| early_high | 5.506084e-04 | above cutoff |

## Interpretation

Run 855 is another exact but weak near-miss. It misses cutoff by
`1.476e-07`, so it remains rejected as a production policy row.

Together with run 854, this brackets the seed21 target-0 threshold in the
interval `[0.49453125, 0.494921875)`. The next lower midpoint is the only
useful continuation if we want one more threshold refinement.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.233677 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one weak row
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_mm is target-specific at 5.0 mm
resources: GPU utilization held around 91%; RAM stayed about 98 GiB available
elapsed: 605.4 s
```

## Next Decision

Run seed21 target 0 at ringdown04947265625 with the same 8-source Tx/Rx=60
configuration. This lower midpoint tests whether the accepted boundary can be
moved above run 854.

# Experiment 446: Seed2584 Target2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run 912 tests seed2584 target2 at the 5-source full-ringdown control after
target0 was rescued at 9 sources.

## 912: Coordinate Optimizer Variable-Depth/Radius Seed2584 Target2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/912_coordinate_optimizer_variable_depth_radius_seed2584_target2_sources5_txrx60_ringdown050_objectives
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
  --target-indices 2 \
  --passes 1 \
  --x-offsets-mm=0 \
  --z-offsets-mm=0:1:1 \
  --radius-offsets-mm=0:1.25:0.25 \
  --replication-cases source_mismatch_ringdown050_noise10_seed2584:1.1,-50.0,1.1,0.10,2584,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed2584 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed2584_target2_sources5_txrx60_ringdown050_objectives
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
case: source_mismatch_ringdown050_noise10_seed2584
target: 2
sources: 5
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 5.528720e-04
offset from cutoff: +5.287201e-05
relative radius margin: 3.293314e-02
confidence label: moderate
fallback warning: none
best misfit: 0.016787710901228395
next radius misfit: 0.017340582911007693
listed competing geometry: x=350 mm, z=121 mm, r=8.75 mm
elapsed: about 397.8 s
```

Diagnostic objective rows all preserve the true target2 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 5.528720e-04 | above cutoff |
| highband | 6.614402e-04 | above cutoff |
| late | 8.311015e-04 | above cutoff |
| late_high | 8.131028e-04 | above cutoff |
| veryhigh | 6.867633e-04 | above cutoff |
| early_high | 4.725436e-04 | below cutoff |

## Interpretation

Run 912 is an accepted seed2584 target2 row. It passes at the 5-source control,
so target2 does not need a 9-source rescue. This keeps the seed2584 branch
focused on target1 after target0 already needed source-density rescue.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.271141 and full dynamic range
visual inspection: confidence figure is readable and shows one moderate row above the 5.0e-4 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target2 truth_radius_mm is 8.0 mm
resources: GPU utilization held around 87%; RAM stayed about 97 GiB available
```

## Next Decision

Continue the seed2584 branch with target1, sources=5, Tx/Rx=60, and
ringdown050.

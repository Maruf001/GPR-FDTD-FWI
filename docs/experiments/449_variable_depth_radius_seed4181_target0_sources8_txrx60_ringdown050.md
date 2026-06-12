# Experiment 449: Seed4181 Target0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Run 915 starts the seed4181 branch with the standard target0 8-source
full-ringdown control.

## 915: Coordinate Optimizer Variable-Depth/Radius Seed4181 Target0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/915_coordinate_optimizer_variable_depth_radius_seed4181_target0_sources8_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed4181:1.1,-50.0,1.1,0.10,4181,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed4181 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed4181_target0_sources8_txrx60_ringdown050_objectives
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
case: source_mismatch_ringdown050_noise10_seed4181
target: 0
sources: 8
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 5.844588e-04
offset from cutoff: +8.445876e-05
relative radius margin: 3.769209e-02
confidence label: moderate
fallback warning: none
best misfit: 0.015506139446628035
next radius misfit: 0.0160905982071135
listed competing geometry: x=150 mm, z=81 mm, r=6.0 mm
elapsed: about 630.6 s
```

Diagnostic objective rows all preserve the true target0 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 5.844588e-04 | above cutoff |
| highband | 7.667026e-04 | above cutoff |
| late | 5.216869e-04 | above cutoff |
| late_high | 6.104873e-04 | above cutoff |
| veryhigh | 6.848315e-04 | above cutoff |
| early_high | 6.198516e-04 | above cutoff |

## Interpretation

Run 915 is an accepted seed4181 target0 row. It has more reserve than the
low-margin target0 rows from seed1597 and seed2584, and every diagnostic
objective variant clears cutoff. Do not run a target0 rescue.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.285754 and full dynamic range
visual inspection: confidence figure is readable and shows one moderate row above the 5.0e-4 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target0 truth_radius_mm is 5.0 mm
resources: GPU utilization held around 90%; RAM stayed about 97 GiB available
```

## Next Decision

Continue the seed4181 branch with target2, sources=5, Tx/Rx=60, and
ringdown050.

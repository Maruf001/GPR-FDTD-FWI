# Experiment 475: Seed46368 Target2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run 941 tests seed46368 target2 at the standard 5-source full-ringdown control
after target0 passed at 8 sources with low reserve.

## 941: Coordinate Optimizer Variable-Depth/Radius Seed46368 Target2 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/941_coordinate_optimizer_variable_depth_radius_seed46368_target2_sources5_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed46368:1.1,-50.0,1.1,0.10,46368,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed46368 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed46368_target2_sources5_txrx60_ringdown050_objectives
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
case: source_mismatch_ringdown050_noise10_seed46368
target: 2
sources: 5
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 5.164762e-04
offset from cutoff: +1.647617e-05
relative radius margin: 3.001390e-02
confidence label: moderate
fallback warning: none
best misfit: 0.017207898644624273
next radius misfit: 0.017724374811082903
listed competing geometry: x=350 mm, z=121 mm, r=8.75 mm
elapsed: about 395.7 s
```

Diagnostic objective rows all preserve the true target2 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 5.164762e-04 | above cutoff |
| highband | 6.104064e-04 | above cutoff |
| late | 7.616623e-04 | above cutoff |
| late_high | 7.374686e-04 | above cutoff |
| veryhigh | 6.350233e-04 | above cutoff |
| early_high | 4.680172e-04 | below cutoff |

## Interpretation

Run 941 is accepted as the seed46368 target2 5-source control, but the branch
is still low-reserve. Base clears cutoff by only 1.648e-05 and early_high is
below cutoff. Continue to target1 at 5 sources.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.251590 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one moderate row above the 5.0e-4 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target2 truth_radius_mm is 8.0 mm
resources: GPU utilization held around 87-88%; RAM stayed about 96 GiB available
```

## Next Decision

Continue the seed46368 branch with target1, sources=5, Tx/Rx=60, and
ringdown050.

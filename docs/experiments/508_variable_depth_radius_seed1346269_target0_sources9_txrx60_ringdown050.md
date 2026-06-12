# Experiment 508: Seed1346269 Target0 Sources=9 Tx/Rx=60 Ringdown050

## Purpose

Run 974 tests whether a 9-source acquisition rescues the weak seed1346269
target0 8-source control.

## 974: Coordinate Optimizer Variable-Depth/Radius Seed1346269 Target0 Sources=9 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/974_coordinate_optimizer_variable_depth_radius_seed1346269_target0_sources9_txrx60_ringdown050_objectives
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
  --target-indices 0 \
  --passes 1 \
  --x-offsets-mm=0 \
  --z-offsets-mm=0:1:1 \
  --radius-offsets-mm=0:1.25:0.25 \
  --replication-cases source_mismatch_ringdown050_noise10_seed1346269:1.1,-50.0,1.1,0.10,1346269,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed1346269 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed1346269_target0_sources9_txrx60_ringdown050_objectives
```

## Results

The final recovered coordinate state is exact, but the confidence margin
remains weak:

```text
x = [150, 250, 350] mm
z = [80, 100, 120] mm
r = [5, 6, 8] mm
```

Base confidence row:

```text
case: source_mismatch_ringdown050_noise10_seed1346269
target: 0
sources: 9
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 4.727708e-04
offset from cutoff: -2.722292e-05
relative radius margin: 2.968348e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 0.015927067520334768
next radius misfit: 0.016399838327837927
listed competing geometry: x=150 mm, z=81 mm, r=6.0 mm
elapsed: about 718.2 s
```

Diagnostic objective rows all preserve the true target0 geometry, but base,
late, and late_high are below cutoff:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 4.727708e-04 | below cutoff |
| highband | 6.909840e-04 | above cutoff |
| late | 3.266419e-04 | below cutoff |
| late_high | 4.208142e-04 | below cutoff |
| veryhigh | 7.316710e-04 | above cutoff |
| early_high | 6.060438e-04 | above cutoff |

## Interpretation

Run 974 worsens the base margin relative to the 8-source row while preserving
the true geometry. Because seed1346269 target0 started within 8.41e-07 of the
cutoff at 8 sources, run one 11-source escalation before marking target0
unresolved.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.227071 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one weak row below the 5.0e-4 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target0 truth_radius_mm is 5.0 mm
resources: 9-source GPU checks were about 91% utilization with about 96 GiB RAM available
```

## Next Decision

Run the seed1346269 target0 11-source escalation. That run is underway as
experiment 975.

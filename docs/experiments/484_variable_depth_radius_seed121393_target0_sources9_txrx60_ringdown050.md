# Experiment 484: Seed121393 Target0 Sources=9 Tx/Rx=60 Ringdown050 Rescue

## Purpose

Run 950 tests the seed121393 target0 9-source rescue after run 949 recovered
the true target0 geometry at 8 sources but failed the base confidence cutoff.

## 950: Coordinate Optimizer Variable-Depth/Radius Seed121393 Target0 Sources=9 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/950_coordinate_optimizer_variable_depth_radius_seed121393_target0_sources9_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed121393:1.1,-50.0,1.1,0.10,121393,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed121393 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed121393_target0_sources9_txrx60_ringdown050_objectives
```

## Results

The final recovered coordinate state is exact, but base confidence remains
below cutoff:

```text
x = [150, 250, 350] mm
z = [80, 100, 120] mm
r = [5, 6, 8] mm
```

Base confidence row:

```text
case: source_mismatch_ringdown050_noise10_seed121393
target: 0
sources: 9
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 4.911751e-04
offset from cutoff: -8.824876e-06
relative radius margin: 3.166350e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 0.015512343520900886
next radius misfit: 0.016003518644606318
listed competing geometry: x=150 mm, z=81 mm, r=6.0 mm
elapsed: about 716.5 s
```

Diagnostic objective rows all preserve the true target0 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 4.911751e-04 | below cutoff |
| highband | 7.133895e-04 | above cutoff |
| late | 3.475432e-04 | below cutoff |
| late_high | 4.343539e-04 | below cutoff |
| veryhigh | 7.384943e-04 | above cutoff |
| early_high | 6.218149e-04 | above cutoff |

## Interpretation

Run 950 is exact but still weak. It improves the target0 base margin from
4.651e-04 at 8 sources to 4.912e-04 at 9 sources, but remains 8.825e-06 below
cutoff. Since the failure is confidence-only and close to the threshold, run
one 11-source escalation before deciding whether seed121393 target0 is
unresolved.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target0 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.238059 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one weak row below the 5.0e-4 cutoff
figure notes: figures/FIGURE_NOTES.md present and flags target0 as weak
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target0 truth_radius_mm is 5.0 mm
resources: GPU utilization held around 91-92%; RAM stayed about 96 GiB available
```

## Next Decision

Run the seed121393 target0 11-source rescue. That run is underway as
experiment 951.

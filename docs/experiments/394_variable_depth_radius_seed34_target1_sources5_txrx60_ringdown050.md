# Experiment 394: Seed34 Target-1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run 860 continues seed34 ringdown050 transfer after target 0 passed in run
859. It tests the 5-source target-1 policy that already passed for seeds 13,
89, and 21.

## 860: Coordinate Optimizer Variable-Depth/Radius Seed34 Target-1 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/860_coordinate_optimizer_variable_depth_radius_seed34_target1_sources5_txrx60_ringdown050_objectives
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
  --target-indices 1 \
  --passes 1 \
  --x-offsets-mm=0 \
  --z-offsets-mm=0:1:1 \
  --radius-offsets-mm=0:1.25:0.25 \
  --replication-cases source_mismatch_ringdown050_noise10_seed34:1.1,-50.0,1.1,0.10,34,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed34 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed34_target1_sources5_txrx60_ringdown050_objectives
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
case: source_mismatch_ringdown050_noise10_seed34
target: 1
sources: 5
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 5.326011e-04
relative radius margin: 3.132986e-02
confidence label: moderate
fallback warning: none
best misfit: 0.016999792690426792
next radius misfit: 0.017532393797170198
listed competing geometry: x=250 mm, z=101 mm, r=6.75 mm
elapsed: 384.82 s
```

Diagnostic objective rows all preserved the true target-1 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 5.326011e-04 | above cutoff |
| highband | 6.891176e-04 | above cutoff |
| late | 8.001559e-04 | above cutoff |
| late_high | 8.929538e-04 | above cutoff |
| veryhigh | 6.495520e-04 | above cutoff |
| early_high | 4.938739e-04 | below cutoff, truth-preserving |

## Interpretation

Run 860 passes target 1 at ringdown050 for seed34, so target 1 now has four
accepted 5-source rows:

| Run | Noise seed | Margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | --- |
| 834 | 13 | 5.293926e-04 | +2.939e-05 | accepted |
| 835 | 89 | 5.590847e-04 | +5.908e-05 | accepted |
| 836 | 21 | 5.799191e-04 | +7.992e-05 | accepted |
| 860 | 34 | 5.326011e-04 | +3.260e-05 | accepted |

The target-1 evidence is now consistent across all tested seeds. Seed34's
remaining policy question is target 2 source count.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.269434 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row above the 0.0005 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_mm is target-specific at 6.0 mm
resources: GPU utilization held around 87-88%; RAM stayed about 97-98 GiB available
elapsed: 384.82 s
```

## Next Decision

Run seed34 target 2 at ringdown050 with 5 sources and Tx/Rx=60. Promote
seed34 as `8/5/5` if target 2 passes; otherwise test a 9-source target-2
rescue.

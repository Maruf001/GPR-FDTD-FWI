# Experiment 396: Seed34 Target-2 Sources=9 Tx/Rx=60 Ringdown050

## Purpose

Run 862 tests the 9-source seed34 target-2 rescue after the 5-source target-2
row from run 861 was exact but weak.

## 862: Coordinate Optimizer Variable-Depth/Radius Seed34 Target-2 Sources=9 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/862_coordinate_optimizer_variable_depth_radius_seed34_target2_sources9_txrx60_ringdown050_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed34_target2_sources9_txrx60_ringdown050_objectives
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
target: 2
sources: 9
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 5.256874e-04
relative radius margin: 3.339203e-02
confidence label: moderate
fallback warning: none
best misfit: 0.0157429012643193
next radius misfit: 0.016268588702272546
listed competing geometry: x=350 mm, z=121 mm, r=8.75 mm
elapsed: 694.55 s
```

Diagnostic objective rows all preserved the true target-2 geometry and cleared
the cutoff:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 5.256874e-04 | above cutoff |
| highband | 7.044050e-04 | above cutoff |
| late | 8.137731e-04 | above cutoff |
| late_high | 9.359431e-04 | above cutoff |
| veryhigh | 7.291948e-04 | above cutoff |
| early_high | 5.224689e-04 | above cutoff |

## Interpretation

Run 862 is a successful target-2 acquisition rescue. It improves the rejected
5-source row from run 861 by `6.817e-05` and clears the production cutoff by
`2.569e-05`.

Seed34 ringdown050 policy rows:

| Target | Run | Sources | Margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | ---: | --- |
| 0 | 859 | 8 | 5.310935e-04 | +3.109e-05 | accepted |
| 1 | 860 | 5 | 5.326011e-04 | +3.260e-05 | accepted |
| 2 | 862 | 9 | 5.256874e-04 | +2.569e-05 | accepted |

The rejected control is run 861: target 2 with 5 sources, margin
`4.575126e-04`, weak.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.265839 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row above the 0.0005 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_mm is target-specific at 8.0 mm
resources: GPU utilization held around 91%; RAM stayed about 97-98 GiB available
elapsed: 694.55 s
```

## Next Decision

Create the seed34 ringdown050 target-specific `8/5/9` policy summary using
runs 859, 860, 862, and rejected control run 861.

# Experiment 433: Seed610 Target-1 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Run 899 tests the 8-source target1 aperture after seed610 target1 failed at
both 5 sources in run 897 and 9 sources in run 898.

## 899: Coordinate Optimizer Variable-Depth/Radius Seed610 Target-1 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/899_coordinate_optimizer_variable_depth_radius_seed610_target1_sources8_txrx60_ringdown050_objectives
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
  --target-indices 1 \
  --passes 1 \
  --x-offsets-mm=0 \
  --z-offsets-mm=0:1:1 \
  --radius-offsets-mm=0:1.25:0.25 \
  --replication-cases source_mismatch_ringdown050_noise10_seed610:1.1,-50.0,1.1,0.10,610,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed610 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed610_target1_sources8_txrx60_ringdown050_objectives
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
case: source_mismatch_ringdown050_noise10_seed610
target: 1
sources: 8
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 4.205166e-04
offset from cutoff: -7.948342e-05
relative radius margin: 2.680636e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 0.015687167280586604
next radius misfit: 0.016107683862244072
listed competing geometry: x=250 mm, z=101 mm, r=6.25 mm
elapsed: 623.22 s
```

Diagnostic objective rows all preserve the true target-1 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 4.205166e-04 | below cutoff |
| highband | 5.602220e-04 | above cutoff |
| late | 5.778854e-04 | above cutoff |
| late_high | 6.853107e-04 | above cutoff |
| veryhigh | 4.949910e-04 | below cutoff |
| early_high | 4.237118e-04 | below cutoff |

## Interpretation

Run 899 is a negative 8-source target1 rescue. Seed610 target1 simple aperture
branch:

| Run | Sources | Margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | --- |
| 897 | 5 | 4.677410e-04 | -3.226e-05 | rejected |
| 899 | 8 | 4.205166e-04 | -7.948e-05 | rejected |
| 898 | 9 | 4.197879e-04 | -8.021e-05 | rejected |

The best simple aperture remains the 5-source row, but it is still below
cutoff. Seed610 now has target0 accepted only by a razor margin, target1
unresolved under 5/8/9 sources, and target2 unresolved under source-density and
ringdown-only controls. Create a seed610 unresolved-branch summary before
choosing a specialized follow-up.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target-1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.214446 and full dynamic range
visual inspection: confidence figure is readable and correctly shows one weak row below the 0.0005 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target1 truth_radius_mm is 6.0 mm
resources: GPU utilization held around 90-91%; RAM stayed about 97 GiB available
elapsed: 623.22 s
```

## Next Decision

Create a seed610 unresolved-branch summary, then move GPU replication to the
next Fibonacci seed target0 while preserving seed610 for a specialized
aperture/objective follow-up.

# Experiment 424: Seed610 Target-2 Sources=11 Tx/Rx=60 Ringdown050

## Purpose

Run 890 tests whether a denser 11-source target-2 acquisition can rescue
seed610 after both 5-source run 888 and 9-source run 889 were exact but weak
at full ringdown050.

## 890: Coordinate Optimizer Variable-Depth/Radius Seed610 Target-2 Sources=11 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/890_coordinate_optimizer_variable_depth_radius_seed610_target2_sources11_txrx60_ringdown050_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 11 \
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
  --run-name coordinate_optimizer_variable_depth_radius_seed610_target2_sources11_txrx60_ringdown050_objectives
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
target: 2
sources: 11
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 3.969889e-04
offset from cutoff: -1.030111e-04
relative radius margin: 2.724090e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 0.014574679979295697
next radius misfit: 0.014971668848926839
listed competing geometry: x=350 mm, z=121 mm, r=8.75 mm
elapsed: 929.29 s
```

Diagnostic objective rows all preserve the true target-2 geometry, but only
two of six clear cutoff:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 3.969889e-04 | below cutoff |
| highband | 4.889197e-04 | below cutoff |
| late | 5.627489e-04 | above cutoff |
| late_high | 6.146249e-04 | above cutoff |
| veryhigh | 4.881123e-04 | below cutoff |
| early_high | 3.196800e-04 | below cutoff |

## Interpretation

Run 890 is a negative source-density result. It confirms that seed610 target 2
is not solved by increasing from the usual 9-source rescue to 11 sources; the
base margin actually drops by `8.325e-05` relative to run 889. The exact
geometry remains rank 1 for every objective variant, so this is still a
confidence-separation problem rather than a coordinate-recovery failure.

Seed610 target-2 full-ringdown050 source-count branch:

| Run | Sources | Margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | --- |
| 888 | 5 | 4.635149e-04 | -3.649e-05 | rejected |
| 889 | 9 | 4.802438e-04 | -1.976e-05 | rejected |
| 890 | 11 | 3.969889e-04 | -1.030e-04 | rejected |

The best full-ringdown050 row is therefore still the 9-source run 889, but it
is not production-confident. The next step should follow the seed21
practical-threshold pattern: keep the best source count at 9 and reduce the
ringdown coefficient to the established `0.49453125` threshold point.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target-2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.204543 and full dynamic range
visual inspection: confidence figure is readable and correctly shows one weak row below the 0.0005 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target2 truth_radius_mm is 8.0 mm
resources: GPU utilization held around 91-93%; RAM stayed about 97 GiB available
elapsed: 929.29 s
```

## Next Decision

Run seed610 target 2 with 9 sources at `ringdown049453125`, matching the
existing practical threshold used to close the seed21 branch. If that passes,
bisect upward toward full ringdown050; if it fails, lower the ringdown stress
before re-testing source/aperture variants.

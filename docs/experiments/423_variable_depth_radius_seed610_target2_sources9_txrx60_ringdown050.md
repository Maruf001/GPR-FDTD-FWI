# Experiment 423: Seed610 Target-2 Sources=9 Tx/Rx=60 Ringdown050

## Purpose

Run 889 tests whether the usual 9-source target-2 rescue restores production
confidence for seed610 after run 888 showed an exact but weak 5-source target-2
row at full ringdown050.

## 889: Coordinate Optimizer Variable-Depth/Radius Seed610 Target-2 Sources=9 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/889_coordinate_optimizer_variable_depth_radius_seed610_target2_sources9_txrx60_ringdown050_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed610_target2_sources9_txrx60_ringdown050_objectives
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
sources: 9
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 4.802438e-04
offset from cutoff: -1.975621e-05
relative radius margin: 3.069278e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 0.01564680341262918
next radius misfit: 0.01612704720438468
listed competing geometry: x=350 mm, z=121 mm, r=8.75 mm
elapsed: 714.54 s
```

Diagnostic objective rows all preserve the true target-2 geometry, but base
and early_high remain below cutoff:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 4.802438e-04 | below cutoff |
| highband | 6.158541e-04 | above cutoff |
| late | 6.839814e-04 | above cutoff |
| late_high | 7.804717e-04 | above cutoff |
| veryhigh | 6.585882e-04 | above cutoff |
| early_high | 4.584077e-04 | below cutoff |

## Interpretation

Run 889 does not rescue seed610 target 2. It improves the base margin over
run 888 by only `1.673e-05`, leaving the row `1.976e-05` below the production
cutoff. This is different from seed34 and seed89, where 9 sources cleared the
target-2 branch after exact-but-weak 5-, 7-, and 8-source rows.

The failure mode is still radius separation rather than geometry selection:
the exact target-2 geometry is rank 1 for all six objective variants. That
makes a denser acquisition test justified before reducing ringdown severity or
changing the objective. The next run should test seed610 target 2 with
11 sources at the same Tx/Rx=60 and ringdown050 settings.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target-2 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.241504 and full dynamic range
visual inspection: confidence figure is readable and correctly shows one weak row below the 0.0005 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target2 truth_radius_mm is 8.0 mm
resources: GPU utilization held around 91%; RAM stayed about 97 GiB available
elapsed: 714.54 s
```

## Next Decision

Run seed610 target 2 with 11 sources at full ringdown050. If 11 sources pass,
seed610 should be treated as a higher-density target-2 outlier rather than an
`8/5/9` seed.

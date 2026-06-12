# Experiment 398: Seed21 Target-2 Sources=9 Tx/Rx=60 Ringdown049453125

## Purpose

Run 864 tests whether seed21 target 2 is accepted at the final practical
seed21 target-0 threshold, `ringdown049453125`. This closes the small mismatch
left by run 850, where target 2 was accepted at the slightly lower
`ringdown049375` point.

## 864: Coordinate Optimizer Variable-Depth/Radius Seed21 Target-2 Sources=9 Tx/Rx=60 Ringdown049453125

Output:

```text
outputs/experiments/864_coordinate_optimizer_variable_depth_radius_seed21_target2_sources9_txrx60_ringdown049453125_objectives
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
  --replication-cases source_mismatch_ringdown049453125_noise10_seed21:1.1,-50.0,1.1,0.10,21,0.49453125,180.0,0.8 \
  --update-case-label source_mismatch_ringdown049453125_noise10_seed21 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed21_target2_sources9_txrx60_ringdown049453125_objectives
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
case: source_mismatch_ringdown049453125_noise10_seed21
target: 2
sources: 9
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 5.148618e-04
relative radius margin: 3.288051e-02
confidence label: moderate
fallback warning: none
best misfit: 0.01565857043167444
next radius misfit: 0.016173432229086286
elapsed: 701.40 s
```

Diagnostic objective rows all preserved the true target-2 geometry and cleared
the cutoff:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 5.148618e-04 | above cutoff |
| highband | 6.859693e-04 | above cutoff |
| late | 7.527228e-04 | above cutoff |
| late_high | 9.027814e-04 | above cutoff |
| veryhigh | 7.093682e-04 | above cutoff |
| early_high | 5.083178e-04 | above cutoff |

## Interpretation

Run 864 closes the seed21 practical-policy gap. Target 2 remains accepted at
the final target-0 threshold, with `1.486e-05` reserve above cutoff. The row is
therefore a better policy input than run 850 because it uses the same
`ringdown049453125` condition as seed21 target 0.

Seed21 practical policy after run 864:

| Target | Run | Sources | Ringdown | Margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 0 | 854 | 8 | 0.49453125 | 5.000315e-04 | +3.148e-08 | accepted, razor-edge |
| 1 | 836 | 5 | 0.50000000 | 5.799191e-04 | +7.992e-05 | accepted |
| 2 | 864 | 9 | 0.49453125 | 5.148618e-04 | +1.486e-05 | accepted |

Target 0 remains the limiting seed21 row; target 2 is no longer the condition
mismatch in cross-seed summaries.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.242619 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row above the 0.0005 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target2 truth_radius_mm is 8.0 mm
source validation: all six diagnostic objectives preserve target2 truth geometry and clear cutoff
resources: GPU utilization held around 90-91%; RAM stayed about 97-98 GiB available
elapsed: 701.40 s
```

## Next Decision

Refresh the cross-seed ringdown050 target-specific synthesis with run 864 as
the seed21 target-2 practical-policy row.

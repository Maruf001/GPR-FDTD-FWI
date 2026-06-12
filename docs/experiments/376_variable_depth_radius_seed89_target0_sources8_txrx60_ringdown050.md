# Experiment 376: Seed89 Target-0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Run 842 starts seed89 transfer of the seed13 target-specific ringdown050
`8/5/5` source-count policy. It checks target 0 first because seed13 target 0
had the only remaining sub-cutoff diagnostic row after run 841.

## 842: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/842_coordinate_optimizer_variable_depth_radius_seed89_target0_sources8_txrx60_ringdown050_objectives
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
  --replication-cases source_mismatch_ringdown050_noise10_seed89:1.1,-50.0,1.1,0.10,89,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed89 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target0_sources8_txrx60_ringdown050_objectives
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
case: source_mismatch_ringdown050_noise10_seed89
target: 0
sources: 8
scan x positions: [50, 106, 162, 218, 274, 330, 386, 450] mm
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 5.460353e-04
relative radius margin: 3.487742e-02
confidence label: moderate
fallback warning: none
best misfit: 0.01565583860155479
next radius misfit: 0.016201873870492733
elapsed: 594.28 s
```

Diagnostic objective rows all preserved the true target-0 geometry:

| Objective | Margin | Delta vs run 823 | Status |
| --- | ---: | ---: | --- |
| base | 5.460353e-04 | -1.882e-05 | above cutoff |
| highband | 6.773202e-04 | -1.756e-06 | above cutoff |
| late | 4.599730e-04 | +7.504e-06 | below cutoff, truth-preserving |
| late_high | 4.892218e-04 | +6.135e-06 | below cutoff, truth-preserving |
| veryhigh | 6.394587e-04 | +4.223e-06 | above cutoff |
| early_high | 5.514364e-04 | +1.490e-05 | above cutoff |

## Interpretation

Seed89 target 0 transfers successfully at ringdown050 under the 8-source
target-specific policy. The production row is exact/moderate and sits
`4.604e-05` above cutoff. It is `1.882e-05` weaker than the same seed/target
at ringdown0459375 from run 823 and `1.654e-05` weaker than seed13 target 0
at ringdown050 from run 840.

The diagnostic pattern remains the shallow target-0 pattern: late and
late_high are below cutoff but truth-preserving. Unlike the production base
row, those two late-window diagnostics slightly improve relative to run 823.
This is a pass, but the seed89 all-target summary should keep production
success separate from late-window diagnostic fragility.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.276564 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_mm is target-specific at 5.0 mm
resources: GPU utilization held around 90-91%; Python RSS stayed about 442-459 MiB; RAM stayed about 98-99 GiB available
elapsed: 594.28 s
```

## Next Decision

Run seed89 target 2 at ringdown050 with 5 sources and Tx/Rx=60. Seed89 target
1 already passed in run 835, and target 0 now passes in run 842, so target 2
is the remaining seed89 all-target input.

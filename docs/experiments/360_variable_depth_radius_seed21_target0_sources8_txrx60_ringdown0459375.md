# Experiment 360: Seed21 Target-0 Sources=8 Tx/Rx=60 Ringdown0459375

## Purpose

Run 826 completes the seed21 all-target ringdown0459375 transfer inputs. It
tests target 0 with 8 sources and Tx/Rx=60 after seed21 target 1 passed in run
820 and target 2 passed in run 825.

## 826: Coordinate Optimizer Variable-Depth/Radius Seed21 Target-0 Sources=8 Tx/Rx=60 Ringdown0459375

Output:

```text
outputs/experiments/826_coordinate_optimizer_variable_depth_radius_seed21_target0_sources8_txrx60_ringdown0459375_objectives
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
  --replication-cases source_mismatch_ringdown0459375_noise10_seed21:1.1,-50.0,1.1,0.10,21,0.459375,180.0,0.8 \
  --update-case-label source_mismatch_ringdown0459375_noise10_seed21 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed21_target0_sources8_txrx60_ringdown0459375_objectives
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
case: source_mismatch_ringdown0459375_noise10_seed21
target: 0
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 5.151442e-04
relative radius margin: 3.120399e-02
confidence label: moderate
fallback warning: none
best misfit: 0.01650892038822192
next radius misfit: 0.0170240646203164
listed competing geometry: x=150 mm, z=81 mm, r=6.0 mm
elapsed: 590.23 s
```

Diagnostic objective rows all preserved the true target-0 geometry:

| Objective | Margin | Ratio vs base | Best misfit |
| --- | ---: | ---: | ---: |
| base | 5.151442e-04 | 1.000 | 1.650892e-02 |
| highband | 6.458593e-04 | 1.254 | 2.409933e-04 |
| late | 3.215678e-04 | 0.624 | 2.001360e-02 |
| late_high | 4.034978e-04 | 0.783 | 2.871978e-04 |
| veryhigh | 6.048448e-04 | 1.174 | 2.709338e-04 |
| early_high | 5.377525e-04 | 1.044 | 8.245940e-05 |

## Interpretation

Seed21 target 0 transfers successfully at ringdown0459375, but it becomes the
limiting seed21 production row. The base row is exact/moderate with a
`5.151442e-04` margin, only `1.514e-05` above the cutoff. It retains 0.946x of
the seed21 target-0 ringdown035 baseline from run 802.

At this stress, seed21 target 0 is 0.926x the target-1 margin from run 820 and
0.981x the target-2 margin from run 825. The all-target summary should
therefore report target 0 as the limiting production row and preserve the
late-window diagnostic weakness.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.249 and full 0-255 RGB-converted dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 5.0 mm
resources: GPU utilization held mostly about 90%; Python RSS stayed about 451-458 MiB; RAM stayed about 98 GiB available
elapsed: 590.23 s
```

## Next Decision

Create a seed21 all-target ringdown0459375 transfer summary from runs 826,
820, and 825.

# Experiment 369: Seed89 Target-1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run 835 starts cross-seed transfer for the seed13-derived 5-source
ringdown050 target-1 policy. The controlled question is whether the acquisition
rescue from seed13 run 834 transfers to seed89 under the same source mismatch,
noise level, Tx/Rx offset, and diagnostic objective suite.

## 835: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-1 Sources=5 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/835_coordinate_optimizer_variable_depth_radius_seed89_target1_sources5_txrx60_ringdown050_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target1_sources5_txrx60_ringdown050_objectives
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
target: 1
sources: 5
scan x positions: [50, 146, 250, 346, 450] mm
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 5.590847e-04
relative radius margin: 3.327378e-02
confidence label: moderate
fallback warning: none
best misfit: 0.016802558924518016
next radius misfit: 0.017361643574993226
listed competing geometry: x=250 mm, z=101 mm, r=6.75 mm
elapsed: 382.74 s
```

Diagnostic objective rows all preserved the true target-1 geometry:

| Objective | Margin | Ratio vs base | Best misfit |
| --- | ---: | ---: | ---: |
| base | 5.590847e-04 | 1.000 | 1.680256e-02 |
| highband | 7.581416e-04 | 1.356 | 2.815247e-04 |
| late | 8.336013e-04 | 1.491 | 2.076771e-02 |
| late_high | 9.311823e-04 | 1.665 | 2.810172e-04 |
| veryhigh | 7.259372e-04 | 1.299 | 3.171178e-04 |
| early_high | 5.752076e-04 | 1.029 | 7.966490e-05 |

## Interpretation

Run 835 is a positive cross-seed transfer result. Seed89 target 1 remains
exact/moderate at ringdown050 with a `5.590847e-04` production margin,
`5.908e-05` above cutoff.

It is stronger than seed13 run 834 at the same 5-source ringdown050 policy by
`2.969e-05` and a 1.056x ratio. It is also stronger than seed89's 9-source
ringdown0459375 transfer row from run 819 by `2.764e-05`, despite the higher
ringdown stress. The result therefore supports transfer of the 5-source
policy, not just a seed13-only rescue.

All objective diagnostics are truth-preserving and above cutoff. The
early_high diagnostic is no longer marginal for seed89; it clears cutoff by
`7.521e-05`.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.281175 and full 0-255 RGB-converted dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 6.0 mm
resources: GPU utilization held mostly about 88%; Python RSS stayed about 449-455 MiB; RAM stayed about 98-99 GiB available
elapsed: 382.74 s
```

## Next Decision

Run seed21 target 1 at ringdown050 with the same 5-source Tx/Rx=60 acquisition
and diagnostic objective suite. If seed21 also passes, summarize the
three-seed target-1 transfer for the 5-source ringdown050 policy.

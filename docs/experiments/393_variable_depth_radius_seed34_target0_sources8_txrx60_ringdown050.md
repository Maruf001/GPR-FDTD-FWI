# Experiment 393: Seed34 Target-0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Run 859 adds a fourth noise-seed control for the shallow target-0 ringdown050
row. It tests whether the seed21 target-0 ringdown050 failure is a universal
shallow-target limit or a seed-sensitive lower-tail case.

## 859: Coordinate Optimizer Variable-Depth/Radius Seed34 Target-0 Sources=8 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/859_coordinate_optimizer_variable_depth_radius_seed34_target0_sources8_txrx60_ringdown050_objectives
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
  --run-name coordinate_optimizer_variable_depth_radius_seed34_target0_sources8_txrx60_ringdown050_objectives
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
target: 0
sources: 8
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 5.310935e-04
relative radius margin: 3.362366e-02
confidence label: moderate
fallback warning: none
best misfit: 0.01579523014867922
next radius misfit: 0.01632632367045108
listed competing geometry: x=150 mm, z=81 mm, r=6.0 mm
elapsed: 602.48 s
```

Diagnostic objective rows all preserved the true target-0 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 5.310935e-04 | above cutoff |
| highband | 6.906263e-04 | above cutoff |
| late | 4.222513e-04 | below cutoff, truth-preserving |
| late_high | 5.162291e-04 | above cutoff |
| veryhigh | 6.465923e-04 | above cutoff |
| early_high | 5.606437e-04 | above cutoff |

## Interpretation

Run 859 passes target 0 at ringdown050 for seed34. With the same 8-source
Tx/Rx=60 policy, target-0 ringdown050 now passes for seeds 13, 89, and 34, and
fails only for seed21 as a near-miss.

Target-0 8-source ringdown050 comparison:

| Run | Noise seed | Margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | --- |
| 840 | 13 | 5.625753e-04 | +6.258e-05 | accepted |
| 842 | 89 | 5.460353e-04 | +4.604e-05 | accepted |
| 846 | 21 | 4.975041e-04 | -2.496e-06 | rejected near-miss |
| 859 | 34 | 5.310935e-04 | +3.109e-05 | accepted |

This does not invalidate the seed21 threshold bracket; it constrains its
scope. Seed21 is the limiting observed seed for target 0 at ringdown050, while
seed34 supports continued ringdown050 transfer.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.268555 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row above the 0.0005 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_mm is target-specific at 5.0 mm
resources: GPU utilization held around 91%; RAM stayed about 97-98 GiB available
elapsed: 602.48 s
```

## Next Decision

Continue seed34 target-specific ringdown050 transfer with target 1 at
5 sources and Tx/Rx=60. If target 1 passes, test target 2 at 5 sources before
deciding whether seed34 follows the seed13 `8/5/5` policy or needs the seed89
`8/5/9` target-2 rescue.

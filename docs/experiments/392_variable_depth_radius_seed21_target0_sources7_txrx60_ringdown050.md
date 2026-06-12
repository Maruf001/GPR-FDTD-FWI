# Experiment 392: Seed21 Target-0 Sources=7 Tx/Rx=60 Ringdown050

## Purpose

Run 858 tests whether a 7-source acquisition rescues the seed21 target-0
ringdown050 production row after the 8-source row from run 846 and the
9-source rescue from run 847 both remained exact but weak.

## 858: Coordinate Optimizer Variable-Depth/Radius Seed21 Target-0 Sources=7 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/858_coordinate_optimizer_variable_depth_radius_seed21_target0_sources7_txrx60_ringdown050_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 7 \
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
  --replication-cases source_mismatch_ringdown050_noise10_seed21:1.1,-50.0,1.1,0.10,21,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed21 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed21_target0_sources7_txrx60_ringdown050_objectives
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
case: source_mismatch_ringdown050_noise10_seed21
target: 0
sources: 7
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 4.425949e-04
relative radius margin: 3.033666e-02
confidence label: weak
fallback warning: radius_weak_confidence
best misfit: 0.014589440831799116
next radius misfit: 0.015032035690093485
listed competing geometry: x=150 mm, z=81 mm, r=6.0 mm
elapsed: 519.76 s
```

Diagnostic objective rows all preserved the true target-0 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 4.425949e-04 | below cutoff, weak |
| highband | 5.860630e-04 | above cutoff |
| late | 4.274124e-04 | below cutoff, truth-preserving |
| late_high | 4.497259e-04 | below cutoff, truth-preserving |
| veryhigh | 5.506648e-04 | above cutoff |
| early_high | 5.110495e-04 | above cutoff |

## Interpretation

Run 858 is exact but rejected. It misses the `5e-04` moderate-confidence cutoff
by `5.741e-05`, which is materially weaker than the 8-source ringdown050
near-miss from run 846 and the failed 9-source rescue from run 847.

Source-count comparison at seed21 target 0, Tx/Rx=60, ringdown050:

| Run | Sources | Margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | --- |
| 846 | 8 | 4.975041e-04 | -2.496e-06 | rejected |
| 847 | 9 | 4.718459e-04 | -2.816e-05 | rejected rescue |
| 858 | 7 | 4.425949e-04 | -5.741e-05 | rejected rescue |

This falsifies the simple source-count rescue hypothesis for the ringdown050
seed21 target-0 row. The ringdown-threshold interpretation from run 857
remains the governing decision: accepted behavior returns only when the
nominal ringdown scale is reduced below the bracketed threshold.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.227064 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one weak row below the 0.0005 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_mm is target-specific at 5.0 mm
resources: GPU utilization held around 89-90%; RAM stayed about 97-98 GiB available
elapsed: 519.76 s
```

## Next Decision

Stop seed21 target-0 ringdown050 source-count rescue tests. Continue with a
new non-redundant stress branch or a cross-seed ringdown050 policy synthesis
that treats 7/8/9 source seed21 target-0 ringdown050 rows as rejected controls.

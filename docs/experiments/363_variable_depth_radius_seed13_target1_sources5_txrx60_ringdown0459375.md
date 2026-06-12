# Experiment 363: Seed13 Target-1 Sources=5 Tx/Rx=60 Ringdown0459375

## Purpose

Run 829 tests a 5-source acquisition alternative for the global limiting row
identified in the three-seed summary. The previous seed13 target-1 9-source run
814 passed ringdown0459375 by only `7.215e-07`, so this run tests whether the
earlier viable 5-source target-1 aperture improves the production margin.

## 829: Coordinate Optimizer Variable-Depth/Radius Seed13 Target-1 Sources=5 Tx/Rx=60 Ringdown0459375

Output:

```text
outputs/experiments/829_coordinate_optimizer_variable_depth_radius_seed13_target1_sources5_txrx60_ringdown0459375_objectives
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
  --replication-cases source_mismatch_ringdown0459375_noise10_seed13:1.1,-50.0,1.1,0.10,13,0.459375,180.0,0.8 \
  --update-case-label source_mismatch_ringdown0459375_noise10_seed13 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed13_target1_sources5_txrx60_ringdown0459375_objectives
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
case: source_mismatch_ringdown0459375_noise10_seed13
target: 1
sources: 5
scan x positions: [50, 146, 250, 346, 450] mm
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 5.427631e-04
relative radius margin: 2.999782e-02
confidence label: moderate
fallback warning: none
best misfit: 0.018093420350313992
next radius misfit: 0.018636183430874895
listed competing geometry: x=250 mm, z=101 mm, r=6.75 mm
elapsed: 380.81 s
```

Diagnostic objective rows all preserved the true target-1 geometry:

| Objective | Margin | Ratio vs base | Best misfit |
| --- | ---: | ---: | ---: |
| base | 5.427631e-04 | 1.000 | 1.809342e-02 |
| highband | 6.752249e-04 | 1.244 | 2.630477e-04 |
| late | 7.574304e-04 | 1.396 | 2.126280e-02 |
| late_high | 8.497971e-04 | 1.566 | 2.641300e-04 |
| veryhigh | 6.369793e-04 | 1.174 | 3.321456e-04 |
| early_high | 4.971237e-04 | 0.916 | 8.900704e-05 |

## Interpretation

Run 829 is a positive acquisition-improvement result. The 5-source aperture
raises the seed13 target-1 production margin by `4.204e-05` relative to
9-source run 814 at the same ringdown0459375 stress. The ratio is 1.084x, and
the result is exact/moderate.

The early_high diagnostic remains just below cutoff but truth-preserving. The
next question is whether this 5-source aperture also rescues the 0.4625
ringdown level, where the 9-source row was weak.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.261 and full 0-255 RGB-converted dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 6.0 mm
resources: GPU utilization held mostly about 88%; Python RSS stayed about 449-455 MiB; RAM stayed about 98 GiB available
elapsed: 380.81 s
```

## Next Decision

Run seed13 target 1 with the same 5-source aperture at ringdown04625.

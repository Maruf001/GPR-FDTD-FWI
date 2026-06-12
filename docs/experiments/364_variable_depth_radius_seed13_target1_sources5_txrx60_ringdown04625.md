# Experiment 364: Seed13 Target-1 Sources=5 Tx/Rx=60 Ringdown04625

## Purpose

Run 830 tests whether the 5-source aperture that strengthened seed13 target 1
at ringdown0459375 also rescues ringdown04625. The earlier 9-source run 812 at
the same ringdown04625 stress was exact but weak by `1.093e-07`, so this is a
targeted acquisition-policy check rather than a generic repeat.

## 830: Coordinate Optimizer Variable-Depth/Radius Seed13 Target-1 Sources=5 Tx/Rx=60 Ringdown04625

Output:

```text
outputs/experiments/830_coordinate_optimizer_variable_depth_radius_seed13_target1_sources5_txrx60_ringdown04625_objectives
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
  --replication-cases source_mismatch_ringdown04625_noise10_seed13:1.1,-50.0,1.1,0.10,13,0.4625,180.0,0.8 \
  --update-case-label source_mismatch_ringdown04625_noise10_seed13 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed13_target1_sources5_txrx60_ringdown04625_objectives
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
case: source_mismatch_ringdown04625_noise10_seed13
target: 1
sources: 5
scan x positions: [50, 146, 250, 346, 450] mm
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 5.419127e-04
relative radius margin: 3.005081e-02
confidence label: moderate
fallback warning: none
best misfit: 0.01803321537228655
next radius misfit: 0.018575128063451764
listed competing geometry: x=250 mm, z=101 mm, r=6.75 mm
elapsed: 387.14 s
```

Diagnostic objective rows all preserved the true target-1 geometry:

| Objective | Margin | Ratio vs base | Best misfit |
| --- | ---: | ---: | ---: |
| base | 5.419127e-04 | 1.000 | 1.803322e-02 |
| highband | 6.763538e-04 | 1.248 | 2.629916e-04 |
| late | 7.578480e-04 | 1.398 | 2.119331e-02 |
| late_high | 8.504629e-04 | 1.570 | 2.632995e-04 |
| veryhigh | 6.375483e-04 | 1.177 | 3.314153e-04 |
| early_high | 4.988612e-04 | 0.921 | 8.865628e-05 |

## Interpretation

Run 830 is a positive acquisition-policy result. The 5-source aperture raises
the ringdown04625 seed13 target-1 production margin from the weak 9-source run
812 value of `4.998907e-04` to `5.419127e-04`, an improvement of `4.202e-05`
and a 1.084x ratio. The row is exact/moderate and sits `4.191e-05` above the
production cutoff.

The result is also nearly flat relative to the 5-source ringdown0459375 run
829: margin loss is only `8.504e-07`, or a 0.998x retention ratio. That means
the previous ringdown04625 weak point was not an unavoidable physics limit of
the scene; it was tied to the 9-source acquisition pattern under this
objective/profile setup.

The early_high diagnostic is still just below cutoff at `4.989e-04`, but it
preserves the true geometry. That remains a diagnostic fragility rather than a
coordinate or radius failure.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.266822 and full 0-255 RGB-converted dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 6.0 mm
resources: GPU utilization held mostly about 87-88%; Python RSS stayed about 447-453 MiB; RAM stayed about 98 GiB available
elapsed: 387.14 s
```

## Next Decision

Run seed13 target 1 with the same 5-source aperture at ringdown046875. If it
remains exact/moderate, continue the acquisition-specific upward bracket; if it
falls weak, summarize the 5-source acquisition boundary around
ringdown04625-046875 before cross-seed transfer.

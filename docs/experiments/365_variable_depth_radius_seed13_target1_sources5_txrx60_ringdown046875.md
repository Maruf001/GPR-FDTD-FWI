# Experiment 365: Seed13 Target-1 Sources=5 Tx/Rx=60 Ringdown046875

## Purpose

Run 831 continues the 5-source seed13 target-1 acquisition branch above
ringdown04625. Run 830 showed that the 5-source aperture rescues the weak
9-source ringdown04625 row; this run checks whether the same acquisition still
passes at ringdown046875 before committing to cross-seed transfer.

## 831: Coordinate Optimizer Variable-Depth/Radius Seed13 Target-1 Sources=5 Tx/Rx=60 Ringdown046875

Output:

```text
outputs/experiments/831_coordinate_optimizer_variable_depth_radius_seed13_target1_sources5_txrx60_ringdown046875_objectives
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
  --replication-cases source_mismatch_ringdown046875_noise10_seed13:1.1,-50.0,1.1,0.10,13,0.46875,180.0,0.8 \
  --update-case-label source_mismatch_ringdown046875_noise10_seed13 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed13_target1_sources5_txrx60_ringdown046875_objectives
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
case: source_mismatch_ringdown046875_noise10_seed13
target: 1
sources: 5
scan x positions: [50, 146, 250, 346, 450] mm
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 5.401188e-04
relative radius margin: 3.015436e-02
confidence label: moderate
fallback warning: none
best misfit: 0.017911795300090745
next radius misfit: 0.01845191407672947
listed competing geometry: x=250 mm, z=101 mm, r=6.75 mm
elapsed: 387.74 s
```

Diagnostic objective rows all preserved the true target-1 geometry:

| Objective | Margin | Ratio vs base | Best misfit |
| --- | ---: | ---: | ---: |
| base | 5.401188e-04 | 1.000 | 1.791180e-02 |
| highband | 6.784727e-04 | 1.256 | 2.629008e-04 |
| late | 7.586030e-04 | 1.405 | 2.117895e-02 |
| late_high | 8.516546e-04 | 1.577 | 2.631704e-04 |
| veryhigh | 6.386560e-04 | 1.182 | 3.306913e-04 |
| early_high | 5.022674e-04 | 0.930 | 8.949423e-05 |

## Interpretation

Run 831 is a second positive 5-source acquisition result beyond the old
9-source boundary. It remains exact/moderate at ringdown046875 with a
`5.401188e-04` production margin, which is `4.012e-05` above cutoff.

Relative to run 830 at ringdown04625, the margin loss is only `1.794e-06`
and retention is 0.997x. Relative to weak 9-source run 812 at ringdown04625,
run 831 is still stronger by `4.023e-05` despite the higher ringdown stress.
This makes the acquisition-rescue interpretation stronger: the 5-source
aperture is not just moving one borderline point, it is shifting the target-1
stress boundary upward.

Unlike run 830, all six diagnostic objective margins are above the production
cutoff. The early_high row is still the smallest diagnostic margin, but it is
truth-preserving and now clears the cutoff at `5.023e-04`.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.263261 and full 0-255 RGB-converted dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 6.0 mm
resources: GPU utilization held mostly about 88%; Python RSS stayed about 447-454 MiB; RAM stayed about 98 GiB available
elapsed: 387.74 s
```

## Next Decision

Run seed13 target 1 with the same 5-source aperture at ringdown0475. If that
passes, the 5-source branch should be summarized against the 9-source branch
and then transferred across seeds; if it fails, bracket the 5-source boundary
between ringdown046875 and ringdown0475.

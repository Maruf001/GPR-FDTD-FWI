# Experiment 366: Seed13 Target-1 Sources=5 Tx/Rx=60 Ringdown0475

## Purpose

Run 832 tests the same 5-source seed13 target-1 acquisition policy at
ringdown0475. Runs 829-831 showed exact/moderate behavior from
ringdown0459375 through ringdown046875; this run checks whether the branch can
hold a larger upward stress step before summarizing or transferring it.

## 832: Coordinate Optimizer Variable-Depth/Radius Seed13 Target-1 Sources=5 Tx/Rx=60 Ringdown0475

Output:

```text
outputs/experiments/832_coordinate_optimizer_variable_depth_radius_seed13_target1_sources5_txrx60_ringdown0475_objectives
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
  --replication-cases source_mismatch_ringdown0475_noise10_seed13:1.1,-50.0,1.1,0.10,13,0.475,180.0,0.8 \
  --update-case-label source_mismatch_ringdown0475_noise10_seed13 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed13_target1_sources5_txrx60_ringdown0475_objectives
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
case: source_mismatch_ringdown0475_noise10_seed13
target: 1
sources: 5
scan x positions: [50, 146, 250, 346, 450] mm
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 5.382033e-04
relative radius margin: 3.025460e-02
confidence label: moderate
fallback warning: none
best misfit: 0.017789137582021265
next radius misfit: 0.01832734084146903
listed competing geometry: x=250 mm, z=101 mm, r=6.75 mm
elapsed: 385.03 s
```

Diagnostic objective rows all preserved the true target-1 geometry:

| Objective | Margin | Ratio vs base | Best misfit |
| --- | ---: | ---: | ---: |
| base | 5.382033e-04 | 1.000 | 1.778914e-02 |
| highband | 6.804036e-04 | 1.264 | 2.627512e-04 |
| late | 7.592505e-04 | 1.411 | 2.112253e-02 |
| late_high | 8.526590e-04 | 1.584 | 2.625022e-04 |
| veryhigh | 6.397230e-04 | 1.189 | 3.297643e-04 |
| early_high | 5.055776e-04 | 0.939 | 8.980856e-05 |

## Interpretation

Run 832 continues the positive acquisition branch. At ringdown0475, the
5-source target-1 row remains exact/moderate with a `5.382033e-04` production
margin, which is `3.820e-05` above cutoff. The margin loss from run 831 at
ringdown046875 is only `1.916e-06`, so the upward trend remains gradual.

Relative to weak 9-source run 812 at ringdown04625, run 832 is still stronger
by `3.831e-05` despite using a higher ringdown scale. This reinforces that the
old target-1 boundary is an acquisition-pattern boundary, not just a source
ringdown boundary.

All six diagnostic objective margins are above cutoff and truth-preserving.
The early_high row remains the smallest diagnostic but now clears cutoff by
`5.558e-06`.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.268550 and full 0-255 RGB-converted dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 6.0 mm
resources: GPU utilization held mostly about 87-88%; Python RSS stayed about 447-452 MiB; RAM stayed about 98 GiB available
elapsed: 385.03 s
```

## Next Decision

Create a 5-source target-1 acquisition-boundary summary from runs 829-832 and
compare it against the 9-source ringdown0459375-04625 boundary. Then decide
whether the next GPU run should be cross-seed transfer at ringdown0475 or a
larger upward seed13 stress probe.

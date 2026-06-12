# Experiment 357: Seed89 Target-0 Sources=8 Tx/Rx=60 Ringdown0459375

## Purpose

Run 823 completes the seed89 all-target ringdown0459375 transfer set. It tests
the shallow target 0 with the target-specific 8-source Tx/Rx=60 policy, after
runs 819 and 822 established seed89 target 1 and target 2 at the same stress.

## 823: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-0 Sources=8 Tx/Rx=60 Ringdown0459375

Output:

```text
outputs/experiments/823_coordinate_optimizer_variable_depth_radius_seed89_target0_sources8_txrx60_ringdown0459375_objectives
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
  --replication-cases source_mismatch_ringdown0459375_noise10_seed89:1.1,-50.0,1.1,0.10,89,0.459375,180.0,0.8 \
  --update-case-label source_mismatch_ringdown0459375_noise10_seed89 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target0_sources8_txrx60_ringdown0459375_objectives
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
case: source_mismatch_ringdown0459375_noise10_seed89
target: 0
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 5.648510e-04
relative radius margin: 3.422974e-02
confidence label: moderate
fallback warning: none
best misfit: 0.01650176341666306
next radius misfit: 0.01706661445174128
listed competing geometry: x=150 mm, z=81 mm, r=6.0 mm
elapsed: 600.04 s
```

Diagnostic objective rows all preserved the true target-0 geometry:

| Objective | Margin | Ratio vs base | Best misfit |
| --- | ---: | ---: | ---: |
| base | 5.648510e-04 | 1.000 | 1.650176e-02 |
| highband | 6.790760e-04 | 1.202 | 2.085357e-04 |
| late | 4.524691e-04 | 0.801 | 2.003372e-02 |
| late_high | 4.830870e-04 | 0.855 | 2.204404e-04 |
| veryhigh | 6.352355e-04 | 1.125 | 2.382859e-04 |
| early_high | 5.365321e-04 | 0.950 | 5.930481e-05 |

## Interpretation

Seed89 target 0 transfers successfully at ringdown0459375. The production base
row remains exact/moderate with a `5.648510e-04` margin, which is `6.485e-05`
above the cutoff. Compared with the seed89 target-0 8-source ringdown035
baseline from run 795, this retains 0.949x of the margin.

At ringdown0459375, seed89 target 0 is 1.063x the target-1 margin from run 819
and 0.948x the target-2 margin from run 822. Seed89 therefore passes all three
target-specific rows at this stress, with target 1 still the limiting target.

The late and late_high diagnostic variants drop below the production cutoff
but remain truth-preserving. This should be reported as a diagnostic-window
weakness for shallow target 0, not as a geometry failure.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.271 and full 0-255 RGB-converted dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 5.0 mm
resources: GPU utilization held mostly 90-91%; Python RSS stayed about 441-457 MiB; RAM stayed about 98 GiB available
elapsed: 600.04 s
```

## Next Decision

Create a seed89 all-target ringdown0459375 transfer summary from runs 823,
819, and 822 before moving to seed21 target 0/2 or another stronger-stress
branch.

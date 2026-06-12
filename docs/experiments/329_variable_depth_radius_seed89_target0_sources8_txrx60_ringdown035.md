# Experiment 329: Seed89 Target-0 Sources=8 Tx/Rx=60 Ringdown035

## Purpose

Run 795 transfers target 0's best ringdown025 uniform source count to the
stronger ringdown035 source stress. In the ringdown025 branch, target 0 peaked
at 8 sources and dropped to weak at 9 sources, so this run tests whether the
8-source advantage remains stable when the fitted ringdown component is larger.

## 795: Coordinate Optimizer Variable-Depth/Radius Seed89 Target-0 Sources=8 Tx/Rx=60 Ringdown035

Output:

```text
outputs/experiments/795_coordinate_optimizer_variable_depth_radius_seed89_target0_sources8_txrx60_ringdown035_objectives
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
  --replication-cases source_mismatch_ringdown035_noise10_seed89:1.1,-50.0,1.1,0.10,89,0.35,180.0,0.8 \
  --update-case-label source_mismatch_ringdown035_noise10_seed89 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 4 \
  --run-name coordinate_optimizer_variable_depth_radius_seed89_target0_sources8_txrx60_ringdown035_objectives
```

## Parameters

```text
backend: gpu-cpml
grid step: 1.0 mm
sources: 8
scan x positions: [50, 106, 162, 218, 274, 330, 386, 450] mm
Tx/Rx offset: 60 mm
receiver sampling: nearest
frequency: 1.5 GHz
truth x/z/r: [150,250,350] / [80,100,120] / [5,6,8] mm
initial x/z/r: truth final state
target index: 0
candidate grid: x offset 0, z offsets 0/+1 mm, radius offsets 0 to +1.25 mm in 0.25 mm steps
candidate count: 12
source stress: frequency scale 1.1, time shift -50 ps, amplitude 1.1, noise 10%, seed 89, ringdown 0.35
ringdown delay/frequency: 180 ps / 0.8
source fit: frequency grid 0.9/1.0/1.1, time shifts -50/0/50 ps, fitted ringdown coefficient
```

## Artifacts

```text
README.md
data/coordinate_confidence_report.csv
data/coordinate_objective_diagnostics.csv
data/coordinate_objective_top_candidates.csv
data/coordinate_state_history.csv
data/coordinate_step_01_target_0_candidates.csv
data/multi_rebar_coordinate_optimizer_summary.json
figures/coordinate_confidence_margins.png
figures/FIGURE_NOTES.md
run_manifest.json
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
case: source_mismatch_ringdown035_noise10_seed89
receiver sampling: nearest
target: 0
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 5.954728e-04
relative radius margin: 3.185375e-02
confidence label: moderate
best misfit: 0.018693962248696704
next radius misfit: 0.019289435023366556
competing geometry: x=150 mm, z=81 mm, r=6.0 mm
elapsed: 624.02 s
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 5.0 | 5.25 | 5.954728e-04 | 1.000 |
| highband | 5.0 | 5.25 | 6.512216e-04 | 1.094 |
| late | 5.0 | 5.25 | 4.268304e-04 | 0.717 |
| late_high | 5.0 | 5.25 | 4.552580e-04 | 0.765 |
| veryhigh | 5.0 | 5.25 | 6.179721e-04 | 1.038 |
| early_high | 5.0 | 5.25 | 4.777184e-04 | 0.802 |

Target-0 transfer comparison:

| Condition | Run | Base margin | Ratio | Confidence |
| --- | ---: | ---: | ---: | --- |
| uniform 5 sources, ringdown025 | 756 | 5.193087e-04 | 1.000 | moderate |
| uniform 7 sources, ringdown025 | 784 | 5.677174e-04 | 1.093 vs run 756 | moderate |
| uniform 8 sources, ringdown025 | 789 | 5.899921e-04 | 1.136 vs run 756 | moderate |
| uniform 9 sources, ringdown025 | 788 | 4.631165e-04 | 0.892 vs run 756 | weak |
| uniform 8 sources, ringdown035 | 795 | 5.954728e-04 | 1.147 vs run 756 | moderate |
| ringdown035 8 sources vs ringdown025 8 sources | 795/789 | 5.954728e-04 | 1.009 | moderate |
| ringdown035 8 sources vs ringdown025 9 sources | 795/788 | 5.954728e-04 | 1.286 | moderate |

## Interpretation

Run 795 is a positive target-0 transfer result. The 8-source aperture remains
exact and moderate under ringdown035, and the base margin is 1.009x the
ringdown025 8-source row from run 789. This preserves target 0's source-count
preference: 8 sources is strong, while the ringdown025 uniform 9-source row was
weak.

The highband and veryhigh diagnostics are truth-preserving and slightly improve
the target-0 margin. Late and late_high reduce the margin, matching the
ringdown025 target-0 behavior where late windows were not the best diagnostic
for the shallow target.

The recovered source profile fits the stronger ringdown stress directly:
ringdown scale is 0.3501 and the fitted ringdown coefficient is 0.3846.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGB with nonwhite_fraction=0.298 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly flags the moderate row
figure notes: figures/FIGURE_NOTES.md present
metadata validation: summary truth_radius_mm is target-specific at 5.0 mm
resources: GPU utilization held mostly about 90%; Python RSS stayed about 441-459 MiB; RAM stayed about 99 GiB available
```

## Next Decision

Complete the best-source-count ringdown035 transfer set with target 2 at 9
sources. Target 2 improved smoothly through 7/8/9 sources under ringdown025,
so the 9-source ringdown035 row will show whether that trend also survives the
stronger source stress.

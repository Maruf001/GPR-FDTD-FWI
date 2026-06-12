# Experiment 305: Seed21 Target-2 Tx/Rx=50.3125 Linear-Receiver Diagnostic

## Purpose

Run 772 tests the larger seed21 nonzero linear receiver offset after run 771
showed the lower-bound Tx/Rx=50.0390625 case remained exact/moderate. It is a
direct seed21 comparison to the seed89 run 765 midpoint.

## 772: Coordinate Optimizer Variable-Depth/Radius Seed21 Target-2 Tx/Rx=50.3125 Linear Receiver Ringdown025

Output:

```text
outputs/experiments/772_coordinate_optimizer_variable_depth_radius_seed21_target2_txrx50p3125_linear_receiver_ringdown025_objectives
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --tx-rx-offset-mm 50.3125 \
  --receiver-sampling linear \
  --frequency-ghz 1.5 \
  --true-x-values-mm 150,250,350 \
  --true-z-values-mm 80,100,120 \
  --truth-radius-values-mm 5,6,8 \
  --initial-x-values-mm 150,250,350 \
  --initial-z-values-mm 80,100,120 \
  --initial-radius-values-mm 5,6,8 \
  --target-indices 2 \
  --passes 1 \
  --x-offsets-mm=0 \
  --z-offsets-mm=0:1:1 \
  --radius-offsets-mm=0:1.25:0.25 \
  --replication-cases source_mismatch_ringdown025_noise10_seed21:1.1,-50.0,1.1,0.10,21,0.25,180.0,0.8 \
  --update-case-label source_mismatch_ringdown025_noise10_seed21 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 4 \
  --run-name coordinate_optimizer_variable_depth_radius_seed21_target2_txrx50p3125_linear_receiver_ringdown025_objectives
```

## Parameters

```text
backend: gpu-cpml
grid step: 1.0 mm
sources: 5
Tx/Rx offset: 50.3125 mm
receiver sampling: linear
frequency: 1.5 GHz
truth x/z/r: [150,250,350] / [80,100,120] / [5,6,8] mm
initial x/z/r: truth final state
target index: 2
candidate grid: x offset 0, z offsets 0-1 mm, radius offsets 0-1.25 mm in 0.25 mm steps
candidate count: 12
source stress: frequency scale 1.1, time shift -50 ps, amplitude 1.1, noise 10%, seed 21, ringdown 0.25
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
data/coordinate_step_01_target_2_candidates.csv
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
case: source_mismatch_ringdown025_noise10_seed21
receiver sampling: linear
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 5.779376e-04
relative radius margin: 2.153973e-02
confidence label: moderate
best misfit: 0.0268312386826405
elapsed: 398.74 s
```

Objective diagnostics:

| Objective | Best radius mm | Next radius mm | Margin abs | Ratio to base |
| --- | ---: | ---: | ---: | ---: |
| base | 8.0 | 8.75 | 5.779376e-04 | 1.000 |
| highband | 8.0 | 8.75 | 6.268599e-04 | 1.085 |
| late | 8.0 | 8.75 | 9.101029e-04 | 1.575 |
| late_high | 8.0 | 8.75 | 9.677989e-04 | 1.675 |
| veryhigh | 8.0 | 8.75 | 8.218615e-04 | 1.422 |
| early_high | 8.0 | 8.75 | 3.792174e-04 | 0.656 |

Seed/offset comparison:

| Condition | Base margin | Confidence | Ratio to seed21 Tx/Rx=50 |
| --- | ---: | --- | ---: |
| seed21 nearest Tx/Rx=50 (run 741) | 8.000475e-04 | moderate | 1.000 |
| seed21 linear Tx/Rx=50.0390625 (run 771) | 5.770182e-04 | moderate | 0.721 |
| seed21 linear Tx/Rx=50.3125 (run 772) | 5.779376e-04 | moderate | 0.722 |
| seed89 linear Tx/Rx=50.3125 (run 765) | 4.769427e-04 | weak | 0.596 |

## Interpretation

Run 772 confirms that seed21 does not share the seed89 weak plateau at tested
linear receiver offsets. The margin is essentially unchanged from the
lower-bound run 771 and remains 1.212x stronger than the seed89 run 765 margin
at the same Tx/Rx=50.3125 offset.

The correct branch statement is now narrower and stronger: nonzero linear
receiver perturbation degrades target-2 base confidence, but the weak/moderate
classification depends on seed/case. Seed89 is exact/weak; seed21 is
exact/moderate at both 0.0390625 and 0.3125 cell contributions.

Late_high remains the strongest truth-preserving target-2 diagnostic at 1.675x
base.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903, dynamic range 255, grayscale std 67.7840
visual inspection: confidence figure is readable and correctly flags the moderate row
figure notes: figures/FIGURE_NOTES.md present
resources: GPU utilization held about 87-88%; RAM stayed healthy with about 100 GiB available
```

## Next Decision

Create a compact cross-seed linear receiver comparison summary from runs 741,
765, 769, 771, and 772 before launching another seed. If the comparison still
leaves the classification boundary under-specified, run one additional seed at
linear Tx/Rx=50.3125.

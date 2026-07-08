# Experiment 761: Seed610 Target1 Tx/Rx=52.5 Acquisition Probe

Date: 2026-06-17

## Purpose

Run one specialized target1 acquisition-offset probe for the broad low-margin
seed610 branch. Earlier seed610 target1 runs preserved exact geometry but
stayed weak under simple source-count changes at Tx/Rx=60:

```text
897: 5 sources, Tx/Rx 60 mm
899: 8 sources, Tx/Rx 60 mm
898: 9 sources, Tx/Rx 60 mm
```

This run tests whether the target1 Tx/Rx=52.5 mm policy evidence improves the
margin without launching a source-count sweep.

## Output

```text
outputs/experiments/1224_coordinate_optimizer_variable_depth_radius_seed610_target1_sources5_txrx52p5_ringdown050_objectives
```

## Command

```bash
conda run -n gpr-fdtd-fwi python -u run_multi_rebar_coordinate_optimizer.py \
  --backend gpu-cpml \
  --grid-step-mm 1.0 \
  --sources 5 \
  --tx-rx-offset-mm 52.5 \
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
  --replication-cases source_mismatch_ringdown050_noise10_seed610:1.1,-50.0,1.1,0.10,610,0.5,180.0,0.8 \
  --update-case-label source_mismatch_ringdown050_noise10_seed610 \
  --source-frequency-scales 0.9,1.0,1.1 \
  --fit-ringdown-coefficient \
  --source-ringdown-delay-ps 180.0 \
  --source-ringdown-frequency-scale 0.8 \
  --source-time-shift-ps-values=-50,0,50 \
  --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15|late:1.5,5.5,0.2,none,none,0.0|late_high:1.5,5.5,0.2,1.1,3.4,0.15|veryhigh:1.0,7.0,0.3,1.8,4.2,0.15|early_high:0.8,3.5,0.2,1.1,3.4,0.15' \
  --top-k 12 \
  --progress-every 2 \
  --run-name coordinate_optimizer_variable_depth_radius_seed610_target1_sources5_txrx52p5_ringdown050_objectives
```

## Result

The final recovered state is exact:

```text
x = [150, 250, 350] mm
z = [80, 100, 120] mm
r = [5, 6, 8] mm
```

Base confidence row:

```text
best target1 candidate: x=250 mm, z=100 mm, r=6.0 mm
next radius:            6.25 mm
base radius margin:     4.962451e-4
offset from cutoff:    -3.754916e-6
confidence label:       weak
fallback warning:       radius_weak_confidence
```

Seed610 target1 branch comparison:

| Run | Sources | Tx/Rx mm | Base margin | Offset from cutoff | Label |
| ---: | ---: | ---: | ---: | ---: | --- |
| 897 | 5 | 60.0 | 4.677410e-4 | -3.226e-5 | weak |
| 899 | 8 | 60.0 | 4.205166e-4 | -7.948e-5 | weak |
| 898 | 9 | 60.0 | 4.197879e-4 | -8.021e-5 | weak |
| 1224 | 5 | 52.5 | 4.962451e-4 | -3.755e-6 | weak near-miss |

Diagnostic objective margins for run 1224:

| Objective | Margin | Offset from cutoff | Exact rank-1 geometry |
| --- | ---: | ---: | --- |
| base | 4.962451e-4 | -3.755e-6 | yes |
| highband | 6.628286e-4 | +1.628e-4 | yes |
| late | 7.653059e-4 | +2.653e-4 | yes |
| late_high | 8.427878e-4 | +3.428e-4 | yes |
| veryhigh | 6.084169e-4 | +1.084e-4 | yes |
| early_high | 4.647512e-4 | -3.525e-5 | yes |

## Interpretation

Tx/Rx=52.5 substantially improves seed610 target1 relative to the old Tx/Rx=60
source-count branch, but the base margin still does not clear the strict
`5.0e-4` acceptance rule. The right label is exact geometry with unresolved
strict radius confidence, not accepted.

This run strengthens the target1 acquisition-policy story: Tx/Rx bracketing can
move weak target1 branches toward the cutoff, but it does not always produce a
clean strict acceptance. Further seed610 target1 GPU work should wait for a new
objective-policy hypothesis rather than repeating source-count or Tx/Rx variants.

## Validation

Figures were generated:

```text
coordinate_confidence_margins.png
coordinate_radius_decision_panel.png
coordinate_objective_radius_candidates.png
system_scene_geometry.png
```

Sampled resource checks during the run stayed below the requested local caps:
GPU utilization was 87% on checks during the active compute phase, and host RAM
was about 10.1%.

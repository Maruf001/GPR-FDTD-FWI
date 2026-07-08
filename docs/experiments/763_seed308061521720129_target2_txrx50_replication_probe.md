# Experiment 763: Seed308061521720129 Target2 Tx/Rx=50 Replication Probe

Date: 2026-06-17

## Purpose

Replicate the target2 Tx/Rx=50 acquisition-offset hypothesis from experiment
762 on a second exact-but-weak target2 near-miss branch. Seed
`308061521720129` was selected because its best prior target2 row was the
5-source Tx/Rx=60 control, so a 5-source Tx/Rx=50 probe tests acquisition
offset without adding source-count confounding.

## Output

```text
outputs/experiments/1226_coordinate_optimizer_variable_depth_radius_seed308061521720129_target2_sources5_txrx50_ringdown050_objectives
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
best target2 candidate: x=350 mm, z=120 mm, r=8.0 mm
next radius:            8.75 mm
base radius margin:     4.707138e-4
offset from cutoff:    -2.928621e-5
confidence label:       weak
fallback warning:       radius_weak_confidence
```

Branch comparison:

| Run | Sources | Tx/Rx mm | Base margin | Offset from cutoff | Label |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1184 | 5 | 60.0 | 4.908834e-4 | -9.117e-6 | weak near-miss |
| 1185 | 7 | 60.0 | 4.508691e-4 | -4.913e-5 | weak |
| 1186 | 9 | 60.0 | 4.443570e-4 | -5.564e-5 | weak |
| 1226 | 5 | 50.0 | 4.707138e-4 | -2.929e-5 | weak |

Diagnostic objective margins for run 1226:

| Objective | Margin | Offset from cutoff | Exact rank-1 geometry |
| --- | ---: | ---: | --- |
| base | 4.707138e-4 | -2.929e-5 | yes |
| highband | 5.999052e-4 | +9.991e-5 | yes |
| late | 7.820924e-4 | +2.821e-4 | yes |
| late_high | 8.147867e-4 | +3.148e-4 | yes |
| veryhigh | 6.479578e-4 | +1.480e-4 | yes |
| early_high | 4.112452e-4 | -8.875e-5 | yes |

## Interpretation

The Tx/Rx=50 acquisition-offset hypothesis did not replicate on seed
`308061521720129`. It preserved exact geometry, but the base margin regressed
relative to the seed's 5-source Tx/Rx=60 control.

Together with experiment 762, this means target2 offset bracketing is
branch-sensitive:

```text
seed20365011074: Tx/Rx=50 rescued target2
seed308061521720129: Tx/Rx=50 did not rescue target2
```

Do not promote Tx/Rx=50 to a universal target2 rescue. Use it as a selective
probe for near-miss branches, and report failed replications explicitly.

## Validation

Figures were generated:

```text
coordinate_confidence_margins.png
coordinate_radius_decision_panel.png
coordinate_objective_radius_candidates.png
system_scene_geometry.png
```

Sampled resource checks during the run stayed below the requested local caps:
GPU utilization was 86-87% on active checks, and host RAM was about 10.1-10.2%.

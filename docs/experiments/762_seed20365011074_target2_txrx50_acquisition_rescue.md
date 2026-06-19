# Experiment 762: Seed20365011074 Target2 Tx/Rx=50 Acquisition Rescue

Date: 2026-06-17

## Purpose

Run one bounded target2 acquisition-offset probe for seed `20365011074`. The
existing target2 source-density ladder at Tx/Rx=60 preserved exact geometry but
did not clear the strict base-margin cutoff:

```text
1090: 5 sources,  Tx/Rx 60 mm, weak near-miss
1091: 7 sources,  Tx/Rx 60 mm, weak regression
1092: 9 sources,  Tx/Rx 60 mm, weak near-miss
1093: 11 sources, Tx/Rx 60 mm, weak regression
```

This run tests a lower Tx/Rx=50 mm offset at the safe 5-source control setting
instead of extending source count.

## Output

```text
outputs/experiments/1225_coordinate_optimizer_variable_depth_radius_seed20365011074_target2_sources5_txrx50_ringdown050_objectives
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
base radius margin:     5.181019e-4
offset from cutoff:    +1.810194e-5
confidence label:       moderate
fallback warning:       none
```

Branch comparison:

| Run | Sources | Tx/Rx mm | Base margin | Offset from cutoff | Label |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1090 | 5 | 60.0 | 4.964072e-4 | -3.593e-6 | weak |
| 1091 | 7 | 60.0 | 4.743122e-4 | -2.569e-5 | weak |
| 1092 | 9 | 60.0 | 4.981292e-4 | -1.871e-6 | weak |
| 1093 | 11 | 60.0 | 4.033775e-4 | -9.662e-5 | weak |
| 1225 | 5 | 50.0 | 5.181019e-4 | +1.810e-5 | moderate |

Diagnostic objective margins for run 1225:

| Objective | Margin | Offset from cutoff | Exact rank-1 geometry |
| --- | ---: | ---: | --- |
| base | 5.181019e-4 | +1.810e-5 | yes |
| highband | 7.020086e-4 | +2.020e-4 | yes |
| late | 8.899153e-4 | +3.899e-4 | yes |
| late_high | 9.562918e-4 | +4.563e-4 | yes |
| veryhigh | 7.791240e-4 | +2.791e-4 | yes |
| early_high | 5.202965e-4 | +2.030e-5 | yes |

## Interpretation

Tx/Rx=50 rescues seed20365011074 target2 at the 5-source control setting. This
is stronger than the previous 9-source Tx/Rx=60 near-miss and avoids the
historical 11-source regression.

The result supports a target2 policy update:

```text
For target2 exact-but-weak near-miss branches at Tx/Rx=60, test one 5-source
Tx/Rx=50 acquisition-offset probe before escalating beyond 9 sources.
```

Do not generalize this to all target2 weak rows. The first selective
replication, seed308061521720129 in run 1226, preserved exact geometry but
remained weak at Tx/Rx=50. The current conclusion is branch-sensitive:
Tx/Rx=50 can rescue some target2 near-miss branches, but it is not a universal
target2 remedy.

## Validation

Figures were generated:

```text
coordinate_confidence_margins.png
coordinate_radius_decision_panel.png
coordinate_objective_radius_candidates.png
system_scene_geometry.png
```

Sampled resource checks during the run stayed below the requested local caps:
GPU utilization was 87% on active checks, and host RAM was about 10.1-10.2%.

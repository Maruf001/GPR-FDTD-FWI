# Experiment 771: Seed610 Target1 5-Source Tx/Rx Bracket

Date: 2026-06-17

## Purpose

Close the seed610 target1 5-source acquisition-offset bracket after the
Tx/Rx=52.5 mm near-miss. The hypothesis was that the strict base-margin
optimum might sit near, but not exactly at, 52.5 mm.

This is a bounded local 2D branch:

```text
new runs:  Tx/Rx 50, 55, and 57.5 mm
existing:  Tx/Rx 52.5 and 60 mm
sources:   5
target:    target1
seed:      610
```

No 7/9/11-source jobs were launched because historical target1 source-density
runs sit too close to, or above, the requested 90% GPU-utilization ceiling.

## Outputs

New runs:

```text
outputs/experiments/1234_coordinate_optimizer_variable_depth_radius_seed610_target1_sources5_txrx50_ringdown050_objectives
outputs/experiments/1235_coordinate_optimizer_variable_depth_radius_seed610_target1_sources5_txrx55_ringdown050_objectives
outputs/experiments/1236_coordinate_optimizer_variable_depth_radius_seed610_target1_sources5_txrx57p5_ringdown050_objectives
```

Reference runs:

```text
outputs/experiments/897_coordinate_optimizer_variable_depth_radius_seed610_target1_sources5_txrx60_ringdown050_objectives
outputs/experiments/1224_coordinate_optimizer_variable_depth_radius_seed610_target1_sources5_txrx52p5_ringdown050_objectives
```

## Result

All five tested 5-source offsets recover exact target1 geometry:

```text
x = [150, 250, 350] mm
z = [80, 100, 120] mm
r = [5, 6, 8] mm
```

Base confidence comparison:

| Run | Tx/Rx mm | Base margin | Offset from cutoff | Label |
| ---: | ---: | ---: | ---: | --- |
| 1234 | 50.0 | 4.885136e-4 | -1.149e-5 | weak |
| 1224 | 52.5 | 4.962451e-4 | -3.755e-6 | weak near-miss |
| 1235 | 55.0 | 4.968949e-4 | -3.105e-6 | weak near-miss |
| 1236 | 57.5 | 4.821007e-4 | -1.789e-5 | weak |
| 897 | 60.0 | 4.677410e-4 | -3.226e-5 | weak |

Best tested 5-source offset:

```text
Tx/Rx=55 mm, base margin 4.968949e-4
```

That is still below the strict `5.0e-4` acceptance cutoff.

Diagnostic objective margins:

| Run | Tx/Rx mm | Highband | Late | Late-high | Veryhigh | Early-high |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1234 | 50.0 | 6.561874e-4 | 7.474516e-4 | 8.245509e-4 | 5.973759e-4 | 4.555491e-4 |
| 1235 | 55.0 | 6.572550e-4 | 7.661203e-4 | 8.413366e-4 | 6.101005e-4 | 4.711905e-4 |
| 1236 | 57.5 | 6.304023e-4 | 7.338656e-4 | 8.058219e-4 | 5.880166e-4 | 4.644347e-4 |

All diagnostic objectives preserve exact rank-1 geometry. `late_high` remains
the strongest target1 secondary confirmation objective.

## Interpretation

The seed610 target1 problem is not solved by fine 5-source Tx/Rx bracketing.
The best offset is around 52.5-55 mm, but even the best tested row remains just
below the production/base acceptance cutoff.

Current target1 policy remains:

```text
Report exact geometry separately from strict base confidence.
Keep seed610 target1 as exact-but-unresolved under the base gate.
Use late_high as secondary confirmation evidence, not as the production label.
Do not run more seed610 target1 source-count escalation locally under the
current 90% GPU cap.
```

This branch is useful for the paper because it demonstrates that the ambiguity
is a thin confidence-margin reserve around the true radius branch, not a
point-geometry failure.

## Resources

All sampled utilization checks stayed within the requested caps:

| Run | Tx/Rx mm | Runtime | Sampled GPU utilization | Host RAM |
| ---: | ---: | ---: | ---: | ---: |
| 1234 | 50.0 | 425.1 s | 87% | about 12 GiB used |
| 1235 | 55.0 | 425.8 s | 86-87% | about 12 GiB used |
| 1236 | 57.5 | 425.4 s | 87% | about 12 GiB used |

## Validation

Each run generated the standard coordinate-confidence, radius-decision,
objective-candidate, and scene-geometry figures. Figure checks confirmed
nonblank output with nonzero dynamic range. Nonwhite fractions for the primary
confidence figures were:

```text
1234 Tx/Rx=50:   coordinate_confidence_margins.png nonwhite=0.3417
1235 Tx/Rx=55:   coordinate_confidence_margins.png nonwhite=0.3469
1236 Tx/Rx=57.5: coordinate_confidence_margins.png nonwhite=0.3377
```

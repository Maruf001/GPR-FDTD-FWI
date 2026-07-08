# Experiment 774: Seed552 Target1 Tx/Rx55 Policy Refresh

Date: 2026-06-17

## Purpose

Narrow target1 acquisition probe for seed5527939710754757, followed by a
CPU-only refresh of the target1 objective diagnostic and cross-target objective
policy matrix.

This was run because seed552 remained weak at Tx/Rx 52.5 and 60 mm, while the
seed610 bracket showed its best 5-source base margin near Tx/Rx 55 mm. The
question was whether seed552 had a similar acquisition-offset rescue.

## Outputs

```text
outputs/experiments/1240_coordinate_optimizer_variable_depth_radius_seed5527939710754757_target1_sources5_txrx55_ringdown050_objectives
outputs/experiments/1241_coordinate_objective_diagnostic_target1_after_seed552_txrx55
outputs/experiments/1242_coordinate_objective_policy_matrix_after_seed552_txrx55
```

Run 1240 used the GPU optimizer. Runs 1241 and 1242 were CPU-only reporting
passes over existing summaries.

## Probe Result

Run 1240 recovered the exact target1 geometry:

```text
x = 250 mm
z = 100 mm
radius = 6 mm
```

But the base confidence remained below the strict `5.0e-4` cutoff:

| Objective | Radius margin | Confidence | Geometry |
| --- | ---: | --- | --- |
| `base` | 4.546578e-4 | weak | exact |
| `early_high` | 4.231850e-4 | weak | exact |
| `highband` | 6.062190e-4 | moderate | exact |
| `late` | 6.014795e-4 | moderate | exact |
| `late_high` | 7.640518e-4 | moderate | exact |
| `veryhigh` | 5.451879e-4 | moderate | exact |

This does not rescue the seed552 target1 base-confidence branch. The prior
seed552 Tx/Rx60, 9-source row remains the best base row among the checked
seed552 variants, and it is still weak.

## Refreshed Target1 Diagnostic

The target1 diagnostic now contains 12 rows:

```text
seed610 target1:              runs 897, 898, 899, 1224, 1234, 1235, 1236
seed5527939710754757 target1: runs 1216, 1217, 1218, 1223, 1240
```

Every objective preserves exact rank-1 truth geometry in every row. The
confidence difference is only margin strength:

| Objective | Rows | Truth rows | Rows clearing `5.0e-4` | Weak rows | Mean margin | Mean ratio to base |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `base` | 12 | 12 | 0 | 12 | 4.559946e-4 | 1.0000 |
| `early_high` | 12 | 12 | 1 | 11 | 4.426656e-4 | 0.9725 |
| `highband` | 12 | 12 | 11 | 1 | 6.094486e-4 | 1.3366 |
| `late` | 12 | 12 | 11 | 1 | 6.600775e-4 | 1.4432 |
| `late_high` | 12 | 12 | 12 | 0 | 7.720872e-4 | 1.6893 |
| `veryhigh` | 12 | 12 | 10 | 2 | 5.575240e-4 | 1.2214 |

All objective-specific confidence rows report zero x/z/r ambiguity width.

## Cross-Target Policy

The refreshed matrix keeps the same target-specific recommendations:

| Target | Base accepted fraction | Full-acceptance secondary objectives | Strongest secondary objective | Mean ratio |
| --- | ---: | --- | --- | ---: |
| target0 | 0.2778 | `highband`, `veryhigh` | `highband` | 1.3327 |
| target1 | 0.0000 | `late_high` | `late_high` | 1.6893 |
| target2 | 0.1111 | `highband`, `late`, `late_high` | `late_high` | 1.6499 |

The production policy should not replace the base gate with a diagnostic
objective. The useful paper statement is narrower:

```text
Target1 weak rows are exact-geometry, base-confidence-limited rows. The
late_high diagnostic objective confirms stable truth geometry across the
audited target1 weak branches, but strict base confidence remains unresolved.
```

## Interpretation

The seed552 Tx/Rx55 probe closes the most plausible small gap left by the
seed610 bracket. It supports stopping narrow target1 acquisition-offset probing
for now. More GPU work on this branch is unlikely to change the strict base
policy unless the objective definition, frequency content, or candidate space is
changed deliberately.

For the 2D paper direction, this strengthens the current framing:

```text
Point recovery, branch identifiability, and strict objective-margin confidence
are separable outcomes. The target1 branch is physically identifiable in these
audited runs, but not confidently separated by the conservative base margin.
```

## Validation

Figures were validated as nonblank:

```text
1240 coordinate_confidence_margins.png:          nonwhite=0.2911, dynamic range=238
1240 coordinate_objective_radius_candidates.png: nonwhite=0.0683, dynamic range=238
1240 coordinate_radius_decision_panel.png:       nonwhite=0.1742, dynamic range=238
1240 system_scene_geometry.png:                  nonwhite=0.6355, dynamic range=255
1241 coordinate_objective_diagnostic_ratios.png: nonwhite=0.2672, dynamic range=255
1242 objective_policy_matrix.png:                nonwhite=0.4575, dynamic range=255
```

The 1240 GPU run was monitored during execution and stayed below the requested
GPU and RAM utilization caps.

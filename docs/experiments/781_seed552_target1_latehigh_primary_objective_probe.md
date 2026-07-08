# Experiment 781: Seed552 Target1 Late-High Primary Objective Probe

Date: 2026-06-17

## Purpose

Bounded GPU probe for the remaining target1 policy question: whether the
late/highband diagnostic that repeatedly confirms target1 can also act as a
primary objective on one audited weak-but-exact branch.

This intentionally changes the primary objective definition for this run. It
does not replace the production/base policy. The canonical base objective is
kept as a diagnostic row named `canonical_base`.

## Output

```text
outputs/experiments/1259_coordinate_optimizer_variable_depth_radius_seed5527939710754757_target1_sources5_txrx55_latehigh_primary_objectives
```

## Setup

The run repeats the seed552 target1 Tx/Rx55 branch from experiment 774 with:

```text
target:             target1
seed:               5527939710754757
sources:            5
Tx/Rx offset:       55 mm
source stress:      ringdown050, 10% noise, frequency scale 1.1, -50 ps shift
candidate grid:     27 candidates
primary objective:  late_high window/band, labelled base for optimizer update
diagnostic control: canonical_base = original 1.0-7.0 ns base window
```

The primary objective used:

```text
1.5-5.5 ns, 0.2 ns taper, 1.1-3.4 GHz band, 0.15 GHz taper
```

## Result

Final recovered state is exact:

```text
x = [150, 250, 350] mm
z = [80, 100, 120] mm
r = [5, 6, 8] mm
```

Primary late-high objective confidence:

```text
best target1:      x=250 mm, z=100 mm, r=6.0 mm
next radius:       6.25 mm
margin:            7.640518e-4
confidence:        moderate
ambiguity width:   0 mm
```

Objective diagnostics:

| Objective | Best x/z/r | Next radius | Margin | Label |
| --- | --- | ---: | ---: | --- |
| `base` late-high primary | 250 / 100 / 6.0 | 6.25 | 7.640518e-4 | moderate |
| `canonical_base` | 250 / 100 / 6.0 | 6.25 | 4.546578e-4 | weak |
| `highband` | 250 / 100 / 6.0 | 6.25 | 6.062190e-4 | moderate |
| `late` | 250 / 100 / 6.0 | 6.25 | 6.014795e-4 | moderate |
| `veryhigh` | 250 / 100 / 6.0 | 6.25 | 5.451879e-4 | moderate |
| `early_high` | 250 / 100 / 6.0 | 6.25 | 4.231850e-4 | weak |

The canonical-base diagnostic exactly matches the prior seed552 Tx/Rx55 result
from run 1240, confirming that this run isolates the objective-definition
change rather than a geometry or noise change.

## Interpretation

This probe supports the current paper framing more than it changes the
production policy:

```text
The weak target1 branch is not a point-geometry failure.
The true target1 radius/location is separable under a late/highband objective.
The canonical base objective remains weak and should stay the conservative
production gate unless a broader update-rule study is designed.
```

This is useful evidence for a possible future two-stage rule:

```text
base objective for production acceptance;
late_high as secondary confirmation for exact but base-weak target1 rows.
```

It is not sufficient by itself to globally promote late_high as the update
objective.

## Resources

The run took 956.7 s. Sampled utilization stayed within the requested caps:

```text
GPU: 87%
RAM: about 11-12% used
```

No additional GPU jobs were run in parallel.

## Validation

Figures were validated as nonblank:

```text
coordinate_confidence_margins.png:          nonwhite=0.4501, dynamic range=238
coordinate_objective_radius_candidates.png: nonwhite=0.0681, dynamic range=238
coordinate_radius_decision_panel.png:       nonwhite=0.1744, dynamic range=241
system_scene_geometry.png:                  nonwhite=0.6365, dynamic range=255
```


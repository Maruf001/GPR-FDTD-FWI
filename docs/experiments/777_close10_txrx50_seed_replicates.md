# Experiment 777: Close10 Tx/Rx50 Seed Replicates

Date: 2026-06-17

## Purpose

Follow-up to the close12 Tx/Rx50 result. Close12 was clean replicated across
three seeds, so the next meaningful boundary question was whether the same
4-source, Tx/Rx50, target2 branch remains identifiable at close10.

This is still a narrow resolution-limit probe, not a broad sweep. Runs were
executed one at a time and monitored during execution; GPU utilization stayed
below 90% and RAM stayed far below 80%.

## Outputs

```text
outputs/experiments/1250_coordinate_optimizer_close10_seed34_sources4_txrx50_objectives
outputs/experiments/1251_coordinate_optimizer_close10_seed13_sources4_txrx50_objectives
outputs/experiments/1252_coordinate_optimizer_close10_seed21_sources4_txrx50_objectives
outputs/experiments/1253_coordinate_confidence_close10_sources4_txrx50_seed_replicates
outputs/experiments/1255_coordinate_resolution_policy_synthesis_after_close10_txrx50_physical_caveat
```

Run 1254 was an intermediate policy refresh before adding the non-overlap
caveat. Run 1255 supersedes it.

## Setup

```text
true x values:      190, 250, 260 mm
true z values:      90, 90, 90 mm
truth radii:        5, 6, 8 mm
target index:       2
sources:            4
Tx/Rx offset:       50 mm
noise RMS:          10%
seeds:              34, 13, 21
backend:            gpu-cpml
grid step:          1 mm
candidate count:    105 per run
```

Each run used two cases:

```text
nominal 10% noise
source mismatch with frequency scale 1.1, time shift -50 ps, amplitude scale 1.1, and 10% noise
```

## Seed Results

All three runs recovered the exact target2 geometry:

```text
x = 260 mm
z = 90 mm
radius = 8 mm
```

| Seed | Nominal margin | Source-mismatch margin | Confidence | Ambiguity width |
| ---: | ---: | ---: | --- | --- |
| 34 | 1.631267e-3 | 3.658694e-3 | strong / strong | 0 mm |
| 13 | 1.632360e-3 | 3.766556e-3 | strong / strong | 0 mm |
| 21 | 1.553340e-3 | 3.821435e-3 | strong / strong | 0 mm |

No radius-ambiguity revisit targets were found in any run.

## Aggregate Result

Run 1253:

```text
rows:                    6
truth geometry rows:     6
strong confidence rows:  6
fallback warnings:       0
x ambiguity rows:        0
min radius margin:       1.553340e-3
mean radius margin:      2.677275e-3
max radius margin:       3.821435e-3
```

## Policy Refresh

Run 1254 updates the default close-spacing synthesis to include both close12
and close10 at Tx/Rx50.

| Tx/Rx | Closest clean spacing | Clean spacings |
| ---: | ---: | --- |
| 35 mm | 30 mm | 30, 35, 40, 45, 50 |
| 45 mm | 14 mm | 14, 15, 20, 25, 28 |
| 50 mm | 10 mm | 10, 12 |

The updated policy decision is:

```text
Existing aggregate evidence keeps 35 mm Tx/Rx at close30 as the standard
clean replicated limit, while 45 mm Tx/Rx extends clean replication to close14
in the tested branch, and 50 mm Tx/Rx reaches close10 in the tested branch.
Close50 at Tx/Rx25 is mixed/ambiguous, and close28 at Tx/Rx35 remains
interval-supported. The 50 mm Tx/Rx close10/close12 extension is an
overlapping-cylinder algorithmic stress test for the current 6 mm and 8 mm
radius pair; close14 is the non-overlap tangent case.
```

## Interpretation

The close-spacing boundary moved again: close10 is now clean replicated under
the same 4-source, Tx/Rx50, target2 setup at 10% noise across seeds 34, 13, and
21. The margins are slightly weaker than close12 but still comfortably strong
and the ambiguity interval is zero in every row.

This does not prove that all 10 mm-separated three-rebar geometries are clean,
and it should not be cited as a physically separated rebar-layout limit. With
the current 6 mm and 8 mm target1/target2 radii, close14 is tangent and close12
or close10 overlaps the cylinders. The close10 result is best used as an
algorithmic discriminability stress test. For physical spacing claims, the
paper should emphasize the non-overlap branch at close14 and larger spacings.

## Validation

Code validation:

```text
python -m py_compile run_coordinate_resolution_policy_synthesis.py: passed
tests/test_coordinate_resolution_policy_synthesis.py: 6 passed
git diff --check: passed
full pytest: 379 passed
```

Figures were validated as nonblank:

```text
1250 coordinate_confidence_margins.png:          nonwhite=0.3481, dynamic range=238
1250 coordinate_objective_radius_candidates.png: nonwhite=0.0516, dynamic range=238
1250 coordinate_radius_decision_panel.png:       nonwhite=0.2172, dynamic range=238
1250 system_scene_geometry.png:                  nonwhite=0.7301, dynamic range=255

1251 coordinate_confidence_margins.png:          nonwhite=0.3452, dynamic range=238
1251 coordinate_objective_radius_candidates.png: nonwhite=0.0516, dynamic range=238
1251 coordinate_radius_decision_panel.png:       nonwhite=0.2169, dynamic range=238
1251 system_scene_geometry.png:                  nonwhite=0.7301, dynamic range=255

1252 coordinate_confidence_margins.png:          nonwhite=0.3409, dynamic range=238
1252 coordinate_objective_radius_candidates.png: nonwhite=0.0516, dynamic range=238
1252 coordinate_radius_decision_panel.png:       nonwhite=0.2162, dynamic range=238
1252 system_scene_geometry.png:                  nonwhite=0.7301, dynamic range=255

1253 coordinate_confidence_aggregate.png:        nonwhite=0.2172, dynamic range=255
1253 coordinate_ambiguity_widths.png:            nonwhite=0.0388, dynamic range=255
1255 coordinate_resolution_policy.png:           nonwhite=0.0795, dynamic range=255
```

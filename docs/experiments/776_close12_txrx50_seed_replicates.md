# Experiment 776: Close12 Tx/Rx50 Seed Replicates

Date: 2026-06-17

## Purpose

Narrow follow-up to the close14 resolution/noise policy. The close14 archive
was already clean replicated and had a tight Tx/Rx50 noise boundary, so the
next useful GPU question was whether a smaller spacing below close14 remained
clean under the same local coordinate-optimizer setup.

This experiment tests close12 at Tx/Rx50 with 4 sources, target2 only, and
three noise seeds. Runs were monitored during execution and stayed below the
requested GPU/RAM utilization caps.

## Outputs

```text
outputs/experiments/1244_coordinate_optimizer_close12_seed34_sources4_txrx50_objectives
outputs/experiments/1245_coordinate_optimizer_close12_seed13_sources4_txrx50_objectives
outputs/experiments/1246_coordinate_optimizer_close12_seed21_sources4_txrx50_objectives
outputs/experiments/1247_coordinate_confidence_close12_sources4_txrx50_seed_replicates
outputs/experiments/1249_coordinate_resolution_policy_synthesis_after_close12_txrx50_v2
```

Run 1248 was an intermediate policy refresh before the reducer decision text
was updated to include the 50 mm Tx/Rx branch. Run 1249 supersedes it.

## Setup

```text
true x values:      190, 250, 262 mm
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

## Seed Results

All three runs recovered the exact target2 geometry:

```text
x = 262 mm
z = 90 mm
radius = 8 mm
```

| Seed | Nominal margin | Source-mismatch margin | Confidence | Ambiguity width |
| ---: | ---: | ---: | --- | --- |
| 34 | 1.952565e-3 | 4.183005e-3 | strong / strong | 0 mm |
| 13 | 1.934355e-3 | 4.298173e-3 | strong / strong | 0 mm |
| 21 | 1.866621e-3 | 4.317412e-3 | strong / strong | 0 mm |

No radius-ambiguity revisit targets were found in any run.

## Aggregate Result

Run 1247:

```text
rows:                    6
truth geometry rows:     6
strong confidence rows:  6
fallback warnings:       0
x ambiguity rows:        0
min radius margin:       1.866621e-3
mean radius margin:      3.092022e-3
max radius margin:       4.317412e-3
```

## Policy Refresh

Run 1249 adds the close12 aggregate to the existing close-spacing policy:

| Tx/Rx | Closest clean spacing | Clean spacings |
| ---: | ---: | --- |
| 35 mm | 30 mm | 30, 35, 40, 45, 50 |
| 45 mm | 14 mm | 14, 15, 20, 25, 28 |
| 50 mm | 12 mm | 12 |

The updated policy decision is:

```text
Existing aggregate evidence keeps 35 mm Tx/Rx at close30 as the standard
clean replicated limit, while 45 mm Tx/Rx extends clean replication to close14
in the tested branch, and 50 mm Tx/Rx reaches close12 in the tested branch.
Close50 at Tx/Rx25 is mixed/ambiguous, and close28 at Tx/Rx35 remains
interval-supported.
```

## Interpretation

Close14 is no longer the smallest clean replicated spacing in the archive. The
new result shows that with Tx/Rx50 and the same 4-source target2 branch, close12
is still clean replicated at 10% noise across seeds 34, 13, and 21.

This does not yet establish the failure boundary below close12. The next GPU
step, if the paper needs a tighter resolution-limit edge, should be a single
seed34 close10 Tx/Rx50 probe before committing to more seed replication.

## Validation

Focused synthesis test:

```text
tests/test_coordinate_resolution_policy_synthesis.py: 6 passed
```

Figures were validated as nonblank:

```text
1244 coordinate_confidence_margins.png:          nonwhite=0.3539, dynamic range=238
1244 coordinate_objective_radius_candidates.png: nonwhite=0.0519, dynamic range=238
1244 coordinate_radius_decision_panel.png:       nonwhite=0.2175, dynamic range=241
1244 system_scene_geometry.png:                  nonwhite=0.7678, dynamic range=255

1245 coordinate_confidence_margins.png:          nonwhite=0.3503, dynamic range=238
1245 coordinate_objective_radius_candidates.png: nonwhite=0.0519, dynamic range=238
1245 coordinate_radius_decision_panel.png:       nonwhite=0.2176, dynamic range=241
1245 system_scene_geometry.png:                  nonwhite=0.7678, dynamic range=255

1246 coordinate_confidence_margins.png:          nonwhite=0.3465, dynamic range=238
1246 coordinate_objective_radius_candidates.png: nonwhite=0.0519, dynamic range=238
1246 coordinate_radius_decision_panel.png:       nonwhite=0.2170, dynamic range=241
1246 system_scene_geometry.png:                  nonwhite=0.7678, dynamic range=255

1247 coordinate_confidence_aggregate.png:        nonwhite=0.2269, dynamic range=255
1247 coordinate_ambiguity_widths.png:            nonwhite=0.0432, dynamic range=255
1249 coordinate_resolution_policy.png:           nonwhite=0.0775, dynamic range=255
```

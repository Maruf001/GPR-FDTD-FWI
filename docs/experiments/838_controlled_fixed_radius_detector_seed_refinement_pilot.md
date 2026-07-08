# Experiment 838: Controlled Fixed-Radius Detector-Seed Refinement Pilot

Date: 2026-06-18

## Purpose

Run one bounded 2D synthetic pilot to test whether a stable detector-exported
x/z seed can be locally refined when the controlled synthetic radius prior is
fixed to the true slot radii.

This follows runs `088-090`, which scoped branch-specific x/z neighborhoods and
the controlled `5,6,8` mm radius prior. It is a single-case GPU pilot, not a
broad GPU sweep, not field transfer, and not detector-inferred radius/material
recovery.

## Output

Completed pilot:

```text
outputs/experiments/1340_local2d_controlled_fixed_radius_seed_refine_target2_close14_seed21_source_mismatch_gpu
```

Initial blocked attempt:

```text
outputs/experiments/1339_local2d_controlled_fixed_radius_seed_refine_target2_close14_seed21_nominal_gpu
```

The run `1339` attempt failed before simulation because the nominal detector
seed geometry overlapped under exact `5,6,8` mm radii, so the non-overlap
filter rejected every first-step candidate. The completed run `1340` used the
non-overlapping stable `target2_close14|seed21|source_mismatch` detector seed.

Key artifacts:

```text
data/multi_rebar_coordinate_optimizer_summary.json
data/coordinate_confidence_report.csv
data/coordinate_state_history.csv
data/coordinate_step_01_target_0_candidates.csv
data/coordinate_step_02_target_1_candidates.csv
data/coordinate_step_03_target_2_candidates.csv
figures/coordinate_radius_decision_panel.png
figures/coordinate_confidence_margins.png
figures/system_scene_geometry.png
```

## Setup

```text
branch:                  target2_close14
seed/case:               seed21 source_mismatch
backend:                 gpu-cpml
sources:                 5
Tx/Rx offset:            45 mm
receiver sampling:       nearest
frequency:               1.5 GHz
truth x/z:               [190,250,264] / [90,90,90] mm
fixed radii:             [5,6,8] mm
initial detector seed:   [190,248,263] / [95,86,81] mm
local x/z offsets:       -4,-2,0,2,4 mm
radius offsets:          0 mm
source profile:          1.1 scale, -50 ps shift, amplitude fit
non-overlap filtering:   enabled
elapsed:                 364.8 s
```

## Result

```text
final state:             [190,250,265] / [91,90,85] mm
initial x errors:        [0,-2,-1] mm
initial z errors:        [5,-4,-9] mm
final x errors:          [0,0,1] mm
final z errors:          [1,0,-5] mm
initial L-infinity err:  9 mm
final L-infinity err:    5 mm
accepted candidates:     target0 25/25, target1 18/25, target2 19/25
radius confidence labels missing: 3/3
```

Interpretation: the controlled fixed-radius pilot improves the detector seed
but does not fully recover the true geometry in one pass. The middle rebar
lands exactly at truth, the left rebar remains 1 mm deep, and the right rebar
remains 1 mm laterally high and 5 mm shallow. Because the radius offsets were
fixed at zero, the radius-margin confidence fields are not meaningful; this is
a coordinate-residual pilot.

The failed run `1339` is also informative: some stable detector coordinate
seeds become physically invalid once exact radii are imposed. A fixed-radius
refinement path therefore needs a seed-geometry non-overlap preflight or a
repair step before launching even narrow local optimization.

## Decision

Do not promote controlled fixed-radius refinement to a launch queue yet. The
next useful 2D work is a CPU-side preflight/synthesis over the ten stable
detector seed cases:

```text
1. identify which exact-radius seed geometries overlap,
2. identify which cases are non-overlap runnable without repair,
3. separate source-mismatch/nominal behavior,
4. keep review cases excluded,
5. keep detector-inferred radius/material, field transfer, broad GPU, and FWI blocked.
```

This pilot supports a narrow follow-up design, not a publication claim that
detector seeds refine cleanly.

## Validation

Figure validation:

```text
coordinate_confidence_margins.png: 1804x665,
nonwhite=0.0454, dynamic range=238
coordinate_radius_decision_panel.png: 2127x1583,
nonwhite=0.0950, dynamic range=238
system_scene_geometry.png: 1733x1028,
nonwhite=0.6634, dynamic range=255
```

Resource guardrail observed during the run:

```text
RAM used: about 16 GiB / 119 GiB
GPU utilization: about 87%, below the 90% cap
```

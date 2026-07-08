# Experiment 841: Repaired Exact-Radius Detector Seed Refinement Pilot

Date: 2026-06-18

## Purpose

Validate one repaired exact-radius detector seed with a bounded GPU waveform
pilot. This follows the geometry-only repair design in run `092`, which found
that the overlap-blocked `target2_close14|seed21|nominal` seed could be made
physically admissible by shifting the middle component 2 mm left.

This is a single-case validation step. It is not a broad GPU queue, not a
radius/material inference claim, not field transfer, and not detector-seeded
FWI.

## Output

```text
outputs/experiments/1341_local2d_repaired_exact_radius_seed_refine_target2_close14_seed21_nominal_gpu
```

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
seed/case:               seed21 nominal
backend:                 gpu-cpml
sources:                 5
Tx/Rx offset:            45 mm
receiver sampling:       nearest
frequency:               1.5 GHz
truth x/z:               [190,250,264] / [90,90,90] mm
fixed radii:             [5,6,8] mm
original detector seed:  [191,254,266] / [86,91,91] mm
repaired seed:           [191,252,266] / [86,91,91] mm
local x/z offsets:       -4,-2,0,2,4 mm
radius offsets:          0 mm
source profile:          nominal, noise fraction 0.153613, seed 21
non-overlap filtering:   enabled
elapsed:                 321.6 s
```

## Result

```text
final state:             [191,252,266] / [90,89,91] mm
initial x errors:        [1,2,2] mm
initial z errors:        [-4,1,1] mm
final x errors:          [1,2,2] mm
final z errors:          [0,-1,1] mm
initial L-infinity err:  4 mm
final L-infinity err:    2 mm
accepted candidates:     target0 25/25, target1 15/25, target2 15/25
radius confidence labels missing: 3/3
```

Interpretation: the repaired exact-radius seed is waveform-runnable and the
one-pass local search improves the maximum x/z error from 4 mm to 2 mm. The
improvement is mostly depth correction: the lateral errors remain 1 mm on the
left bar and 2 mm on the middle/right bars. Because radius offsets were fixed
at zero, radius-margin confidence fields are expectedly missing and should not
be interpreted as radius confidence.

Run `1341` is a useful repaired-seed validation, but it still does not justify
a broad detector-seeded refinement queue or FWI launch. The next meaningful
2D question is whether a second pass or a different update order can remove
the remaining lateral offset without increasing the search budget too much.

## Validation

Focused and full regressions before this pilot:

```text
focused detector/field regression: 54 passed
full project suite:                869 passed
```

Figure validation:

```text
coordinate_confidence_margins.png: 1804x665,
nonwhite=0.0452, dynamic range=238
coordinate_radius_decision_panel.png: 2127x1583,
nonwhite=0.0981, dynamic range=241
system_scene_geometry.png: 1595x1028,
nonwhite=0.7194, dynamic range=255
```

Resource guardrail observed during the run:

```text
RAM used: about 16 GiB / 119 GiB
GPU utilization: 86-87%, below the 90% cap
```

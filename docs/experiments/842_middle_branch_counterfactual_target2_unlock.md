# Experiment 842: Middle-Branch Counterfactual Target2 Unlock

Date: 2026-06-18

## Purpose

Test whether the residual right-bar lateral error in run `1341` is caused by a
greedy middle-branch lock. Run `1341` selected the middle bar at `x=252,z=89`,
while the saved candidate surface had a near-tie at `x=250,z=89`. Under exact
`5,6,8` mm radii, the selected `x=252` middle branch blocks the right bar from
moving to the true lateral position without overlap.

This run uses the near-tie middle branch as a counterfactual diagnostic and
updates only target 2. It is not a deployable detector policy, not broad GPU
work, and not FWI.

## Output

```text
outputs/experiments/1342_local2d_counterfactual_middle_neartie_target2_unlock_close14_seed21_nominal_gpu
```

Key artifacts:

```text
data/multi_rebar_coordinate_optimizer_summary.json
data/coordinate_confidence_report.csv
data/coordinate_state_history.csv
data/coordinate_step_01_target_2_candidates.csv
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
counterfactual seed:     [191,250,266] / [90,89,91] mm
updated target:          target2 only
local x/z offsets:       -4,-2,0,2,4 mm
radius offsets:          0 mm
source profile:          nominal, noise fraction 0.153613, seed 21
non-overlap filtering:   enabled
elapsed:                 116.8 s
```

## Result

```text
final state:             [191,250,264] / [90,89,91] mm
initial x errors:        [1,0,2] mm
initial z errors:        [0,-1,1] mm
final x errors:          [1,0,0] mm
final z errors:          [0,-1,1] mm
initial L-infinity err:  2 mm
final L-infinity err:    1 mm
accepted candidates:     target2 20/25
best target2 candidate:  x=264 mm, z=91 mm
next geometry:           x=266 mm, z=91 mm
best/next misfit:        0.069865725 / 0.072306181
```

Interpretation: the counterfactual confirms that the right-bar waveform support
exists once the middle bar is placed on the near-tie `x=250` branch. The
remaining run `1341` failure is therefore best interpreted as a greedy
branch-lock / coupled-assignment problem, not as absence of a target2
waveform signal at the true lateral position.

This is useful for paper framing: the controlled synthetic result now has a
specific ambiguity mechanism. The next 2D design should target coupled
middle-right branch selection or a small beam-search/branch-preservation rule,
not simply repeat a greedy coordinate pass.

## Validation

Figure validation:

```text
coordinate_confidence_margins.png: 1804x665,
nonwhite=0.0361, dynamic range=238
coordinate_radius_decision_panel.png: 2127x1583,
nonwhite=0.0875, dynamic range=241
system_scene_geometry.png: 1625x1028,
nonwhite=0.7065, dynamic range=255
```

Resource guardrail observed during the run:

```text
RAM used: about 16 GiB / 119 GiB
GPU utilization: 87%, below the 90% cap
```

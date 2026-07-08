# Experiment 1659: 84-Grid Pilot Transition-Bin Mapper Candidate Design

Date: 2026-06-30

## Purpose

Design the missing transition-bin mapping layer identified by run `1658`.

Run `1658` showed that the five-row pilot cannot be sent directly to the CPU
FDTD solver because each `transition_bin` still needs to become concrete model
inputs. This run maps the 18-bin pilot axis to a candidate Tx/Rx-offset axis
using the saved fine-transition and crossing audits.

This run does not execute FDTD, accept pilot evidence, define the unresolved
`retained_blend` objective, launch GPU work, transfer to field evidence, or
promote 3D/HPC readiness.

## Output

```text
outputs/experiments/1659_local_2d_state_consistent_objective_revision_84grid_pilot_transition_bin_mapper_candidate_design
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_transition_bin_mapper_candidate_design_all_bin_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_transition_bin_mapper_candidate_design_pilot_mapper_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_transition_bin_mapper_candidate_design_representative_margin_curve.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_transition_bin_mapper_candidate_design_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_transition_bin_mapper_candidate_design.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source translation-gap audit ready:       true
source fine-margin audit ready:           true
source crossing audit ready:              true
transition bins designed:                 18
pilot rows mapped:                        5
directly sampled pilot offsets:           2
interpolated pilot offsets:               3
pilot rows at/above crossing:             1
pilot rows below crossing:                4
offset axis:                              40.0 to 45.0 mm
offset step:                              0.29411764705882354 mm
zero-margin crossing offset:              44.62073709151374 mm
candidate mapper design ready:            true
accepted execution mapper ready:          false
retained_blend definition available:      false
real executor script available:           false
new FDTD executed:                        false
GPU work ready:                           false
field transfer ready:                     false
3D/HPC ready:                             false
```

The five pilot rows map as follows:

| Pilot order | Objective | Transition bin | Candidate offset (mm) | Direct sample | Margin | Crossing status |
| ---: | --- | ---: | ---: | --- | ---: | --- |
| 1 | highband | 0 | 40.0000 | yes | -0.0010191060 | below |
| 2 | late | 4 | 41.1765 | no | -0.0006028914 | below |
| 3 | late_high | 9 | 42.6471 | no | -0.0006084972 | below |
| 4 | retained_blend | 13 | 43.8235 | no | -0.0004161108 | below |
| 5 | veryhigh | 17 | 45.0000 | yes | 0.0002290503 | at/above |

The representative margin curve remains negative from 40 to 44 mm and crosses
positive by 45 mm. The saved crossing estimate is 44.62073709151374 mm.

## Interpretation

The transition-bin axis now has a concrete candidate design: map bin `0` to a
40 mm Tx/Rx offset, bin `17` to a 45 mm Tx/Rx offset, and linearly interpolate
the bins between those endpoints.

This is a design result, not an execution contract. Three of the five pilot
rows use interpolated offsets. One pilot row still uses `retained_blend`, which
is not yet a concrete objective definition. A separate real pilot executor is
also still missing.

## Decision

Use this run as the candidate transition-bin mapper design. Keep the five-row
FDTD pilot, full 84-row expansion, GPU work, field transfer, and 3D/HPC blocked
until the mapper is validated, `retained_blend` is defined or removed, and the
separate real executor writes accepted pilot outputs.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_transition_bin_mapper_candidate_design.py
5 passed
```

Figure check:

```text
3364x878, dynamic range=255
```

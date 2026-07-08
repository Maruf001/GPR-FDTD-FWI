# Experiment 1450: Objective Revision Boundary Extension Stress

Date: 2026-06-28

## Purpose

Execute a CPU stress extension after the run `1449` coverage-gap audit. This
run tests whether the revised local objective policy still works when the
near/far radius perturbations are pushed harder than the five-case
materialization from runs `1446`-`1448`.

This is still the same local synthetic geometry family. It is not an
independent geometry holdout and it is not field evidence.

It does not launch GPU work, transfer to field evidence, run field FWI, or
start 3D/HPC work.

## Output

```text
outputs/experiments/1450_local_2d_state_consistent_objective_revision_boundary_extension_stress_cpu
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_boundary_extension_objective_rows.csv
data/local_2d_state_consistent_objective_revision_boundary_extension_policy_rows.csv
data/local_2d_state_consistent_objective_revision_boundary_extension_design_rows.csv
data/local_2d_state_consistent_objective_revision_boundary_extension_stress_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_expanded_window_radius_bracket.png
figures/local_2d_state_consistent_objective_revision_boundary_extension_stress.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_BOUNDARY_EXTENSION_STRESS.md
scripts/run_local_2d_state_consistent_objective_revision_boundary_extension_stress_cpu.py
scripts/run_local_2d_state_consistent_expanded_window_radius_bracket_cpu.py
scripts/script_snapshot_manifest.json
```

## Result

```text
stress perturbations:                7
objective selection rows:            42
objectives per case:                 6
veryhigh failure count:              4
non-veryhigh failure count:          10
drop-veryhigh recovered cases:       5 / 7
majority-vote recovered cases:       5 / 7
strict all-objectives recovered:     3 / 7
veryhigh-only recovered:             3 / 7
boundary extension stress ready:     false
promote revised objective now:       false
broad radius promoted:               false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
elapsed seconds:                     359.354
```

Outcome by perturbation:

| Perturbation | Objective outcome | Policy outcome |
| --- | --- | --- |
| correct state | all six objectives select truth | all candidate policies recover truth |
| near radius +1.80 mm | all six objectives select truth | all candidate policies recover truth |
| near radius +1.90 mm | all six objectives select truth | all candidate policies recover truth |
| near radius +2.10 mm | only `veryhigh` fails | drop-`veryhigh` and majority vote recover truth |
| far radius -1.60 mm | only `veryhigh` fails | drop-`veryhigh` and majority vote recover truth |
| far radius -1.80 mm | all six objectives fail, selecting x=187 mm | no candidate policy recovers truth |
| near +1.90 mm plus far -1.60 mm | all six objectives fail, selecting x=187 mm | no candidate policy recovers truth |

## Interpretation

This run narrows the objective-revision result. Drop-`veryhigh` and majority
vote are not general repairs for harder boundary extensions. They still work
when the new failure is isolated to `veryhigh`, but they fail once the wrong
x=187 mm candidate becomes preferred by the lower-frequency and late-window
objectives as well.

The important result is not simply that `veryhigh` can be unstable. The harder
far-radius and combined perturbations show a stronger local ambiguity where all
six objectives agree on the wrong x-position. That blocks any broad-radius or
physical-transfer claim from this branch.

## Decision

Use run `1450` as the current local 2D boundary-extension stress result.
Preserve the earlier revised-policy result only inside its validated narrow
scope. Do not promote broad-radius, physical-transfer, GPU, field-FWI, or
3D/HPC claims from the current 2D objective-revision branch.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_boundary_extension_stress_cpu.py
3 passed
```

Figure validation:

```text
local_2d_state_consistent_expanded_window_radius_bracket.png: 2459x1459, dynamic range=255
local_2d_state_consistent_objective_revision_boundary_extension_stress.png: 3582x999, dynamic range=255
```

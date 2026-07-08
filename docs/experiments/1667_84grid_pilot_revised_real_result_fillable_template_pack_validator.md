# Experiment 1667: 84-Grid Pilot Revised Real-Result Fillable Template-Pack Validator

Date: 2026-06-30

## Purpose

Validate the revised five-row pilot template pack from run `1666`.

This run checks that the package is internally consistent, targets the revised
payload set, keeps measured-result fields empty, and does not promote template
files into FDTD evidence.

This run does not execute FDTD, accept pilot evidence, launch GPU work,
transfer to field evidence, or promote 3D/HPC readiness.

## Output

```text
outputs/experiments/1667_local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_fillable_template_pack_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_fillable_template_pack_validator_checks.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_fillable_template_pack_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_fillable_template_pack_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source template pack ready:             true
checks:                                 6
passed checks:                          6
failed checks:                          0
template files:                         5
template fields:                        50
required payload IDs:                   1;23;46;68;72
contains payload 68:                    true
contains stale payload 86:              false
contains retained_blend:                false
prefilled design fields:                20
blank or null measured fields:          30
real result files:                      0
new FDTD executions:                    0
GPU work ready:                         false
field transfer ready:                   false
3D/HPC ready:                           false
validation ready:                       true
```

Validation checks:

| Check | Result |
| --- | --- |
| Source template pack ready | Pass |
| Template shape | Pass |
| Revised payload identity | Pass |
| Real-result fields blank | Pass |
| Downstream states blocked | Pass |
| Figure and frozen scripts present | Pass |

## Interpretation

The revised five-row pilot intake package is now coherent through the template
layer. It targets payload rows `1;23;46;68;72`, includes payload `68`, excludes
stale payload `86`, excludes `retained_blend`, and preserves empty measured
fields.

This still does not authorize real execution. It only validates the intake
package that future real FDTD results must fill.

## Decision

Use run `1667` as the current validated revised template-pack checkpoint. The
next useful work should either add sensitivity tests around this validator or
move to the next non-FDTD preparation gate before building a real executor.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_fillable_template_pack_validator.py
5 passed
```

Figure check:

```text
2501x847, dynamic range=255
```

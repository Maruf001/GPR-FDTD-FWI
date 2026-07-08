# Experiment 1668: 84-Grid Pilot Revised Real-Result Fillable Template-Pack Validation Sensitivity

Date: 2026-06-30

## Purpose

Sensitivity-test the run `1667` revised template-pack validator.

Runs `1666` and `1667` refreshed and validated the five-row pilot template
pack around payload rows `1;23;46;68;72`. This run checks that the validator
rejects stale payload identity, filled result fields, downstream promotion,
figure damage, and missing frozen-script evidence.

This run does not execute FDTD, accept pilot evidence, launch GPU work,
transfer to field evidence, or promote 3D/HPC readiness.

## Output

```text
outputs/experiments/1668_local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_fillable_template_pack_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_fillable_template_pack_validation_sensitivity_cases.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_fillable_template_pack_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_fillable_template_pack_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:              true
sensitivity cases:                   9
expected pass cases:                 1
expected fail cases:                 8
actual pass cases:                   1
actual fail cases:                   8
unexpected cases:                    0
damaged cases:                       8
execution permitted:                 false
new FDTD executed:                   false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
sensitivity ready:                   true
```

Damaged cases rejected:

| Case | Damage |
| --- | --- |
| summary ready false | summary readiness false |
| missing manifest row | remove one template manifest row |
| stale payload summary | replace payload 68 with stale payload 86 in summary |
| stale template identity | replace payload 68 template identity with retained_blend payload 86 |
| filled solver status | insert a real-looking solver status into a blank template |
| downstream promotion | premature physical-claim promotion |
| figure damage | zero figure dynamic range |
| script snapshot damage | remove frozen script snapshots |

## Interpretation

The revised template-pack validator is sensitive to the failure modes that
matter for this branch. It rejects the stale payload `86` path, rejects
`retained_blend` re-entry, rejects filled template values being treated as
evidence, and rejects downstream promotion without real FDTD results.

## Decision

Use runs `1666`-`1668` as the guarded revised template-pack block. The revised
pilot remains blocked until real FDTD outputs fill the templates and the run
`1665` command checks pass.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_revised_real_result_fillable_template_pack_validation_sensitivity.py
4 passed
```

Figure check:

```text
1709x847, dynamic range=255
```

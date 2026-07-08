# Experiment 1656: 84-Grid Pilot Real-Result Fillable Template Pack Validator

Date: 2026-06-30

## Purpose

Validate the five-row pilot real-result templates from run `1655`.

The validator checks that the template pack is ready, has five JSON files and
50 total fields, keeps runtime/status/hash/result/execution fields blank or
null, promotes no pilot evidence or downstream readiness, and includes a
nonblank figure plus frozen scripts.

This run does not execute FDTD, accept pilot evidence, launch GPU work, or
promote field transfer or 3D/HPC readiness.

## Output

```text
outputs/experiments/1656_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_fillable_template_pack_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_fillable_template_pack_validator_checks.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_fillable_template_pack_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_fillable_template_pack_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source template pack ready:                true
validation checks:                         5
passed checks:                             5
failed checks:                             0
template files:                            5
template fields:                           50
blank or null fields:                      35
real result files:                         0
new FDTD executions:                       0
bounded pilot execution ready:             false
physical claim ready:                      false
GPU work ready:                            false
field transfer ready:                      false
3D/HPC ready:                              false
validation ready:                          true
```

## Interpretation

The five pilot templates are valid preparation files and not FDTD results. They
are ready to be filled only by real pilot execution outputs.

## Decision

Use runs `1655-1656` as the guarded five-row pilot result-template block. Keep
the 84-row screen blocked until the five real pilot results are produced,
checked with run `1654`, and accepted by the identity and field-domain gates.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_fillable_template_pack.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_fillable_template_pack_validator.py
8 passed
```

Figure check:

```text
2106x843, dynamic range=255
```

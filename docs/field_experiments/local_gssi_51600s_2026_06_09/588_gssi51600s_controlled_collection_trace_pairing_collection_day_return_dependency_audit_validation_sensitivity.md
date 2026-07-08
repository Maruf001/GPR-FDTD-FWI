# Field Experiment 588: Controlled Collection Return Dependency Audit Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `587` validator with damaged versions of the run `586`
dependency audit.

The damaged scenarios include count changes, fake preflight passes, fake ready
stages, fake ready actions, trace-pairing promotion, controlled-field-evidence
promotion, field FWI promotion, field 3D/HPC promotion, figure damage, and
script-snapshot damage.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/588_gssi51600s_controlled_collection_trace_pairing_collection_day_return_dependency_audit_validation_sensitivity
```

## Result

```text
scenarios:                         18
expected pass scenarios:           1
expected fail scenarios:           17
observed pass scenarios:           1
observed fail scenarios:           17
unexpected outcomes:               0
damaged scenarios:                 17
damaged scenarios rejected:        17
gpu priority:                      none
```

The exact saved dependency audit passes. All seventeen damaged variants fail.

## Decision

Use this sensitivity run to keep the controlled-collection dependency map
fail-closed.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_dependency_audit_validation_sensitivity.py
3 passed
```

Figure check:

```text
3220x895, dynamic range=255
```

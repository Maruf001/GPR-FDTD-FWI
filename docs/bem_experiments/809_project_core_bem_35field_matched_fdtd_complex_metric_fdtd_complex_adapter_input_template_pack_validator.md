# BEM Experiment 809: Complex FDTD Adapter Input Template Pack Validator

Date: 2026-07-01

## Purpose

Validate the saved run `808` complex FDTD adapter input template packet.

Run `808` created the producer-side template that a real FDTD export must fill.
This validator checks the schema, row count, stage shape, contract hash,
blank-value fields, and blocked evidence state.

## Output

```text
outputs/bem_experiments/809_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_template_pack_validator
```

## Result

```text
validation checks:                         8
passed checks:                             8
failed checks:                             0
adapter input columns:                     12
template rows:                             279
stages:                                    5
identity cells prefilled:                  1116
contract hash cells prefilled:             279
FDTD value blank cells:                    558
FDTD provenance blank cells:               1395
contains real FDTD values:                 false
accepted as real FDTD input:               false
completed stage files ready:               false
real BEM/FDTD comparison ready:            false
3D/HPC ready:                              false
gpu priority:                              none
```

## Interpretation

The saved template packet is stable. It has the expected 279
receiver-frequency rows, exact adapter schema, prefilled identity and contract
hash fields, blank FDTD value/provenance fields, and no promoted comparison
state.

## Decision

Use this validator before handing the template to a real FDTD export path. Keep
the BEM/FDTD comparison blocked until the template is filled with real FDTD
complex values and passes the adapter input checks.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_template_pack_validator.py

3 passed
```

Figure check:

```text
2861x933, dynamic range=255
```

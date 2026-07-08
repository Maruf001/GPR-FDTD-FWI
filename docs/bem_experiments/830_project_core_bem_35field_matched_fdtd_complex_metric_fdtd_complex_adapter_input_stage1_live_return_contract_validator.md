# BEM Experiment 830: Complex FDTD Adapter Input Stage-1 Live Return Contract Validator

Date: 2026-07-01

## Purpose

Validate the saved run `829` stage-1 live complex-field return contract.

The validator checks the one-row contract shape, receiver-frequency identity,
12-column complex adapter schema, absent partial and full external files,
blocked full preflight, blocked acceptance, action sequence, blocked
comparison/downstream states, figure validation, and script snapshots.

## Output

```text
outputs/bem_experiments/830_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_live_return_contract_validator
```

## Result

```text
validation checks:                  9
passed checks:                      9
failed checks:                      0
stage-1 contract rows:              1
required columns:                   12
full required rows:                 279
stage-1 live partial file present:  false
full external input file present:   false
accepted as full external input:    false
real BEM/FDTD comparison ready:     false
3D/HPC ready:                       false
```

## Interpretation

The saved contract is stable. It remains a partial one-row live-return
contract, not a full external input and not comparison evidence.

## Decision

Use this validator before accepting changes to the stage-1 live complex-field
return contract.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_live_return_contract_validator.py
```

Figure check:

```text
2825x929, dynamic range=255
```

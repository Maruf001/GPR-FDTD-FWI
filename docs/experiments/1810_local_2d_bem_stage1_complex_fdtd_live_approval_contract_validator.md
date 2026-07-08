# Experiment 1810: BEM Stage-1 Complex FDTD Live Approval Contract Validator

Date: 2026-07-01

## Purpose

Validate the saved run `1809` BEM-specific 2D live approval contract.

The validator checks the approval JSON contract, the BEM partial-return CSV
contract, absent live files, zero accepted approvals, and blocked FDTD
execution/comparison states.

## Output

```text
outputs/experiments/1810_local_2d_bem_stage1_complex_fdtd_live_approval_contract_validator
```

## Result

```text
validation checks:                 8
passed checks:                     8
failed checks:                     0
contract rows:                     2
approval fields required:          9
partial CSV columns required:     12
expected receiver index:          15
expected frequency:                1.0 GHz
live approval file present:        false
BEM partial file present:          false
accepted live approvals:           0
FDTD producer authorized now:      false
FDTD executed now:                 false
real BEM/FDTD comparison ready:    false
field transfer ready:              false
3D/HPC ready:                      false
```

## Interpretation

The BEM-specific 2D live approval contract validates and remains
non-authorizing.

## Decision

Use this validator before accepting a live approval JSON for the BEM stage-1
FDTD return.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_contract.py
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_contract_validator.py
5 passed
```

Figure check:

```text
3221x895, dynamic range=255
```

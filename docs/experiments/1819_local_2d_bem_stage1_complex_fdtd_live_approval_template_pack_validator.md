# Experiment 1819: BEM Stage-1 Complex FDTD Live Approval Template Pack Validator

Date: 2026-07-01

## Purpose

Validate the saved run `1818` approval template pack from artifacts.

The validator checks source readiness, template shape, draft payload fields,
output-local placement, blocked live approval, blocked FDTD authorization,
blocked BEM/FDTD comparison, figure validation, and script snapshots.

## Output

```text
outputs/experiments/1819_local_2d_bem_stage1_complex_fdtd_live_approval_template_pack_validator
```

## Result

```text
validation checks:                         6
passed checks:                             6
failed checks:                             0
approval templates:                        1
required approval fields:                  9
prefilled target fields:                   5
blank approval-provenance fields:          4
templates under live approval root:        0
live approval file present:             false
accepted live approvals:                   0
FDTD producer authorized now:           false
FDTD executed now:                      false
real BEM/FDTD comparison ready:         false
gpu priority:                           none
```

## Interpretation

The approval template validates as output-local draft material, not live
approval.

## Decision

Keep FDTD authorization blocked until a real live approval JSON is supplied
under the live approval path.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_template_pack_validator.py
10 passed with template/sensitivity block
```

Figure check:

```text
2285x862, dynamic range=255
```

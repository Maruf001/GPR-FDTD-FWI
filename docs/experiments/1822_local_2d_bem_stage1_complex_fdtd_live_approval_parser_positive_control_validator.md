# Experiment 1822: BEM Stage-1 Complex FDTD Live Approval Parser Positive Control Validator

Date: 2026-07-01

## Purpose

Validate the saved run `1821` parser positive-control state.

The validator checks that the positive-control payload has the expected shape,
remains output-local, does not appear in the live approval location, does not
authorize FDTD, and does not promote BEM/FDTD comparison or downstream field/3D
work.

## Output

```text
outputs/experiments/1822_local_2d_bem_stage1_complex_fdtd_live_approval_parser_positive_control_validator
```

## Result

```text
validation checks:                       5
checks passed:                           5
checks failed:                           0
positive-control files:                  1
parser checks:                           5
parser checks passed:                    5
accepted as payload shape:            true
written under live approval root:     false
live approval file present:           false
accepted live approvals:                 0
FDTD executed now:                    false
real BEM/FDTD comparison ready:       false
field transfer ready:                 false
ready for 3D/HPC:                     false
gpu priority:                         none
```

## Interpretation

The positive control is valid for parser-shape testing and invalid as execution
approval. This preserves the boundary between a complete example payload and a
real authorization to run FDTD.

## Decision

Keep FDTD execution blocked until a real live approval JSON is supplied.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_parser_positive_control.py
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_parser_positive_control_validator.py
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_parser_positive_control_validation_sensitivity.py
8 passed
```

Figure check:

```text
1925x838, dynamic range=255
```

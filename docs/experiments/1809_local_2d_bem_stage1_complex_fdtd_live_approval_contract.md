# Experiment 1809: BEM Stage-1 Complex FDTD Live Approval Contract

Date: 2026-07-01

## Purpose

Define the 2D-side live approval contract for generating the first BEM stage-1
complex FDTD return.

This run does not create a live approval JSON, create a BEM partial-return CSV,
execute FDTD, run BEM/FDTD comparison, transfer to field data, or start 3D/HPC
work.

## Output

```text
outputs/experiments/1809_local_2d_bem_stage1_complex_fdtd_live_approval_contract
```

## Result

```text
contract rows:                     2
approval fields required:          9
partial CSV columns required:     12
expected pair id:                  stage01_pair000
expected receiver index:          15
expected frequency:                1.0 GHz
live approval parent present:      false
live approval file present:        false
BEM partial parent present:        true
BEM partial file present:          false
accepted live approvals:           0
FDTD producer authorized now:      false
FDTD executed now:                 false
real BEM/FDTD comparison ready:    false
field transfer ready:              false
3D/HPC ready:                      false
```

The required live approval path is:

```text
outputs/experiments/_external_2d_returns/bem_stage1_complex_fdtd_pending/APPROVED_BEM_STAGE1_COMPLEX_FDTD_RETURN.json
```

The expected BEM partial-return path is:

```text
outputs/bem_experiments/_external_fdtd_returns/project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_partial.csv
```

## Interpretation

The first BEM-specific 2D approval contract is now explicit: one live approval
JSON plus one stage-1 partial complex-field CSV. Neither live file is present.

## Decision

Use this as the live approval contract for the first BEM stage-1 FDTD return.
Keep FDTD execution and BEM/FDTD comparison blocked until the approval exists
and the partial return passes intake.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_contract.py
2 passed
```

Figure check:

```text
2609x883, dynamic range=255
```

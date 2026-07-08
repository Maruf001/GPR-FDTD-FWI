# Experiment 1818: BEM Stage-1 Complex FDTD Live Approval Template Pack

Date: 2026-07-01

## Purpose

Create an output-local approval JSON template for the first BEM stage-1 FDTD
return.

The template pre-fills the immutable target fields for the one-row FDTD return:
pair ID, receiver index, frequency, output CSV path, and required partial-return
CSV columns. It leaves approval provenance blank. It does not write to the live
approval directory, authorize FDTD execution, or promote BEM/FDTD comparison.

## Output

```text
outputs/experiments/1818_local_2d_bem_stage1_complex_fdtd_live_approval_template_pack
```

Key artifact:

```text
data/approval_template/APPROVED_BEM_STAGE1_COMPLEX_FDTD_RETURN.template.json
```

## Result

```text
source contract ready:                  true
source refresh sensitivity ready:       true
approval templates:                        1
approval template file present:          true
required approval fields:                   9
prefilled target fields:                    5
blank approval-provenance fields:           4
review status is draft:                  true
templates under live approval root:         0
live approval file present:              false
accepted live approvals:                    0
FDTD producer authorized now:            false
FDTD executed now:                       false
real BEM/FDTD comparison ready:          false
gpu priority:                            none
```

## Interpretation

The template is useful preparation material. It identifies the exact one-row
FDTD return being requested, but it is still a draft because approval ID,
approval time, reviewer, and approval reason are blank.

The `approved_required_columns` field refers to the required stage-1
partial-return CSV schema, including real and imaginary FDTD values plus solver
provenance fields.

## Decision

Use this template for approval preparation only. Do not treat it as live
approval or FDTD authorization.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_template_pack.py
10 passed with validator/sensitivity block
```

Figure check:

```text
2465x846, dynamic range=255
```

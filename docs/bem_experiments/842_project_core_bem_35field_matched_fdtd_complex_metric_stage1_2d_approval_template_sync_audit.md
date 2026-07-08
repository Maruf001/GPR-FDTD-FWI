# BEM Experiment 842: Stage-1 2D Approval Template Sync Audit

Date: 2026-07-01

## Purpose

Audit whether the BEM stage-1 producer packet matches the 2D approval template
from run `1818`.

This run checks that the template target fields and required partial-return CSV
columns match the BEM producer packet exactly. It does not treat the template as
live approval and does not execute FDTD.

## Output

```text
outputs/bem_experiments/842_project_core_bem_35field_matched_fdtd_complex_metric_stage1_2d_approval_template_sync_audit
```

## Result

```text
source BEM packet ready:              true
source BEM/2D sync sensitivity ready: true
source 2D template ready:             true
source 2D template validation ready:  true
source 2D template sensitivity ready: true
audit checks:                            7
passed audit checks:                     7
failed audit checks:                     0
receiver index:                         15
frequency:                    1000000000 Hz
approval templates:                      1
prefilled target fields:                 5
blank approval fields:                   4
live approval file present:           false
accepted live approvals:                 0
FDTD executed now:                    false
real BEM/FDTD comparison ready:       false
gpu priority:                         none
```

## Interpretation

The BEM producer packet and the 2D approval template are synchronized. The
template approves the correct partial-return CSV schema, including the real and
imaginary FDTD fields and solver provenance fields, but it is still only an
output-local draft template.

## Decision

Keep FDTD execution blocked until the output-local template is replaced by a
real live approval JSON.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_2d_approval_template_sync_audit.py
8 passed with validator/sensitivity block
```

Figure check:

```text
2789x858, dynamic range=255
```

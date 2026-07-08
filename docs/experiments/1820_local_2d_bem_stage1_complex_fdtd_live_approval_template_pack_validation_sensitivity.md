# Experiment 1820: BEM Stage-1 Complex FDTD Live Approval Template Pack Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `1819` validator by damaging the saved run `1818` approval
template pack in controlled ways.

The sensitivity set checks source-readiness damage, row-count damage,
required-field damage, target-prefill damage, approval-provenance promotion,
draft-status promotion, live-root promotion, false live approval, false
acceptance, FDTD authorization/execution promotion, comparison promotion,
field/3D promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/experiments/1820_local_2d_bem_stage1_complex_fdtd_live_approval_template_pack_validation_sensitivity
```

## Result

```text
scenarios:                         19
expected passes:                    1
expected failures:                 18
observed passes:                    1
observed failures:                 18
unexpected outcomes:                0
damaged scenarios:                 18
damaged scenarios rejected:        18
FDTD executed now:                false
real BEM/FDTD comparison ready:   false
gpu priority:                     none
```

The exact output-local draft template state passes. All damaged states fail.

## Interpretation

The validator accepts only the exact draft approval-template state and rejects
false promotion to live approval, FDTD authorization, comparison, field
transfer, or 3D/HPC.

## Decision

Use runs `1818-1820` as the guarded BEM stage-1 approval-template block.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_template_pack.py
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_template_pack_validator.py
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_template_pack_validation_sensitivity.py
10 passed
```

Figure check:

```text
3131x842, dynamic range=255
```

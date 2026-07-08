# BEM Experiment 814: Complex FDTD Adapter Input External Handoff Claim Boundary

Date: 2026-07-01

## Purpose

Record the claim boundary after the guarded complex FDTD external handoff block.

Runs `811-813` proved that the output-local fill-in template is separate from
the expected external return file. This run states exactly what that block
supports and what remains blocked.

## Output

```text
outputs/bem_experiments/814_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_external_handoff_claim_boundary
```

## Result

```text
claims:                            5
guarded claims:                    2
blocked claims:                    3
source guard ready:                true
source validation ready:           true
source sensitivity ready:          true
handoff items:                     2
output-local template present:     true
output-local template rows:        279
external input file present:       false
external input rows:               0
external input accepted:           false
damaged scenarios rejected:        11
unexpected outcomes:               0
completed stage files ready:       false
real BEM/FDTD comparison ready:    false
field transfer ready:              false
3D/HPC ready:                      false
gpu priority:                      none
```

The two guarded claims are:

| Claim | Supporting runs | Status |
| --- | --- | --- |
| complex FDTD input template is guarded | 808-813 | guarded |
| external filled-input handoff is fail-closed | 811-813 | guarded |

The blocked claims are real external FDTD complex input, completed stage files
with FDTD complex values, and real BEM/FDTD comparison or downstream escalation.

## Interpretation

The current BEM branch has a clean handoff boundary. The template is ready for
a real FDTD producer to fill, but no real external FDTD rows have been accepted.
That means this block is a data-contract and guard result, not evidence of
BEM/FDTD agreement.

## Decision

Use this claim boundary before accepting any real complex FDTD return file. Do
not cite this block as BEM/FDTD agreement, field transfer, or 3D/HPC readiness.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_external_handoff_claim_boundary.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_external_handoff_claim_boundary_validator.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_external_handoff_claim_boundary_validation_sensitivity.py

9 passed
```

Figure check:

```text
3725x938, dynamic range=255
```

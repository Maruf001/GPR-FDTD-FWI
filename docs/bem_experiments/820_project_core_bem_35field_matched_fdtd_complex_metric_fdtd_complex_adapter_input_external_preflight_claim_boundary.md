# BEM Experiment 820: Complex FDTD External Input Preflight Claim Boundary

Date: 2026-07-01

## Purpose

Record the claim boundary after the real complex FDTD input preflight gate.

Runs `817-819` define and harden the acceptance gate for a future real external
FDTD input CSV. This run states what that gate proves and what still requires
real returned data.

## Output

```text
outputs/bem_experiments/820_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_external_preflight_claim_boundary
```

## Result

```text
claims:                         5
guarded claims:                 2
blocked claims:                 3
preflight items:                1
expected rows:                  279
external input file present:    false
external input rows:            0
external input accepted:        false
finite FDTD value cells:        0
provenance/status cells:        0
completed stage files ready:    false
real BEM/FDTD comparison ready: false
field transfer ready:           false
3D/HPC ready:                   false
gpu priority:                   none
```

The two guarded claims are the external input preflight gate and the fail-closed
absent-file state. The blocked claims are real external complex FDTD input,
completed stage files with real FDTD values, and real BEM/FDTD comparison or
downstream transfer.

## Interpretation

The branch now has a complete acceptance boundary for the real complex FDTD
input file. The expected file is still absent, so this is an acceptance rule and
not a real comparison result.

## Decision

Use this boundary to prevent preflight mechanics from being cited as real
BEM/FDTD agreement. The next promotion requires a real CSV that passes the run
`817` gate.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_external_preflight_claim_boundary.py

3 passed
```

Figure check:

```text
3581x896, dynamic range=255
```

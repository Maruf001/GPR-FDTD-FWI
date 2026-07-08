# BEM Experiment 262: Half-Space Finite-Rebar Trace-Root Synthetic BEM Pairwise Negative-Control Audit

Date: 2026-06-28

## Purpose

Compare the synthetic trace-root frequency bins against the BEM scattered
spectra as a negative control.

Runs `259-261` proved that the trace-root frequency extraction mechanics are
guarded. This run checks the claim boundary:

```text
Do those self-referenced synthetic bins accidentally look like BEM/FDTD
agreement evidence?
```

They should not. The staged traces are arbitrary synthetic acceptance fixtures,
not real FDTD traces generated from the BEM target case.

It does not run real FDTD, ingest real trace files, claim BEM/FDTD agreement,
launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/262_project_core_bem_halfspace_finite_rebar_trace_root_synthetic_bem_pairwise_negative_control_audit
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_trace_root_synthetic_bem_pairwise_negative_control_rows.csv
data/project_core_bem_halfspace_finite_rebar_trace_root_synthetic_bem_pairwise_negative_control_frequency_summary.csv
data/project_core_bem_halfspace_finite_rebar_trace_root_synthetic_bem_pairwise_negative_control_audit_summary.json
figures/project_core_bem_halfspace_finite_rebar_trace_root_synthetic_bem_pairwise_negative_control_audit.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_TRACE_ROOT_SYNTHETIC_BEM_PAIRWISE_NEGATIVE_CONTROL_AUDIT.md
scripts/run_project_core_bem_halfspace_finite_rebar_trace_root_synthetic_bem_pairwise_negative_control_audit.py
scripts/test_project_core_bem_halfspace_finite_rebar_trace_root_synthetic_bem_pairwise_negative_control_audit.py
```

## Result

```text
BEM scattered keys:                         117
trace-root keys:                            117
paired keys:                                117
frequency rows:                             9
missing BEM keys:                           0
missing trace-root keys:                    0
duplicate BEM keys:                         0
duplicate trace-root keys:                  0
key completeness ready:                     true
max scattered relative error:               1.000208702121816
normalized L2 error:                        1.0000000672667073
trace-root synthetic negative-control ready: true
synthetic BEM/FDTD agreement ready:         false
real trace files present:                   false
real FDTD frequency extraction ready:       false
real BEM/FDTD comparison ready:             false
ready for 3D validation:                    false
inversion-scale half-space ready:           false
field transfer ready:                       false
ready for GPU work:                         false
field FWI ready:                            false
```

## Interpretation

The trace-root synthetic frequency bins have complete receiver-frequency keys,
but they intentionally do not agree with the BEM scattered spectra. The
normalized L2 mismatch is about `1.0`, which is a strong no-go signal for any
agreement claim.

This confirms that the self-reference frequency table is useful for plumbing
only and must not be promoted as BEM/FDTD agreement evidence.

## Decision

Use run `262` as the negative-control boundary for trace-root synthetic bins.
Real trace files, real FDTD frequency extraction, real BEM/FDTD comparison, 3D
validation, inversion, field transfer, GPU/HPC readiness, and field FWI remain
blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_trace_root_synthetic_bem_pairwise_negative_control_audit.py
5 passed
```

Figure validation:

```text
figures/project_core_bem_halfspace_finite_rebar_trace_root_synthetic_bem_pairwise_negative_control_audit.png
2536x845, dynamic range=255
```

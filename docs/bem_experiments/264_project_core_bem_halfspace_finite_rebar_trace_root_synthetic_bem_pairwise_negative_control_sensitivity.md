# BEM Experiment 264: Half-Space Finite-Rebar Trace-Root Synthetic BEM Pairwise Negative-Control Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `263` negative-control validator.

Run `263` validated that the synthetic trace-root frequency bins are a
negative control, not BEM/FDTD agreement evidence. This run checks whether that
validator fails closed when the source readiness flags, pairwise rows, frequency
summaries, mismatch metrics, or downstream readiness states are damaged.

It does not run real FDTD, ingest real trace files, claim BEM/FDTD agreement,
launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/264_project_core_bem_halfspace_finite_rebar_trace_root_synthetic_bem_pairwise_negative_control_sensitivity
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_trace_root_synthetic_bem_pairwise_negative_control_sensitivity_scenarios.csv
data/project_core_bem_halfspace_finite_rebar_trace_root_synthetic_bem_pairwise_negative_control_sensitivity_summary.json
figures/project_core_bem_halfspace_finite_rebar_trace_root_synthetic_bem_pairwise_negative_control_sensitivity.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_TRACE_ROOT_SYNTHETIC_BEM_PAIRWISE_NEGATIVE_CONTROL_SENSITIVITY.md
scripts/run_project_core_bem_halfspace_finite_rebar_trace_root_synthetic_bem_pairwise_negative_control_sensitivity.py
scripts/test_project_core_bem_halfspace_finite_rebar_trace_root_synthetic_bem_pairwise_negative_control_sensitivity.py
```

## Result

```text
scenarios:                         29
expected pass scenarios:           1
expected failure scenarios:        28
observed pass scenarios:           1
observed failure scenarios:        28
unexpected outcomes:               0
sensitivity ready:                 true
synthetic BEM/FDTD agreement:      false
real BEM/FDTD comparison ready:    false
```

The exact run `262` audit passes. All 28 damaged scenarios fail as expected,
including source-readiness drift, key-coverage drift, nonfinite pairwise values,
frequency-summary drift, mismatch-metric drift, false synthetic-agreement
promotion, and false real-comparison/3D/inversion/field/GPU/FWI promotion.

## Interpretation

The negative-control validator accepts the exact audit and rejects controlled
damage to the source flags, pairwise key coverage, frequency summaries,
recomputed mismatch metrics, and downstream claim states.

This closes the immediate loophole around the synthetic trace-root table: the
table can support plumbing and format checks, but it cannot be promoted into
BEM/FDTD agreement evidence by changing summary flags or dropping rows.

## Decision

Use runs `262-264` as the guarded negative-control package for synthetic
trace-root bins. These bins remain plumbing evidence only. Real FDTD traces and
a real paired BEM/FDTD comparison are still required before any agreement,
3D-validation, inversion, field-transfer, GPU/HPC, or field-FWI claim.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_trace_root_synthetic_bem_pairwise_negative_control_sensitivity.py
6 passed
```

Figure validation:

```text
figures/project_core_bem_halfspace_finite_rebar_trace_root_synthetic_bem_pairwise_negative_control_sensitivity.png
3509x894, dynamic range=255
```

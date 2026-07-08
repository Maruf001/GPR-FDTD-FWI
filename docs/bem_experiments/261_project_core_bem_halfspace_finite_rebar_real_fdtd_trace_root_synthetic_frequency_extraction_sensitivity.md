# BEM Experiment 261: Half-Space Finite-Rebar Real FDTD Trace-Root Synthetic Frequency Extraction Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `260` trace-root frequency-extraction validator against
controlled damage cases.

This run checks whether the validator accepts only the exact run `259`
frequency-extraction smoke and rejects drift in source readiness, trace counts,
role counts, sample counts, receiver/frequency coverage, finite-bin state,
receiver summaries, self-reference fields, and downstream readiness flags.

It does not run real FDTD, ingest real trace files, compare real paired FDTD
files, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/261_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_root_synthetic_frequency_extraction_sensitivity
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_root_synthetic_frequency_extraction_sensitivity_scenarios.csv
data/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_root_synthetic_frequency_extraction_sensitivity_summary.json
figures/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_root_synthetic_frequency_extraction_sensitivity.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_REAL_FDTD_TRACE_ROOT_SYNTHETIC_FREQUENCY_EXTRACTION_SENSITIVITY.md
scripts/run_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_root_synthetic_frequency_extraction_sensitivity.py
scripts/test_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_root_synthetic_frequency_extraction_sensitivity.py
```

## Result

```text
scenarios:                                            31
expected pass scenarios:                              1
expected failure scenarios:                           30
observed pass scenarios:                              1
observed failure scenarios:                           30
unexpected outcomes:                                  0
trace-root frequency-extraction sensitivity ready:    true
real trace files present:                             false
real FDTD frequency extraction ready:                 false
real BEM/FDTD comparison ready:                       false
ready for 3D validation:                              false
inversion-scale half-space ready:                     false
field transfer ready:                                 false
ready for GPU work:                                   false
field FWI ready:                                      false
```

The exact run `259` state passes. The 30 damaged variants fail as expected:

| Damage family | Examples |
| --- | --- |
| Source readiness drift | trace smoke not ready, trace guard not ready, extraction flag false |
| Trace-count drift | synthetic trace files, background traces, target traces, sample count |
| Frequency-bin drift | receiver count, frequency count, bin count, finite-bin count, missing row |
| Receiver-summary drift | row count, frequency count per receiver, sample count per receiver |
| Self-reference drift | reference value mismatch, nonzero self-reference error, flag false |
| Downstream promotion | real traces, real FDTD extraction, real comparison, 3D, inversion, field, GPU, or field FWI marked ready |

## Interpretation

The trace-root frequency-extraction validator has guarded sensitivity
coverage. It accepts the exact synthetic extraction smoke and rejects controlled
corruption of source readiness, counts, finite-bin state, receiver summaries,
self-reference schema fields, and claim-boundary fields.

## Decision

Use runs `259-261` as the guarded trace-root-to-frequency-bin mechanics
package. Real trace files, real FDTD frequency extraction, real BEM/FDTD
comparison, 3D validation, inversion, field transfer, GPU/HPC readiness, and
field FWI remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_root_synthetic_frequency_extraction_sensitivity.py
6 passed
```

Figure validation:

```text
figures/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_root_synthetic_frequency_extraction_sensitivity.png
3473x894, dynamic range=255
```

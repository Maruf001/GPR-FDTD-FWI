# BEM Experiment 259: Half-Space Finite-Rebar Real FDTD Trace-Root Synthetic Frequency Extraction Smoke

Date: 2026-06-28

## Purpose

Extract synthetic frequency bins from the populated trace-root smoke produced
in run `256`.

Runs `256-258` proved that the trace intake layout can pass both fail-closed
and populated-root guards. This run checks the next mechanics step:

```text
Can the accepted trace-root layout be consumed by a frequency-bin extractor?
```

It does not run real FDTD, ingest real trace files, compare real paired FDTD
files, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/259_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_root_synthetic_frequency_extraction_smoke
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_root_synthetic_frequency_bins.csv
data/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_root_synthetic_frequency_receiver_summary.csv
data/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_root_synthetic_frequency_extraction_smoke_summary.json
figures/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_root_synthetic_frequency_extraction_smoke.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_REAL_FDTD_TRACE_ROOT_SYNTHETIC_FREQUENCY_EXTRACTION_SMOKE.md
scripts/run_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_root_synthetic_frequency_extraction_smoke.py
scripts/test_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_root_synthetic_frequency_extraction_smoke.py
```

## Result

```text
synthetic trace files:                     26
background trace files:                    13
target trace files:                        13
receivers:                                 13
frequencies:                               9
frequency bins:                            117
finite frequency bins:                     117
receiver summary rows:                     13
trace samples per file:                    16
synthetic trace-root frequency extraction: true
synthetic frequency bins present:          true
self-reference error reported:             true
real trace files present:                  false
real FDTD frequency extraction ready:      false
real BEM/FDTD comparison ready:            false
ready for 3D validation:                   false
inversion-scale half-space ready:          false
field transfer ready:                      false
ready for GPU work:                        false
field FWI ready:                           false
```

## Interpretation

The accepted synthetic trace-root layout can be consumed by a frequency-bin
extractor. The 26 staged traces produce 117 finite receiver-frequency bins
across 13 receivers and nine required frequencies.

The `reference_scattered_*`, `abs_error`, and `relative_error` fields are
self-reference fields used for schema compatibility. They do not show BEM/FDTD
agreement and should not be interpreted as real comparison accuracy.

## Decision

Use run `259` as the positive trace-root-to-frequency-bin mechanics smoke.
Real trace files, real FDTD frequency extraction, real BEM/FDTD comparison, 3D
validation, inversion, field transfer, GPU/HPC readiness, and field FWI remain
blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_root_synthetic_frequency_extraction_smoke.py
5 passed
```

Figure validation:

```text
figures/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_root_synthetic_frequency_extraction_smoke.png
2536x846, dynamic range=255
```

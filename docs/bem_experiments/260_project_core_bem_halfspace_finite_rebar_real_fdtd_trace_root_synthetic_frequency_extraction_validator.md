# BEM Experiment 260: Half-Space Finite-Rebar Real FDTD Trace-Root Synthetic Frequency Extraction Validator

Date: 2026-06-28

## Purpose

Validate the run `259` trace-root synthetic frequency-extraction smoke from a
consumer perspective.

Run `259` showed that the accepted synthetic trace-root layout can produce a
frequency-bin table. This run checks that the output is internally consistent,
that the self-reference schema boundary is explicit, and that real comparison
states remain blocked.

It does not run real FDTD, ingest real trace files, compare real paired FDTD
files, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/260_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_root_synthetic_frequency_extraction_validator
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_root_synthetic_frequency_extraction_validator_checks.csv
data/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_root_synthetic_frequency_extraction_validator_summary.json
figures/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_root_synthetic_frequency_extraction_validator.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_REAL_FDTD_TRACE_ROOT_SYNTHETIC_FREQUENCY_EXTRACTION_VALIDATOR.md
scripts/run_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_root_synthetic_frequency_extraction_validator.py
scripts/test_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_root_synthetic_frequency_extraction_validator.py
```

## Result

```text
validation checks:                         6
validation passes:                         6
blocking failures:                         0
synthetic extraction validation ready:      true
source frequency bins:                     117
source receiver summaries:                 13
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

The validator checks six requirements:

| Check | Passes |
| --- | ---: |
| source guards and extraction ready | 1 |
| trace and role counts match source contract | 1 |
| frequency bins are complete and finite | 1 |
| receiver summary matches frequency bins | 1 |
| self-reference schema boundary is explicit | 1 |
| real comparison and downstream states blocked | 1 |

## Interpretation

The trace-root synthetic frequency-extraction smoke is internally consistent.
Source guards are ready, 26 traces produce 117 finite bins, receiver summaries
match the bin table, self-reference fields are explicit, and real
extraction/comparison states remain blocked.

## Decision

Use run `260` as the positive validator for trace-root-to-frequency-bin
mechanics. Sensitivity remains required before treating this extraction path as
fully guarded.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_root_synthetic_frequency_extraction_validator.py
7 passed
```

Figure validation:

```text
figures/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_root_synthetic_frequency_extraction_validator.png
2573x841, dynamic range=255
```

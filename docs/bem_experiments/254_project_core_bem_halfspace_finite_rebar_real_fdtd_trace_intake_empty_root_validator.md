# BEM Experiment 254: Half-Space Finite-Rebar Real FDTD Trace Intake Empty-Root Validator

Date: 2026-06-28

## Purpose

Validate the run `253` empty-root dry run from a consumer perspective.

This run checks whether the fail-closed precheck can be trusted before future
real-FDTD trace staging.

It does not run real FDTD, ingest real trace files, extract real frequency
bins, compare real paired FDTD files, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/254_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_empty_root_validator
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_empty_root_validator_checks.csv
data/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_empty_root_validator_summary.json
figures/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_empty_root_validator.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_REAL_FDTD_TRACE_INTAKE_EMPTY_ROOT_VALIDATOR.md
scripts/run_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_empty_root_validator.py
scripts/test_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_empty_root_validator.py
```

## Result

```text
validation checks:                         6
validation passes:                         6
blocking failures:                         0
validation ready:                          true
source dry-run checks:                     182
source dry-run failures:                   182
real trace files present:                  false
real FDTD frequency extraction ready:      false
real BEM/FDTD comparison ready:            false
ready for 3D validation:                   false
inversion-scale half-space ready:          false
field transfer ready:                      false
ready for GPU work:                        false
field FWI ready:                           false
```

The six checks validate:

| Check group | Outcome |
| --- | --- |
| Source readiness | manifest and sensitivity guard are ready |
| Dry-run counts | 182 checks, zero passes, 182 failures |
| Failure reasons | 26 missing trace files and 156 dependent blocked checks |
| Check groups | all seven planned check groups represented, 26 checks each |
| Execution boundary | no shell execution and no real trace promotion |
| Claim boundary | real extraction/comparison and downstream states remain false |

## Interpretation

The empty-root dry run is internally consistent. It proves the precheck fails
closed when the real-FDTD trace root is empty and does not infer real trace
intake, real frequency extraction, or real comparison from absent files.

## Decision

Use run `254` as the positive validator for the empty-root real-FDTD trace
intake dry run. Sensitivity remains required before treating this fail-closed
precheck as fully guarded.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_empty_root_validator.py
7 passed
```

Figure validation:

```text
figures/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_empty_root_validator.png
2501x839, dynamic range=255
```

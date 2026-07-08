# BEM Experiment 252: Half-Space Finite-Rebar Real FDTD Trace Intake Manifest Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `251` real-FDTD trace intake manifest validator against
controlled damage cases.

This run checks whether the validator accepts only the exact manifest and
rejects common source-readiness, trace-coverage, schema, planned-check,
real-intake, and downstream-promotion failures.

This is CPU-only sensitivity validation. It does not run real FDTD, ingest real
trace files, extract real frequency bins, compare real paired FDTD files,
implement full 3D Maxwell BEM, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/252_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_manifest_sensitivity
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_manifest_sensitivity_scenarios.csv
data/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_manifest_sensitivity_summary.json
figures/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_manifest_sensitivity.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_REAL_FDTD_TRACE_INTAKE_MANIFEST_SENSITIVITY.md
scripts/run_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_manifest_sensitivity.py
scripts/test_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_manifest_sensitivity.py
```

## Result

```text
scenarios:                                  35
expected pass scenarios:                    1
expected failure scenarios:                 34
observed pass scenarios:                    1
observed failure scenarios:                 34
unexpected outcomes:                        0
sensitivity ready:                          true
ready for real trace generation:            true
real trace files present:                   false
real FDTD frequency extraction ready:       false
real BEM/FDTD comparison ready:             false
ready for 3D validation:                    false
inversion-scale half-space ready:           false
field transfer ready:                       false
ready for GPU work:                         false
field FWI ready:                            false
```

The exact manifest passes. The 34 damaged variants fail as expected:

| Damage family | Examples |
| --- | --- |
| Source readiness drift | input contract, pairwise guard, or manifest marked not ready |
| Trace coverage drift | trace-count drift, missing trace row, role drift, receiver-key drift |
| Schema drift | schema-count drift, missing schema column, wrong trace format, missing reference/projection requirement |
| Planned-check drift | check-count drift, missing check row, unexpected check group, check executed, check passed |
| Real-intake drift | trace generation not ready, real trace file present, row extraction ready, real references/projection marked ready |
| Downstream promotion | real FDTD extraction, real BEM/FDTD comparison, 3D, inversion, field transfer, GPU, or field FWI marked ready |

## Interpretation

The real-FDTD trace intake manifest validator now has guarded sensitivity
coverage. It accepts the exact manifest and rejects controlled corruption of
the file-role coverage, receiver keys, schema contract, planned checks,
real-intake state, and claim boundary.

This completes a guarded intake-manifest package for future real FDTD trace
generation. It still does not create or accept real trace files.

## Decision

Use runs `250-252` as the guarded real-FDTD trace intake manifest package.
Real trace files, real projection convention, real time-zero/amplitude
references, real frequency extraction, real BEM/FDTD comparison, 3D validation,
inversion-scale use, field transfer, GPU/HPC readiness, and field FWI remain
blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_manifest_sensitivity.py
7 passed
```

Figure validation:

```text
figures/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_manifest_sensitivity.png
3761x886, dynamic range=255
```

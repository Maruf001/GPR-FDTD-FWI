# BEM Experiment 255: Half-Space Finite-Rebar Real FDTD Trace Intake Empty-Root Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `254` empty-root dry-run validator against controlled
damage cases.

This run checks whether the validator accepts only the exact fail-closed dry
run and rejects source-readiness, count, failure-reason, check-group,
shell-execution, real-trace, and downstream-promotion drift.

It does not run real FDTD, ingest real trace files, extract real frequency
bins, compare real paired FDTD files, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/255_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_empty_root_sensitivity
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_empty_root_sensitivity_scenarios.csv
data/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_empty_root_sensitivity_summary.json
figures/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_empty_root_sensitivity.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_REAL_FDTD_TRACE_INTAKE_EMPTY_ROOT_SENSITIVITY.md
scripts/run_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_empty_root_sensitivity.py
scripts/test_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_empty_root_sensitivity.py
```

## Result

```text
scenarios:                                  22
expected pass scenarios:                    1
expected failure scenarios:                 21
observed pass scenarios:                    1
observed failure scenarios:                 21
unexpected outcomes:                        0
sensitivity ready:                          true
real trace files present:                   false
real FDTD frequency extraction ready:       false
real BEM/FDTD comparison ready:             false
ready for 3D validation:                    false
inversion-scale half-space ready:           false
field transfer ready:                       false
ready for GPU work:                         false
field FWI ready:                            false
```

The exact fail-closed dry run passes. The 21 damaged variants fail as expected:

| Damage family | Examples |
| --- | --- |
| Source readiness drift | manifest not ready, guard not ready, fail-closed flag false |
| Dry-run count drift | check count, pass count, fail count, row pass |
| Failure-reason drift | wrong failure reason, missing-file count drift |
| Check-group drift | check group changed |
| Execution/trace drift | shell execution, real trace files present |
| Downstream promotion | real FDTD extraction, real comparison, 3D, inversion, field, GPU, or field FWI marked ready |

## Interpretation

The empty-root dry-run validator now has guarded sensitivity coverage. It
accepts the exact fail-closed dry run and rejects controlled corruption of the
failure shape, execution boundary, and claim boundary.

## Decision

Use runs `253-255` as the guarded fail-closed precheck package for future
real-FDTD trace staging. Real trace files, real frequency extraction, real
BEM/FDTD comparison, 3D validation, inversion, field transfer, GPU/HPC
readiness, and field FWI remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_empty_root_sensitivity.py
6 passed
```

Figure validation:

```text
figures/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_empty_root_sensitivity.png
3401x891, dynamic range=255
```

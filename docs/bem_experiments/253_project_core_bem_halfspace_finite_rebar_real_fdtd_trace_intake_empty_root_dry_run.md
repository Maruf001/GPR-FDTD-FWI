# BEM Experiment 253: Half-Space Finite-Rebar Real FDTD Trace Intake Empty-Root Dry Run

Date: 2026-06-28

## Purpose

Evaluate the guarded real-FDTD trace intake manifest against an empty trace
root.

This run checks whether the manifest evaluator fails closed when no projected
trace files are staged.

It does not run real FDTD, ingest real trace files, extract real frequency
bins, compare real paired FDTD files, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/253_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_empty_root_dry_run
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_empty_root_dry_run_checks.csv
data/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_empty_root_dry_run_summary.json
figures/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_empty_root_dry_run.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_REAL_FDTD_TRACE_INTAKE_EMPTY_ROOT_DRY_RUN.md
scripts/run_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_empty_root_dry_run.py
scripts/test_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_empty_root_dry_run.py
```

## Result

```text
source manifest ready:                      true
source manifest guard ready:                true
dry-run checks:                             182
dry-run passes:                             0
dry-run failures:                           182
required trace files:                       26
file-present failures:                      26
blocked-by-missing-file failures:           156
check groups:                               7
empty-root dry run fail-closed ready:       true
shell commands executed:                    false
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

The guarded real-FDTD trace intake manifest fails closed against an empty trace
root. All 182 planned checks fail: 26 file-present checks fail because the
required trace files are absent, and 156 dependent checks remain blocked by the
missing files.

No shell commands are executed and no real extraction is inferred.

## Decision

Use run `253` as the fail-closed precheck for future real-FDTD trace staging.
Real trace files, real frequency extraction, real BEM/FDTD comparison, 3D
validation, inversion-scale use, field transfer, GPU/HPC readiness, and field
FWI remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_empty_root_dry_run.py
4 passed
```

Figure validation:

```text
figures/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_empty_root_dry_run.png
2500x847, dynamic range=255
```

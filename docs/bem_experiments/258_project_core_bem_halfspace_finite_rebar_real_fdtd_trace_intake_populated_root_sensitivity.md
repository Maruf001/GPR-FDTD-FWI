# BEM Experiment 258: Half-Space Finite-Rebar Real FDTD Trace Intake Populated-Root Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `257` populated-root synthetic validator against controlled
damage cases.

This run checks whether the validator accepts only the exact run `256`
synthetic acceptance smoke and rejects drift in source readiness, trace
inventory, sample counts, check counts, check groups, checksums, execution
state, synthetic/real trace boundaries, and downstream readiness flags.

It does not run real FDTD, ingest real trace files, extract real frequency
bins, compare real paired FDTD files, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/258_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_populated_root_sensitivity
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_populated_root_sensitivity_scenarios.csv
data/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_populated_root_sensitivity_summary.json
figures/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_populated_root_sensitivity.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_REAL_FDTD_TRACE_INTAKE_POPULATED_ROOT_SENSITIVITY.md
scripts/run_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_populated_root_sensitivity.py
scripts/test_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_populated_root_sensitivity.py
```

## Result

```text
scenarios:                                  30
expected pass scenarios:                    1
expected failure scenarios:                 29
observed pass scenarios:                    1
observed failure scenarios:                 29
unexpected outcomes:                        0
populated-root synthetic sensitivity ready: true
real trace files present:                   false
real FDTD frequency extraction ready:       false
real BEM/FDTD comparison ready:             false
ready for 3D validation:                    false
inversion-scale half-space ready:           false
field transfer ready:                       false
ready for GPU work:                         false
field FWI ready:                            false
```

The exact run `256` state passes. The 29 damaged variants fail as expected:

| Damage family | Examples |
| --- | --- |
| Source readiness drift | manifest not ready, empty-root guard not ready, acceptance flag false |
| Trace inventory drift | file-count, per-file samples, total samples, missing inventory row |
| Manifest check drift | check-count, pass-count, failure-count, check-group, missing check row |
| Checksum drift | missing row checksum, missing inventory checksum |
| Execution boundary drift | shell execution marked true |
| Synthetic/real boundary drift | synthetic trace flag false, real trace flag true |
| Downstream promotion | real FDTD extraction, real comparison, 3D, inversion, field, GPU, or field FWI marked ready |

## Interpretation

The populated-root synthetic validator has guarded sensitivity coverage. It
accepts the exact synthetic acceptance smoke and rejects controlled corruption
of inventory, sample, check, checksum, execution, and claim-boundary fields.

## Decision

Use runs `256-258` as the guarded positive acceptance-mechanics package for
future real-FDTD trace staging. Real trace files, real frequency extraction,
real BEM/FDTD comparison, 3D validation, inversion, field transfer, GPU/HPC
readiness, and field FWI remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_populated_root_sensitivity.py
6 passed
```

Figure validation:

```text
figures/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_populated_root_sensitivity.png
3437x891, dynamic range=255
```

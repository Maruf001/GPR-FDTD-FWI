# BEM Experiment 251: Half-Space Finite-Rebar Real FDTD Trace Intake Manifest Validator

Date: 2026-06-28

## Purpose

Validate the run `250` real-FDTD trace intake manifest from a consumer
perspective.

This run checks whether the manifest can be safely used as a future real-trace
generation and intake target while still blocking real frequency extraction,
real BEM/FDTD comparison, 3D validation, inversion-scale use, field transfer,
GPU/HPC readiness, and field FWI.

This is CPU-only validation. It does not run real FDTD, ingest real trace
files, extract real frequency bins, compare real paired FDTD files, implement
full 3D Maxwell BEM, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/251_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_manifest_validator
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_manifest_validator_checks.csv
data/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_manifest_validator_summary.json
figures/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_manifest_validator.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_REAL_FDTD_TRACE_INTAKE_MANIFEST_VALIDATOR.md
scripts/run_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_manifest_validator.py
scripts/test_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_manifest_validator.py
```

## Result

```text
validation checks:                         6
validation passes:                         6
blocking failures:                         0
validation ready:                          true
source required trace files:               26
source planned checks:                     182
ready for real trace generation:           true
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
| Source readiness | input contract, pairwise guard, and manifest are ready |
| Trace/receiver coverage | 26 trace rows, two roles, 13 receivers, two traces per receiver |
| Schema requirements | 13 schema columns, 9 frequencies, CSV trace table format, references and projection required |
| Planned checks | 182 planned checks, seven check groups, none executed |
| Intake boundary | ready for trace generation, no real traces/projection/references/extraction |
| Claim boundary | real comparison and downstream states remain false |

## Interpretation

The real-FDTD trace intake manifest is internally consistent. It gives the
next real FDTD generation target a precise shape: two projected scalar trace
roles, 13 receiver keys, 26 trace files, and 182 planned checks.

The artifact remains a validator for a future intake package. It does not
ingest or accept real trace files.

## Decision

Use run `251` as the consumer validator for the real-FDTD trace intake
manifest. Sensitivity remains required before treating the manifest guard as
robust.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_manifest_validator.py
7 passed
```

Figure validation:

```text
figures/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_manifest_validator.png
2537x840, dynamic range=255
```

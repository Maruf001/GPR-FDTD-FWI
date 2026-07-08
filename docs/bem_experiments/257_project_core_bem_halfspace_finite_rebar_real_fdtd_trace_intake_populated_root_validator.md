# BEM Experiment 257: Half-Space Finite-Rebar Real FDTD Trace Intake Populated-Root Validator

Date: 2026-06-28

## Purpose

Validate the run `256` populated-root synthetic smoke from a consumer
perspective.

Run `256` showed that the manifest mechanics can accept a correctly staged
synthetic trace root. This run checks whether that acceptance state is
internally consistent and keeps the real-data claim boundary intact.

It does not run real FDTD, ingest real trace files, extract real frequency
bins, compare real paired FDTD files, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/257_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_populated_root_validator
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_populated_root_validator_checks.csv
data/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_populated_root_validator_summary.json
figures/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_populated_root_validator.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_REAL_FDTD_TRACE_INTAKE_POPULATED_ROOT_VALIDATOR.md
scripts/run_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_populated_root_validator.py
scripts/test_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_populated_root_validator.py
```

## Result

```text
validation checks:                         6
validation passes:                         6
blocking failures:                         0
populated-root synthetic validation ready: true
source synthetic trace files:              26
source populated-root checks:              182
synthetic trace files present:             true
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
| source guards and acceptance ready | 1 |
| trace inventory matches manifest count | 1 |
| populated-root checks all pass | 1 |
| check-group coverage is complete | 1 |
| checksums and execution boundary hold | 1 |
| real comparison and downstream states blocked | 1 |

## Interpretation

The populated-root synthetic smoke is internally consistent. Source guards are
ready, 26 synthetic trace files are staged, all 182 checks pass across seven
groups, checksums are recorded, no shell commands are executed, and real
extraction/comparison states remain blocked.

## Decision

Use run `257` as the positive validator for the populated-root synthetic
acceptance smoke. Sensitivity remains required before treating this acceptance
path as fully guarded.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_populated_root_validator.py
8 passed
```

Figure validation:

```text
figures/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_populated_root_validator.png
2573x841, dynamic range=255
```

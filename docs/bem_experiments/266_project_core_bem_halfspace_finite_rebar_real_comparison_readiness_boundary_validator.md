# BEM Experiment 266: Half-Space Finite-Rebar Real Comparison Readiness Boundary Validator

Date: 2026-06-28

## Purpose

Validate the run `265` real-comparison readiness boundary from a consumer
perspective.

Run `265` joined the BEM comparison contract, exporter, synthetic trace
mechanics, and negative-control boundary into one real-comparison readiness
table. This run checks that the table has the expected items, status counts,
synthetic-only boundary, real blockers, and downstream no-go states.

It does not run real FDTD, ingest real trace files, claim BEM/FDTD agreement,
launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/266_project_core_bem_halfspace_finite_rebar_real_comparison_readiness_boundary_validator
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_real_comparison_readiness_boundary_validator_checks.csv
data/project_core_bem_halfspace_finite_rebar_real_comparison_readiness_boundary_validator_summary.json
figures/project_core_bem_halfspace_finite_rebar_real_comparison_readiness_boundary_validator.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_REAL_COMPARISON_READINESS_BOUNDARY_VALIDATOR.md
scripts/run_project_core_bem_halfspace_finite_rebar_real_comparison_readiness_boundary_validator.py
scripts/test_project_core_bem_halfspace_finite_rebar_real_comparison_readiness_boundary_validator.py
```

## Result

```text
validation checks:                 5
validation passes:                 5
blocking failures:                 0
validation ready:                  true
source boundary items:             10
source blocking items:             4
real BEM/FDTD comparison ready:    false
ready for GPU work:                false
field FWI ready:                   false
```

The validator checks:

| Check | Result |
| --- | --- |
| Boundary summary counts are consistent | pass |
| Boundary items and statuses match contract | pass |
| Synthetic support is not real agreement | pass |
| Required real blockers are present | pass |
| Real comparison and downstream states are blocked | pass |

## Interpretation

The readiness boundary is internally consistent. The expected 10 items are
present, synthetic-only support is not treated as real agreement, and the four
real-comparison blockers are explicit.

## Decision

Use run `266` as the positive validator for the real-comparison readiness
boundary. Sensitivity remains required before treating the boundary as fully
guarded.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_real_comparison_readiness_boundary_validator.py
5 passed
```

Figure validation:

```text
figures/project_core_bem_halfspace_finite_rebar_real_comparison_readiness_boundary_validator.png
2573x841, dynamic range=255
```

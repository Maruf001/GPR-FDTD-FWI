# BEM Experiment 267: Half-Space Finite-Rebar Real Comparison Readiness Boundary Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `266` real-comparison readiness-boundary validator.

Run `266` validated the run `265` readiness boundary. This run checks whether
that validator fails closed when item counts, status counts, synthetic-only
boundaries, real blocker rows, needed-next fields, or downstream readiness
states are damaged.

It does not run real FDTD, ingest real trace files, claim BEM/FDTD agreement,
launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/267_project_core_bem_halfspace_finite_rebar_real_comparison_readiness_boundary_sensitivity
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_real_comparison_readiness_boundary_sensitivity_scenarios.csv
data/project_core_bem_halfspace_finite_rebar_real_comparison_readiness_boundary_sensitivity_summary.json
figures/project_core_bem_halfspace_finite_rebar_real_comparison_readiness_boundary_sensitivity.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_REAL_COMPARISON_READINESS_BOUNDARY_SENSITIVITY.md
scripts/run_project_core_bem_halfspace_finite_rebar_real_comparison_readiness_boundary_sensitivity.py
scripts/test_project_core_bem_halfspace_finite_rebar_real_comparison_readiness_boundary_sensitivity.py
```

## Result

```text
scenarios:                         23
expected pass scenarios:           1
expected failure scenarios:        22
observed pass scenarios:           1
observed failure scenarios:        22
unexpected outcomes:               0
sensitivity ready:                 true
real BEM/FDTD comparison ready:    false
field FWI ready:                   false
```

The exact run `265` boundary passes. All 22 damaged scenarios fail as expected,
including item-count drift, status-count drift, synthetic support promotion,
missing real blockers, missing next-action fields, and false real/downstream
readiness.

## Interpretation

The readiness-boundary validator accepts the exact run `265` boundary and
rejects controlled damage to the fields that matter. The real-comparison
blocker table is now guarded: synthetic plumbing remains separated from real
agreement evidence.

## Decision

Use runs `265-267` as the guarded real-comparison readiness boundary. Real FDTD
trace files, real frequency extraction, real paired comparison, and threshold
calibration remain required.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_real_comparison_readiness_boundary_sensitivity.py
6 passed
```

Figure validation:

```text
figures/project_core_bem_halfspace_finite_rebar_real_comparison_readiness_boundary_sensitivity.png
3365x886, dynamic range=255
```

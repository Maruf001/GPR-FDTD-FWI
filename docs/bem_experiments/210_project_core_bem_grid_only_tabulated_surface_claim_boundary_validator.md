# BEM Experiment 210: Grid-Only Tabulated Surface Claim Boundary Validator

Date: 2026-06-28

## Purpose

Validate the run `209` refreshed BEM claim boundary from a consumer
perspective.

This is a CPU-only validation run. It does not rerun FDTD/BEM solvers, compare
against field data, launch GPU/HPC work, run 3D validation, run field FWI, or
promote results to synthetic `outputs/experiments`.

## Output

```text
outputs/bem_experiments/210_project_core_bem_grid_only_tabulated_surface_claim_boundary_validator
```

Key artifacts:

```text
data/project_core_bem_grid_only_tabulated_surface_claim_boundary_validation_checks.csv
data/project_core_bem_grid_only_tabulated_surface_claim_boundary_validator_summary.json
figures/project_core_bem_grid_only_tabulated_surface_claim_boundary_validator.png
docs/PROJECT_CORE_BEM_GRID_ONLY_TABULATED_SURFACE_CLAIM_BOUNDARY_VALIDATOR.md
scripts/run_project_core_bem_grid_only_tabulated_surface_claim_boundary_validator.py
scripts/test_project_core_bem_grid_only_tabulated_surface_claim_boundary_validator.py
```

## Result

```text
validation checks:                  13
validation passes:                  13
blocking failures:                  0
recommended practical claim:        grid15_tabulated_surface_offset_repair
recommended surface policy:         grid_15mm_only
recommended surface samples:        13
recommended surface worst L2:       0.6083307089797199
claim-boundary validation ready:    true
claim-boundary sensitivity ready:   true
analytic contract refresh ready:    false
field transfer ready:               false
3D validation ready:                false
GPU work ready:                     false
field FWI ready:                    false
```

The validator confirms:

| Check family | Result |
| --- | --- |
| Claim count | Passed |
| Ready/blocked counts | Passed |
| Single recommended practical policy | Passed |
| 15 mm grid-only ready with positive margin | Passed |
| 20 mm grid-only blocked with negative margin | Passed |
| Analytic shell support remains scoped-ready | Passed |
| Depth-robust analytic shell rule remains blocked | Passed |
| Analytic replacement claim remains blocked | Passed |
| Field transfer claim remains blocked | Passed |
| Previous 10 mm plus-exact policy is superseded | Passed |
| Claim-boundary refresh marked ready | Passed |
| Analytic contract refresh remains blocked | Passed |
| Field, 3D, GPU, and field FWI remain blocked | Passed |

## Interpretation

The refreshed claim boundary is consumer-valid. Exactly one practical policy is
recommended, 15 mm grid-only is ready with positive margin, 20 mm grid-only and
analytic/field overclaims remain blocked, and downstream promotion flags remain
blocked.

## Decision

Use run `210` as the validator for the run `209` refreshed BEM claim boundary.
Add negative-control sensitivity before downstream use.

## Validation

Focused tests:

```text
tests/test_project_core_bem_grid_only_tabulated_surface_claim_boundary_validator.py
5 passed
```

Figure validation:

```text
project_core_bem_grid_only_tabulated_surface_claim_boundary_validator.png
2825x859, dynamic range=255
```

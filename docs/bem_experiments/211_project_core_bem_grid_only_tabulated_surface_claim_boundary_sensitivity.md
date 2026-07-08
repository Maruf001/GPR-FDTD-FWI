# BEM Experiment 211: Grid-Only Tabulated Surface Claim Boundary Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `210` refreshed claim-boundary validator with damaged
variants of the run `209` result.

This is a CPU-only guard run. It does not rerun FDTD/BEM solvers, compare
against field data, launch GPU/HPC work, run 3D validation, run field FWI, or
promote results to synthetic `outputs/experiments`.

## Output

```text
outputs/bem_experiments/211_project_core_bem_grid_only_tabulated_surface_claim_boundary_sensitivity
```

Key artifacts:

```text
data/project_core_bem_grid_only_tabulated_surface_claim_boundary_sensitivity_rows.csv
data/project_core_bem_grid_only_tabulated_surface_claim_boundary_sensitivity_summary.json
figures/project_core_bem_grid_only_tabulated_surface_claim_boundary_sensitivity.png
docs/PROJECT_CORE_BEM_GRID_ONLY_TABULATED_SURFACE_CLAIM_BOUNDARY_SENSITIVITY.md
scripts/run_project_core_bem_grid_only_tabulated_surface_claim_boundary_sensitivity.py
scripts/test_project_core_bem_grid_only_tabulated_surface_claim_boundary_sensitivity.py
```

## Result

```text
sensitivity scenarios:              14
expected pass scenarios:            1
observed pass scenarios:            1
expected failure scenarios:         13
observed failure scenarios:         13
unexpected outcomes:                0
claim-boundary sensitivity ready:   true
analytic contract refresh ready:    false
field transfer ready:               false
3D validation ready:                false
GPU work ready:                     false
field FWI ready:                    false
```

The exact refreshed claim boundary passes. Thirteen damaged variants fail:

| Scenario | Expected | Observed | Failed checks |
| --- | --- | --- | --- |
| exact claim boundary | pass | pass | none |
| missing 15 mm grid claim | fail | fail | claim count, ready/blocked count, recommended policy, grid15 readiness |
| multiple recommended claims | fail | fail | recommended policy, scoped analytic support |
| grid15 marked blocked | fail | fail | ready/blocked count, grid15 readiness |
| grid15 negative margin | fail | fail | grid15 readiness |
| grid20 marked ready | fail | fail | ready/blocked count, grid20 block |
| analytic shell marked not ready | fail | fail | ready/blocked count, scoped analytic support |
| depth-robust marked ready | fail | fail | ready/blocked count, depth-robust block |
| analytic replacement marked ready | fail | fail | ready/blocked count, analytic replacement block |
| field transfer claim marked ready | fail | fail | ready/blocked count, field transfer block |
| previous 10 mm not superseded | fail | fail | superseded-policy flag |
| claim boundary marked not ready | fail | fail | refresh-ready flag |
| analytic contract refresh marked ready | fail | fail | analytic refresh block |
| field transfer marked ready | fail | fail | field/3D/GPU/FWI block |

## Interpretation

The run `210` validator is sensitive to the important claim-language failure
modes: missing or duplicated recommendations, grid15/grid20 claim drift,
analytic overclaims, field-transfer overclaims, and summary promotion flags.

## Decision

Use runs `209`-`211` as the guarded refreshed BEM claim-boundary package. The
practical claim is 15 mm grid-only for the tested 35 mm offset family. Analytic
replacement, field transfer, 3D validation, GPU/HPC, field FWI, and synthetic
`outputs/experiments` promotion remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_grid_only_tabulated_surface_claim_boundary_sensitivity.py
4 passed
```

Figure validation:

```text
project_core_bem_grid_only_tabulated_surface_claim_boundary_sensitivity.png
3005x883, dynamic range=255
```

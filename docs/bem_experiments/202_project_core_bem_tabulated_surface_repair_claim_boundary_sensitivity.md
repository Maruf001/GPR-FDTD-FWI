# BEM Experiment 202: Tabulated Surface Repair Claim Boundary Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `201` claim-boundary validator with damaged variants of
the run `200` BEM claim-boundary synthesis.

This is a CPU-only guard run. It does not rerun FDTD/BEM solvers, compare
against field data, launch GPU/HPC work, run 3D validation, run field FWI, or
promote results to synthetic `outputs/experiments`.

## Output

```text
outputs/bem_experiments/202_project_core_bem_tabulated_surface_repair_claim_boundary_sensitivity
```

Key artifacts:

```text
data/project_core_bem_tabulated_surface_repair_claim_boundary_sensitivity_rows.csv
data/project_core_bem_tabulated_surface_repair_claim_boundary_sensitivity_summary.json
figures/project_core_bem_tabulated_surface_repair_claim_boundary_sensitivity.png
docs/PROJECT_CORE_BEM_TABULATED_SURFACE_REPAIR_CLAIM_BOUNDARY_SENSITIVITY.md
scripts/run_project_core_bem_tabulated_surface_repair_claim_boundary_sensitivity.py
scripts/test_project_core_bem_tabulated_surface_repair_claim_boundary_sensitivity.py
```

## Result

```text
sensitivity scenarios:              10
expected pass scenarios:            1
observed pass scenarios:            1
expected failure scenarios:         9
observed failure scenarios:         9
unexpected outcomes:                0
claim-boundary sensitivity ready:   true
analytic contract refresh ready:    false
field transfer ready:               false
3D validation ready:                false
GPU work ready:                     false
field FWI ready:                    false
```

The exact claim-boundary synthesis passes. The nine damaged variants all fail:

| Scenario | Expected | Observed | Failed checks |
| --- | --- | --- | --- |
| exact claim boundary | pass | pass | none |
| missing offset-family claim | fail | fail | claim count, ready/blocked count, offset-family readiness |
| offset-family marked blocked | fail | fail | ready/blocked count, offset-family readiness |
| offset-family negative margin | fail | fail | offset-family readiness |
| depth-robust analytic shell marked ready | fail | fail | ready/blocked count, depth-robust block |
| depth-robust analytic shell positive margin | fail | fail | depth-robust block |
| analytic replacement marked ready | fail | fail | ready/blocked count, analytic replacement block |
| synthesis marked not ready | fail | fail | synthesis-ready flag |
| analytic contract refresh marked ready | fail | fail | analytic refresh block |
| field transfer marked ready | fail | fail | field/3D/GPU/FWI block |

## Interpretation

The run `201` validator is sensitive to the important overclaim modes. It
detects missing or demoted tabulated-surface repair claims, premature analytic
overclaims, and premature field/3D/GPU promotion flags.

## Decision

Use runs `200`-`202` as the guarded BEM claim-boundary package. The supported
claim is a scoped analytic shell-support contract plus a guarded
tabulated-surface repair for the tested 35 mm offset family. Do not claim
depth-robust analytic replacement, field transfer, 3D validation, GPU/HPC
readiness, field FWI readiness, or synthetic `outputs/experiments` promotion
from this package.

## Validation

Focused tests:

```text
tests/test_project_core_bem_tabulated_surface_repair_claim_boundary_sensitivity.py
4 passed
```

Figure validation:

```text
project_core_bem_tabulated_surface_repair_claim_boundary_sensitivity.png
2789x865, dynamic range=255
```

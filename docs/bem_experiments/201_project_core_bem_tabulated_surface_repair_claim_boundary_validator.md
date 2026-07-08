# BEM Experiment 201: Tabulated Surface Repair Claim Boundary Validator

Date: 2026-06-27

## Purpose

Validate the run `200` BEM claim-boundary synthesis from a consumer
perspective.

This is a CPU-only validation run. It does not rerun FDTD/BEM solvers, compare
against field data, launch GPU/HPC work, run 3D validation, run field FWI, or
promote results to synthetic `outputs/experiments`.

## Output

```text
outputs/bem_experiments/201_project_core_bem_tabulated_surface_repair_claim_boundary_validator
```

Key artifacts:

```text
data/project_core_bem_tabulated_surface_repair_claim_boundary_validation_checks.csv
data/project_core_bem_tabulated_surface_repair_claim_boundary_validator_summary.json
figures/project_core_bem_tabulated_surface_repair_claim_boundary_validator.png
docs/PROJECT_CORE_BEM_TABULATED_SURFACE_REPAIR_CLAIM_BOUNDARY_VALIDATOR.md
scripts/run_project_core_bem_tabulated_surface_repair_claim_boundary_validator.py
scripts/test_project_core_bem_tabulated_surface_repair_claim_boundary_validator.py
```

## Result

```text
validation checks:                  8
validation passes:                  8
blocking failures:                  0
source claims:                      5
source ready claims:                3
source blocked claims:              2
claim-boundary validation ready:    true
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
| Offset-family tabulated repair ready with positive margin | Passed |
| Depth-robust analytic shell rule blocked with negative margin | Passed |
| Analytic replacement claim blocked | Passed |
| Claim-boundary synthesis ready | Passed |
| Analytic contract refresh remains blocked | Passed |
| Field, 3D, GPU, and field FWI remain blocked | Passed |

## Interpretation

The claim-boundary synthesis is consumer-valid. The ready and blocked claim
counts match, the offset-family tabulated repair is ready with positive margin,
analytic overclaims remain blocked, and field/3D/GPU states remain blocked.

## Decision

Use run `201` as the validator for BEM claim-boundary language. Add
negative-control sensitivity before using the synthesis as a report or
presentation source.

## Validation

Focused tests:

```text
tests/test_project_core_bem_tabulated_surface_repair_claim_boundary_synthesis.py
tests/test_project_core_bem_tabulated_surface_repair_claim_boundary_validator.py
7 passed
```

Figure validation:

```text
project_core_bem_tabulated_surface_repair_claim_boundary_validator.png
2591x840, dynamic range=255
```

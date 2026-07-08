# BEM Experiment 207: Tabulated Surface Grid-Only Ablation Validator

Date: 2026-06-28

## Purpose

Validate the run `206` grid-only ablation result from a consumer perspective.

This is a CPU-only validation run. It does not rerun FDTD/BEM solvers, compare
against field data, launch GPU/HPC work, run 3D validation, run field FWI, or
promote results to synthetic `outputs/experiments`.

## Output

```text
outputs/bem_experiments/207_project_core_bem_layered_payload_tabulated_surface_grid_only_ablation_validator
```

Key artifacts:

```text
data/project_core_bem_layered_payload_tabulated_surface_grid_only_ablation_validation_checks.csv
data/project_core_bem_layered_payload_tabulated_surface_grid_only_ablation_validator_summary.json
figures/project_core_bem_layered_payload_tabulated_surface_grid_only_ablation_validator.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_TABULATED_SURFACE_GRID_ONLY_ABLATION_VALIDATOR.md
scripts/run_project_core_bem_layered_payload_tabulated_surface_grid_only_ablation_validator.py
scripts/test_project_core_bem_layered_payload_tabulated_surface_grid_only_ablation_validator.py
```

## Result

```text
validation checks:                  13
validation passes:                  13
blocking failures:                  0
cheapest all-case-ready policy:     grid_15mm_only
cheapest all-case-ready samples:    13
cheapest all-case-ready worst L2:   0.6083307089797199
lower-sample than 10 mm ready:      true
grid-only validation ready:         true
grid-only sensitivity ready:        true
analytic contract refresh ready:    false
field transfer ready:               false
3D validation ready:                false
GPU work ready:                     false
field FWI ready:                    false
```

The validator confirms:

| Check family | Result |
| --- | --- |
| Support/policy row count | Passed |
| Case, support-mode, and policy counts | Passed |
| 20 mm grid-only fails the boundary | Passed |
| 20 mm plus exact fails the boundary | Passed |
| 15 mm grid-only is the cheapest ready policy | Passed |
| 15 mm grid-only does not include exact source/receiver points | Passed |
| 15 mm plus exact is ready but uses more samples | Passed |
| 10 mm plus exact remains a higher-sample ready baseline | Passed |
| 5 mm grid-only is the best observed accuracy reference | Passed |
| Lower-sample than 10 mm plus exact is marked ready | Passed |
| Grid-only ablation is marked ready | Passed |
| Analytic contract refresh remains blocked | Passed |
| Field, 3D, GPU, and field FWI remain blocked | Passed |

## Interpretation

The grid-only ablation is consumer-valid. The 20 mm policies remain failed,
15 mm grid-only is the cheapest all-case-ready policy, exact source/receiver
insertion is not required for that policy, and downstream promotion flags remain
blocked.

## Decision

Use run `207` as the validator for the run `206` grid-only ablation. Add
negative-control sensitivity before refreshing the BEM tabulated-surface claim
boundary around 15 mm grid-only.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_tabulated_surface_grid_only_ablation_validator.py
5 passed
```

Figure validation:

```text
project_core_bem_layered_payload_tabulated_surface_grid_only_ablation_validator.png
2807x873, dynamic range=255
```

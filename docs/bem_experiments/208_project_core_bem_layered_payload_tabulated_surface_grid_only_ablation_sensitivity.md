# BEM Experiment 208: Tabulated Surface Grid-Only Ablation Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `207` grid-only ablation validator with damaged variants of
the run `206` result.

This is a CPU-only guard run. It does not rerun FDTD/BEM solvers, compare
against field data, launch GPU/HPC work, run 3D validation, run field FWI, or
promote results to synthetic `outputs/experiments`.

## Output

```text
outputs/bem_experiments/208_project_core_bem_layered_payload_tabulated_surface_grid_only_ablation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_layered_payload_tabulated_surface_grid_only_ablation_sensitivity_rows.csv
data/project_core_bem_layered_payload_tabulated_surface_grid_only_ablation_sensitivity_summary.json
figures/project_core_bem_layered_payload_tabulated_surface_grid_only_ablation_sensitivity.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_TABULATED_SURFACE_GRID_ONLY_ABLATION_SENSITIVITY.md
scripts/run_project_core_bem_layered_payload_tabulated_surface_grid_only_ablation_sensitivity.py
scripts/test_project_core_bem_layered_payload_tabulated_surface_grid_only_ablation_sensitivity.py
```

## Result

```text
sensitivity scenarios:              13
expected pass scenarios:            1
observed pass scenarios:            1
expected failure scenarios:         12
observed failure scenarios:         12
unexpected outcomes:                0
grid-only ablation sensitivity:     true
analytic contract refresh ready:    false
field transfer ready:               false
3D validation ready:                false
GPU work ready:                     false
field FWI ready:                    false
```

The exact grid-only ablation passes. Twelve damaged variants fail:

| Scenario | Expected | Observed | Failed checks |
| --- | --- | --- | --- |
| exact grid-only ablation | pass | pass | none |
| missing 15 mm grid policy | fail | fail | 15 mm cheapest policy, no exact insertion, 15 mm plus-exact comparison, 10 mm baseline |
| support/policy row-count drift | fail | fail | row count |
| 20 mm grid promoted | fail | fail | 20 mm grid failure |
| 20 mm plus exact promoted | fail | fail | 20 mm plus-exact failure |
| 15 mm grid marked not ready | fail | fail | 15 mm cheapest policy |
| 15 mm grid exact inserted | fail | fail | no exact insertion |
| 15 mm grid sample-count drift | fail | fail | 15 mm cheapest policy, 10 mm baseline |
| cheapest policy changed from 15 mm grid | fail | fail | 15 mm cheapest policy |
| lower-sample readiness removed | fail | fail | lower-sample readiness |
| grid-only ablation marked not ready | fail | fail | ablation-ready flag |
| analytic contract refresh marked ready | fail | fail | analytic refresh block |
| field transfer marked ready | fail | fail | field/3D/GPU/FWI block |

## Interpretation

The run `207` validator is sensitive to the important overclaim and drift
modes: missing 15 mm grid-only evidence, 20 mm overpromotion, exact-insertion
drift, cheapest-policy drift, and premature analytic or field promotion.

## Decision

Use runs `206`-`208` as the guarded BEM grid-only tabulated-surface package.
The practical policy for the tested five-case 35 mm offset family is 15 mm
grid-only. Analytic replacement, field transfer, 3D validation, GPU/HPC, field
FWI, and synthetic `outputs/experiments` promotion remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_tabulated_surface_grid_only_ablation_sensitivity.py
4 passed
```

Figure validation:

```text
project_core_bem_layered_payload_tabulated_surface_grid_only_ablation_sensitivity.png
2969x882, dynamic range=255
```

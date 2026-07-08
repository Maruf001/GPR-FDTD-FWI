# BEM Experiment 223: Tabulated-Surface Scaling Budget Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `222` tabulated-surface scaling budget validator with
damaged scaling summaries.

This run does not run new FDTD/FWI, use field data, perform 3D validation,
launch GPU/HPC work, or promote inversion-scale half-space BEM.

## Output

```text
outputs/bem_experiments/223_project_core_bem_tabulated_surface_scaling_budget_sensitivity
```

Key artifacts:

```text
data/project_core_bem_tabulated_surface_scaling_budget_sensitivity_scenarios.csv
data/project_core_bem_tabulated_surface_scaling_budget_sensitivity_summary.json
figures/project_core_bem_tabulated_surface_scaling_budget_sensitivity.png
docs/PROJECT_CORE_BEM_TABULATED_SURFACE_SCALING_BUDGET_SENSITIVITY.md
scripts/run_project_core_bem_tabulated_surface_scaling_budget_sensitivity.py
scripts/test_project_core_bem_tabulated_surface_scaling_budget_sensitivity.py
```

## Result

```text
scenarios:                         21
expected pass scenarios:           1
expected failure scenarios:        20
observed pass scenarios:           1
observed failure scenarios:        20
unexpected outcomes:               0
sensitivity ready:                 true
inversion-scale half-space ready:  false
field transfer ready:              false
3D validation ready:               false
GPU work ready:                    false
field FWI ready:                   false
```

The exact scaling boundary passes. Damaged cases fail for policy-count drift,
budget-count drift, recommendation policy/support drift, grid15 sample count or
readiness drift, baseline sample/savings drift, recommended L2 or margin drift,
5 mm fine-grid cost/gain drift, candidate-budget scaling drift, scaling-policy
readiness drift, half-space promotion, field transfer, 3D validation, GPU
readiness, and field-FWI readiness.

## Interpretation

Runs `221`-`223` form a guarded BEM tabulated-surface scaling budget package.
The local 2D answer is now clear: 15 mm grid-only with 11 mm shell support is
the practical low-sample policy for the tested 35 mm offset family.

## Decision

Use runs `221`-`223` as the guarded BEM tabulated-surface scaling budget
package.

Keep inversion-scale half-space BEM, analytic replacement, field transfer, 3D
validation, GPU work, and field FWI blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_tabulated_surface_scaling_budget_sensitivity.py
5 passed
```

Python compile check:

```text
run_project_core_bem_tabulated_surface_scaling_budget_sensitivity.py: pass
tests/test_project_core_bem_tabulated_surface_scaling_budget_sensitivity.py: pass
```

Figure check:

```text
3131x878, dynamic range=255
```

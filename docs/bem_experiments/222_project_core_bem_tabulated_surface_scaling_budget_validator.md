# BEM Experiment 222: Tabulated-Surface Scaling Budget Validator

Date: 2026-06-28

## Purpose

Validate the run `221` tabulated-surface scaling budget audit from a consumer
perspective.

This run does not run new FDTD/FWI, use field data, perform 3D validation,
launch GPU/HPC work, or promote inversion-scale half-space BEM.

## Output

```text
outputs/bem_experiments/222_project_core_bem_tabulated_surface_scaling_budget_validator
```

Key artifacts:

```text
data/project_core_bem_tabulated_surface_scaling_budget_validation_checks.csv
data/project_core_bem_tabulated_surface_scaling_budget_validator_summary.json
figures/project_core_bem_tabulated_surface_scaling_budget_validator.png
docs/PROJECT_CORE_BEM_TABULATED_SURFACE_SCALING_BUDGET_VALIDATOR.md
scripts/run_project_core_bem_tabulated_surface_scaling_budget_validator.py
scripts/test_project_core_bem_tabulated_surface_scaling_budget_validator.py
```

## Result

```text
validation checks:                  8
validation passes:                  8
blocking failures:                  0
validation ready:                   true
recommended policy:                 grid_15mm_only
recommended samples:                13
inversion-scale half-space ready:   false
field transfer ready:               false
3D validation ready:                false
GPU work ready:                     false
field FWI ready:                    false
```

The validator confirms the five policy rows, fifteen budget scenarios,
recommended 13-sample `grid_15mm_only` policy with `outer_shell_11mm_binary`,
positive savings against the 19-sample baseline, positive acceptance margin,
5 mm fine-grid cost/gain tradeoff, candidate-count scaling, and blocked
downstream states.

## Interpretation

The run `221` scaling budget is internally consistent. It is now positively
validated, but not yet stress-tested by negative controls.

## Decision

Use run `222` as the positive validator for the BEM tabulated-surface scaling
budget.

Run sensitivity testing before treating this scaling boundary as fully guarded.

## Validation

Focused tests:

```text
tests/test_project_core_bem_tabulated_surface_scaling_budget_validator.py
4 passed
```

Python compile check:

```text
run_project_core_bem_tabulated_surface_scaling_budget_validator.py: pass
tests/test_project_core_bem_tabulated_surface_scaling_budget_validator.py: pass
```

Figure check:

```text
2573x841, dynamic range=255
```

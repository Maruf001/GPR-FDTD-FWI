# BEM Experiment 214: Grid-15 Support-Mode Contract Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `213` support-mode contract validator with damaged contract
summaries.

This run does not run FDTD/FWI, launch GPU/HPC work, use field data, perform 3D
validation, or promote field transfer.

## Output

```text
outputs/bem_experiments/214_project_core_bem_grid15_support_mode_contract_sensitivity
```

Key artifacts:

```text
data/project_core_bem_grid15_support_mode_contract_sensitivity_scenarios.csv
data/project_core_bem_grid15_support_mode_contract_sensitivity_summary.json
figures/project_core_bem_grid15_support_mode_contract_sensitivity.png
docs/PROJECT_CORE_BEM_GRID15_SUPPORT_MODE_CONTRACT_SENSITIVITY.md
scripts/run_project_core_bem_grid15_support_mode_contract_sensitivity.py
scripts/test_project_core_bem_grid15_support_mode_contract_sensitivity.py
```

## Result

```text
scenarios:                         15
expected pass scenarios:           1
expected failure scenarios:        14
observed pass scenarios:           1
observed failure scenarios:        14
unexpected outcomes:               0
sensitivity ready:                 true
field transfer ready:              false
3D validation ready:               false
GPU work ready:                    false
field FWI ready:                   false
```

The exact support contract passes. Damaged contracts fail for the intended
checks: wrong surface policy, wrong case count, wrong sample count, only one
ready shell mode, shell-18 not ready, wrong recommended support, negative
margin, L2 above gate, volume support promoted, volume ready count drift,
per-case router required, contract not ready, field transfer ready, and GPU
ready.

## Interpretation

The support-mode contract now has both positive validation and negative-control
coverage. The guarded fixed contract is:

```text
surface policy: grid_15mm_only
support mode:   outer_shell_11mm_binary
sample count:   13
scope:          tested local 2D 35 mm offset family
```

This does not promote analytic replacement, field transfer, 3D validation,
GPU/HPC, or field FWI.

## Decision

Use runs `212`-`214` as the guarded BEM grid-15 support-mode contract.

## Validation

Focused tests:

```text
tests/test_project_core_bem_grid15_support_mode_contract_sensitivity.py
4 passed
```

Python compile check:

```text
run_project_core_bem_grid15_support_mode_contract_sensitivity.py: pass
tests/test_project_core_bem_grid15_support_mode_contract_sensitivity.py: pass
```

Figure check:

```text
3005x860, dynamic range=255
```

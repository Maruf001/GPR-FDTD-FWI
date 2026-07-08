# BEM Experiment 213: Grid-15 Support-Mode Contract Validator

Date: 2026-06-28

## Purpose

Validate the run `212` support-mode contract from a consumer perspective.

This run does not run FDTD/FWI, launch GPU/HPC work, use field data, perform 3D
validation, or promote field transfer.

## Output

```text
outputs/bem_experiments/213_project_core_bem_grid15_support_mode_contract_validator
```

Key artifacts:

```text
data/project_core_bem_grid15_support_mode_contract_validation_checks.csv
data/project_core_bem_grid15_support_mode_contract_validator_summary.json
figures/project_core_bem_grid15_support_mode_contract_validator.png
docs/PROJECT_CORE_BEM_GRID15_SUPPORT_MODE_CONTRACT_VALIDATOR.md
scripts/run_project_core_bem_grid15_support_mode_contract_validator.py
scripts/test_project_core_bem_grid15_support_mode_contract_validator.py
```

## Result

```text
validation checks:                  9
validation passes:                  9
blocking failures:                  0
validation ready:                   true
recommended support mode:           outer_shell_11mm_binary
recommended worst leave-one L2:     0.6083307089797199
field transfer ready:               false
3D validation ready:                false
GPU work ready:                     false
field FWI ready:                    false
```

The validator confirms the `grid_15mm_only` surface policy, five tested cases,
13 surface samples, two ready shell support modes, `outer_shell_11mm_binary` as
the fixed support recommendation, rejection of volume support, no per-case
router requirement, support-contract readiness, and blocked downstream states.

## Interpretation

The support-mode contract is internally consistent and ready for
negative-control sensitivity testing.

## Decision

Use run `213` as the validator for run `212`. Do not fold the support-mode
contract into refreshed BEM claim language until sensitivity testing also
passes.

## Validation

Focused tests:

```text
tests/test_project_core_bem_grid15_support_mode_contract_validator.py
4 passed
```

Python compile check:

```text
run_project_core_bem_grid15_support_mode_contract_validator.py: pass
tests/test_project_core_bem_grid15_support_mode_contract_validator.py: pass
```

Figure check:

```text
2645x841, dynamic range=255
```

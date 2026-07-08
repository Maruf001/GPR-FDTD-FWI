# BEM Experiment 216: Grid-15 Shell-11 Claim-Boundary Validator

Date: 2026-06-28

## Purpose

Validate the run `215` support-specific BEM claim-boundary refresh.

This run does not run FDTD/FWI, launch GPU/HPC work, use field data, perform 3D
validation, or promote field transfer.

## Output

```text
outputs/bem_experiments/216_project_core_bem_grid15_shell11_claim_boundary_validator
```

Key artifacts:

```text
data/project_core_bem_grid15_shell11_claim_boundary_validation_checks.csv
data/project_core_bem_grid15_shell11_claim_boundary_validator_summary.json
figures/project_core_bem_grid15_shell11_claim_boundary_validator.png
docs/PROJECT_CORE_BEM_GRID15_SHELL11_CLAIM_BOUNDARY_VALIDATOR.md
scripts/run_project_core_bem_grid15_shell11_claim_boundary_validator.py
scripts/test_project_core_bem_grid15_shell11_claim_boundary_validator.py
```

## Result

```text
validation checks:                  9
validation passes:                  9
blocking failures:                  0
validation ready:                   true
recommended policy:                 grid15_shell11_tabulated_surface_offset_repair
recommended support mode:           outer_shell_11mm_binary
field transfer ready:               false
3D validation ready:                false
GPU work ready:                     false
field FWI ready:                    false
```

The validator confirms a single recommended practical policy, correct sample
count and margin, shell-18 as a non-recommended alternative, volume support
blocked, per-case support router blocked, field transfer blocked, and downstream
field/3D/GPU/FWI states blocked.

## Interpretation

The support-specific BEM claim boundary is internally consistent and ready for
negative-control sensitivity testing.

## Decision

Use run `216` as the validator for run `215`; sensitivity remains required
before treating the support-specific claim boundary as fully guarded.

## Validation

Focused tests:

```text
tests/test_project_core_bem_grid15_shell11_claim_boundary_validator.py
4 passed
```

Python compile check:

```text
run_project_core_bem_grid15_shell11_claim_boundary_validator.py: pass
tests/test_project_core_bem_grid15_shell11_claim_boundary_validator.py: pass
```

Figure check:

```text
2645x842, dynamic range=255
```

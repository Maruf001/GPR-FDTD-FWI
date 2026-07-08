# BEM Experiment 217: Grid-15 Shell-11 Claim-Boundary Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `216` support-specific BEM claim-boundary validator with
damaged claim rows and summaries.

This run does not run FDTD/FWI, launch GPU/HPC work, use field data, perform 3D
validation, or promote field transfer.

## Output

```text
outputs/bem_experiments/217_project_core_bem_grid15_shell11_claim_boundary_sensitivity
```

Key artifacts:

```text
data/project_core_bem_grid15_shell11_claim_boundary_sensitivity_scenarios.csv
data/project_core_bem_grid15_shell11_claim_boundary_sensitivity_summary.json
figures/project_core_bem_grid15_shell11_claim_boundary_sensitivity.png
docs/PROJECT_CORE_BEM_GRID15_SHELL11_CLAIM_BOUNDARY_SENSITIVITY.md
scripts/run_project_core_bem_grid15_shell11_claim_boundary_sensitivity.py
scripts/test_project_core_bem_grid15_shell11_claim_boundary_sensitivity.py
```

## Result

```text
scenarios:                         14
expected pass scenarios:           1
expected failure scenarios:        13
observed pass scenarios:           1
observed failure scenarios:        13
unexpected outcomes:               0
sensitivity ready:                 true
field transfer ready:              false
3D validation ready:               false
GPU work ready:                    false
field FWI ready:                   false
```

The exact support-specific claim boundary passes. Damaged variants fail for the
intended reasons: claim-count drift, missing recommended policy, multiple
recommended policies, wrong support mode, negative recommended margin, shell-18
not ready, volume marked ready, volume positive margin, router marked ready,
field claim marked ready, boundary not ready, field-transfer summary ready, and
GPU summary ready.

## Interpretation

Runs `215`-`217` form a guarded support-specific BEM claim-boundary package.
The supported practical claim is:

```text
grid_15mm_only + outer_shell_11mm_binary
```

with 13 surface samples, worst leave-one L2 `0.6083307089797199`, and margin
`0.14166929102028014`, scoped to the tested local 2D 35 mm offset family.

## Decision

Use runs `215`-`217` as the guarded support-specific BEM claim-boundary package.

Do not promote analytic replacement, field transfer, 3D validation, GPU/HPC, or
field FWI.

## Validation

Focused tests:

```text
tests/test_project_core_bem_grid15_shell11_claim_boundary_sensitivity.py
4 passed
```

Python compile check:

```text
run_project_core_bem_grid15_shell11_claim_boundary_sensitivity.py: pass
tests/test_project_core_bem_grid15_shell11_claim_boundary_sensitivity.py: pass
```

Figure check:

```text
2969x861, dynamic range=255
```

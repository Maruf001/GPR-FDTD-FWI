# BEM Experiment 221: Tabulated-Surface Scaling Budget Audit

Date: 2026-06-28

## Purpose

Quantify the surface-sample budget for the guarded BEM tabulated-surface policy
from runs `203`, `206`, `212`, and `217`.

This run does not run new FDTD/FWI, use field data, perform 3D validation,
launch GPU/HPC work, or promote inversion-scale half-space BEM.

## Output

```text
outputs/bem_experiments/221_project_core_bem_tabulated_surface_scaling_budget_audit
```

Key artifacts:

```text
data/project_core_bem_tabulated_surface_scaling_policy_rows.csv
data/project_core_bem_tabulated_surface_scaling_budget_rows.csv
data/project_core_bem_tabulated_surface_scaling_budget_audit_summary.json
figures/project_core_bem_tabulated_surface_scaling_budget_audit.png
docs/PROJECT_CORE_BEM_TABULATED_SURFACE_SCALING_BUDGET_AUDIT.md
scripts/run_project_core_bem_tabulated_surface_scaling_budget_audit.py
scripts/test_project_core_bem_tabulated_surface_scaling_budget_audit.py
```

## Result

```text
policies audited:                  5
budget scenarios:                  15
offset cases:                      5
recommended policy:                grid_15mm_only
recommended support:               outer_shell_11mm_binary
recommended samples:               13
baseline policy:                   dense_10mm_plus_exact
baseline samples:                  19
sample savings vs baseline:        31.579%
recommended worst L2:              0.6083307089797199
baseline worst L2:                 0.650662226077945
recommended margin:                0.14166929102028014
5 mm samples:                      37
5 mm worst L2:                     0.5917389381889764
5 mm extra samples vs recommended: 24
5 mm L2 gain vs recommended:       0.016591770790743476
tabulated scaling policy ready:    true
inversion-scale half-space ready:  false
field transfer ready:              false
3D validation ready:               false
GPU work ready:                    false
field FWI ready:                   false
```

The 15 mm grid-only policy is the current practical tabulation point for the
tested local 2D 35 mm offset family. It reduces surface samples by 31.579%
relative to the previous 10 mm plus-exact baseline and improves the worst
leave-one L2 in the audited table.

The 5 mm grid-only table is more accurate, but it costs 37 samples instead of
13. That is 24 extra samples per candidate for a worst-case L2 gain of about
0.0166.

## Interpretation

The unresolved Green-function acceleration question now has a bounded answer
for this tested family: use the guarded 15 mm grid-only tabulated surface with
the 11 mm binary outer-shell support.

This is not an inversion-scale half-space promotion. It is a local 2D
tabulation budget result.

## Decision

Use `grid_15mm_only` with `outer_shell_11mm_binary` as the guarded scaling
policy for the tested local 2D 35 mm offset family.

Keep inversion-scale half-space BEM, analytic replacement, field transfer, 3D
validation, GPU work, and field FWI blocked from this scaling audit.

## Validation

Focused tests:

```text
tests/test_project_core_bem_tabulated_surface_scaling_budget_audit.py
4 passed
```

Python compile check:

```text
run_project_core_bem_tabulated_surface_scaling_budget_audit.py: pass
tests/test_project_core_bem_tabulated_surface_scaling_budget_audit.py: pass
```

Figure check:

```text
3076x865, dynamic range=255
```

# BEM Experiment 446: Reference-Coefficient Precision-Budget Audit

Date: 2026-06-29

## Purpose

Audit how many significant digits must be preserved for the normalized
comparator reference coefficient from the real-return scorecard template.

The upstream scorecard template uses a strict `1e-12` relative residual
tolerance. This run checks whether rounded coefficient text can fail that
tolerance before any real returned BEM/FDTD values exist.

## Output

```text
outputs/bem_experiments/446_project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_precision_budget_audit
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_precision_budget_audit_precision_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_precision_budget_audit_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_precision_budget_audit.png
```

## Result

```text
source template ready:                  true
precision budget ready:                 true
reference coefficient:                  0.01907878402833891
relative tolerance:                     1e-12
precision scenarios:                    10
passing precision scenarios:            5
failing precision scenarios:            5
minimum passing significant digits:     13
maximum failing significant digits:     12
recommended minimum significant digits: 13
real return values present:             false
real BEM/FDTD comparison ready:         false
3D validation ready:                    false
GPU/HPC ready:                          false
field FWI ready:                        false
```

The threshold is concrete: preserving 12 significant digits gives relative
coefficient error above the `1e-12` tolerance, while 13 significant digits pass.

## Decision

Preserve at least 13 significant digits for the normalized-comparator reference
coefficient in future real-return scorecards. This is a formatting and
precision guard, not real BEM/FDTD comparison evidence.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_precision_budget_audit.py
3 passed
```

Figure check:

```text
3219x880, dynamic range=255
```

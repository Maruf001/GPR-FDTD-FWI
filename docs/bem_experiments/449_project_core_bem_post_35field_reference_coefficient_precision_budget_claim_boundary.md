# BEM Experiment 449: Post-Precision-Budget Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded reference-coefficient precision-budget block from runs
`446-448` into the BEM claim boundary.

## Output

```text
outputs/bem_experiments/449_project_core_bem_post_35field_reference_coefficient_precision_budget_claim_boundary
```

Key artifacts:

```text
data/project_core_bem_post_35field_reference_coefficient_precision_budget_claim_boundary_claim_rows.csv
data/project_core_bem_post_35field_reference_coefficient_precision_budget_claim_boundary_summary.json
figures/project_core_bem_post_35field_reference_coefficient_precision_budget_claim_boundary.png
```

## Result

```text
claims:                                  27
guarded claims:                          24
blocked claims:                          3
precision budget ready:                  true
precision validation ready:              true
precision sensitivity ready:             true
reference coefficient:                   0.01907878402833891
relative tolerance:                      1e-12
precision scenarios:                     10
passing precision scenarios:             5
failing precision scenarios:             5
minimum passing significant digits:      13
maximum failing significant digits:      12
recommended minimum significant digits:  13
real BEM/FDTD comparison ready:          false
3D validation ready:                     false
GPU/HPC ready:                           false
field FWI ready:                         false
```

The new guarded claim records that future real-return scorecards must preserve
at least 13 significant digits for the normalized-comparator reference
coefficient.

## Decision

Use this as the current BEM claim boundary after the precision-budget block.
The precision rule is now part of the guarded evidence contract, but real
BEM/FDTD comparison and all downstream escalation remain blocked until real
returned values and hashes exist.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_reference_coefficient_precision_budget_claim_boundary.py
4 passed
```

Figure check:

```text
3941x899, dynamic range=255
```

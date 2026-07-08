# BEM Experiment 443: Post-Scorecard-Template Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded non-evidence real-return scorecard template from runs
`440-442` into the BEM claim boundary.

## Output

```text
outputs/bem_experiments/443_project_core_bem_post_35field_real_normalized_comparator_scorecard_template_claim_boundary
```

Key artifacts:

```text
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_template_claim_boundary_claim_rows.csv
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_template_claim_boundary_summary.json
figures/project_core_bem_post_35field_real_normalized_comparator_scorecard_template_claim_boundary.png
```

## Result

```text
claims:                             26
guarded claims:                     23
blocked claims:                     3
scorecard template ready:           true
template validation sensitivity:    true
template rows:                      279
receivers:                          31
frequencies:                        9
required real input cells:          1116
acceptance rules:                   5
template rows currently evidence:   0
real return values present:         false
real BEM/FDTD comparison ready:     false
3D validation ready:                false
GPU/HPC ready:                      false
field FWI ready:                    false
```

The new guarded claim records that the scorecard template is ready to receive
future returned values and hashes. It does not promote the template to real
comparison evidence.

## Decision

Use this as the current BEM claim boundary after the real-return
scorecard-template block. Keep real comparison, 3D validation, GPU/HPC, field
transfer, and field FWI blocked until real returned values exist.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_real_normalized_comparator_scorecard_template_claim_boundary.py
4 passed
```

Figure check:

```text
3941x909, dynamic range=255
```

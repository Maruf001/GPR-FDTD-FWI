# BEM Experiment 445: Post-Scorecard-Template Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `444` validator for the BEM post-scorecard-template claim
boundary.

## Output

```text
outputs/bem_experiments/445_project_core_bem_post_35field_real_normalized_comparator_scorecard_template_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_template_claim_boundary_validation_sensitivity_scenario_rows.csv
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_template_claim_boundary_validation_sensitivity_summary.json
figures/project_core_bem_post_35field_real_normalized_comparator_scorecard_template_claim_boundary_validation_sensitivity.png
```

## Result

```text
scenarios:                          29
expected pass scenarios:            1
observed pass scenarios:            1
expected failure scenarios:         28
observed failure scenarios:         28
unexpected outcomes:                0
validation sensitivity ready:       true
validator accepts exact run 443:    true
validator rejects damaged variants: true
real return values present:         false
real BEM/FDTD comparison ready:     false
3D validation ready:                false
GPU/HPC ready:                      false
field FWI ready:                    false
```

The damaged variants cover claim-count drift, missing or altered
scorecard-template claims, metric drift, evidence promotion, downstream
promotion, blocked-row support drift, blank figures, and missing script
snapshots.

## Decision

Use runs `443-445` as the current guarded BEM post-scorecard-template
claim-boundary block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_real_normalized_comparator_scorecard_template_claim_boundary.py
tests/test_project_core_bem_post_35field_real_normalized_comparator_scorecard_template_claim_boundary_validator.py
tests/test_project_core_bem_post_35field_real_normalized_comparator_scorecard_template_claim_boundary_validation_sensitivity.py
12 passed
```

Figure check:

```text
3581x879, dynamic range=255
```

# BEM Experiment 499: Post Real Return-File Filesystem Gap-Audit Claim-Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `498` validator against controlled damage to the run `497`
claim boundary.

## Output

```text
outputs/bem_experiments/499_project_core_bem_post_35field_real_normalized_comparator_scorecard_real_return_filesystem_gap_audit_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_real_return_filesystem_gap_audit_claim_boundary_validation_sensitivity_scenario_rows.csv
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_real_return_filesystem_gap_audit_claim_boundary_validation_sensitivity_summary.json
figures/project_core_bem_post_35field_real_normalized_comparator_scorecard_real_return_filesystem_gap_audit_claim_boundary_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                       27
expected pass scenarios:                     1
observed pass scenarios:                     1
expected failure scenarios:                  26
observed failure scenarios:                  26
unexpected outcomes:                         0
validation sensitivity ready:                true
validator accepts exact run 497:             true
validator rejects damaged variants:          true
real return files present:                   false
real return packet accepted:                 false
real BEM/FDTD comparison ready:              false
```

The damaged variants cover claim-count drift, claim-support drift, filesystem
metric drift, accepted-real-count promotion, downstream promotion, figure
damage, and script-snapshot damage.

## Decision

Use runs `497-499` as the guarded post-filesystem-gap BEM claim-boundary block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_real_normalized_comparator_scorecard_real_return_filesystem_gap_audit_claim_boundary_validation_sensitivity.py
3 passed
```

Figure check:

```text
3689x918, dynamic range=255
```

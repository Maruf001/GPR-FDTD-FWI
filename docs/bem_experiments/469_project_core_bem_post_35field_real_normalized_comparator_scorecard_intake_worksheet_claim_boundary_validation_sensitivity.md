# BEM Experiment 469: Post-Scorecard Intake Worksheet Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `468` validator with controlled damage to claim counts,
worksheet readiness, worksheet metrics, claim support, downstream states,
figure validation, and script snapshots.

## Output

```text
outputs/bem_experiments/469_project_core_bem_post_35field_real_normalized_comparator_scorecard_intake_worksheet_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_intake_worksheet_claim_boundary_validation_sensitivity_scenario_rows.csv
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_intake_worksheet_claim_boundary_validation_sensitivity_summary.json
figures/project_core_bem_post_35field_real_normalized_comparator_scorecard_intake_worksheet_claim_boundary_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                       38
expected passes:                             1
observed passes:                             1
expected failures:                           37
observed failures:                           37
unexpected outcomes:                         0
validation sensitivity ready:                true
validator accepts exact run 467:             true
validator rejects damaged variants:          true
real return values present:                  false
real BEM/FDTD comparison ready:              false
3D validation ready:                         false
GPU/HPC ready:                               false
field FWI ready:                             false
```

## Decision

Use runs `467-469` as the current guarded BEM post-intake-worksheet
claim-boundary block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_real_normalized_comparator_scorecard_intake_worksheet_claim_boundary_validation_sensitivity.py
3 passed
```

Figure check:

```text
3581x885, dynamic range=255
```

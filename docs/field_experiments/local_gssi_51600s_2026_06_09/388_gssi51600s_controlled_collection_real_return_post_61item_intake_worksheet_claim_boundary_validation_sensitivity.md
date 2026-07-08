# Field Experiment 388: Post-Intake-Worksheet Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `387` validator for the post-intake-worksheet field claim
boundary.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/388_gssi51600s_controlled_collection_real_return_post_61item_intake_worksheet_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_intake_worksheet_claim_boundary_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_post_61item_intake_worksheet_claim_boundary_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_intake_worksheet_claim_boundary_validation_sensitivity.png
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
validator accepts exact run 386:    true
validator rejects damaged variants: true
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

The damaged variants cover claim-count drift, intake-claim support drift,
worksheet metric drift, completed-row and evidence-row promotion, downstream
promotion, figure drift, and script-snapshot drift.

## Decision

Use runs `386-388` as the current guarded field post-intake-worksheet
claim-boundary block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_intake_worksheet_claim_boundary.py
tests/test_gssi_field_controlled_collection_real_return_post_61item_intake_worksheet_claim_boundary_validator.py
tests/test_gssi_field_controlled_collection_real_return_post_61item_intake_worksheet_claim_boundary_validation_sensitivity.py
12 passed
```

Figure check:

```text
3581x878, dynamic range=255
```

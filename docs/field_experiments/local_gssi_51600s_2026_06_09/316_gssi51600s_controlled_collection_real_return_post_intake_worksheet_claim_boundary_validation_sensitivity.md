# Field Experiment 316: Real-Return Post-Intake Worksheet Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `315` field post-intake claim-boundary validator with
controlled damaged variants.

This run checks that the validator accepts the exact run `314` boundary and
rejects damaged variants covering source identity drift, claim-count drift,
intake-worksheet claim drift, worksheet-metric drift, blocked-row drift,
downstream promotion, GPU-priority drift, figure drift, and script-snapshot
drift.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/316_gssi51600s_controlled_collection_real_return_post_intake_worksheet_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_intake_worksheet_claim_boundary_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_post_intake_worksheet_claim_boundary_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_post_intake_worksheet_claim_boundary_validation_sensitivity.png
scripts/
```

## Result

```text
scenarios:                         11
expected pass:                     1
observed pass:                     1
expected failures:                 10
observed failures:                 10
unexpected outcomes:               0
sensitivity ready:                 true
accepts exact run 314:             true
rejects damaged variants:          true
real packet files present:         false
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

## Interpretation

The run `315` validator accepts the exact run `314` field boundary and rejects
controlled damaged variants. This protects the post-intake boundary from claim
count drift, worksheet promotion, downstream field promotion, and missing
validation artifacts.

## Decision

Use runs `314-316` as the guarded field post-intake claim-boundary block. Field
evidence, field FWI, GPU work, and field 3D/HPC remain blocked until real
measured packet files pass the acceptance gate.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_intake_worksheet_claim_boundary_validation_sensitivity.py
2 passed
```

Figure validation:

```text
3365x909, dynamic range=255
```

# Field Experiment 322: Post Staging Dependency Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `321` validator for the saved run `320` field post-staging
dependency claim boundary.

This run checks that the validator accepts the exact run `320` artifacts and
rejects controlled damaged variants for claim drift, staging row drift, staging
metric drift, blocked-row drift, field-state promotion, GPU-priority drift,
figure drift, and script-snapshot drift.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/322_gssi51600s_controlled_collection_real_return_post_staging_dependency_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_staging_dependency_claim_boundary_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_post_staging_dependency_claim_boundary_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_post_staging_dependency_claim_boundary_validation_sensitivity.png
scripts/
```

## Result

```text
scenarios:                          14
expected pass:                      1
observed pass:                      1
expected failures:                  13
observed failures:                  13
unexpected outcomes:                0
sensitivity ready:                  true
accepts exact run 320:              true
rejects damaged variants:           true
stages:                             7
dependency edges:                   9
missing packet items:               57
real packet files present:          false
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

## Interpretation

The run `321` validator accepts the exact run `320` claim boundary and rejects
controlled damaged variants. This guards the field post-staging claim-boundary
result while preserving the main blocker: the 57-item measured return packet is
still absent.

## Decision

Use runs `320-322` as the guarded field post-staging claim-boundary block.
Field evidence remains blocked until the 57-item measured packet is present
and passes the acceptance gate.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_staging_dependency_claim_boundary_validation_sensitivity.py
3 passed
```

Figure validation:

```text
3581x904, dynamic range=255
```

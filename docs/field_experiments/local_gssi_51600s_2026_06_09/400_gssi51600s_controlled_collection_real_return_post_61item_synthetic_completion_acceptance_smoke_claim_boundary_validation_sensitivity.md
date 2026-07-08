# Field Experiment 400: Post-Synthetic Completion Smoke Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `399` validator against controlled damage to the run `398`
field claim boundary.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/400_gssi51600s_controlled_collection_real_return_post_61item_synthetic_completion_acceptance_smoke_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_synthetic_completion_acceptance_smoke_claim_boundary_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_post_61item_synthetic_completion_acceptance_smoke_claim_boundary_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_synthetic_completion_acceptance_smoke_claim_boundary_validation_sensitivity.png
```

## Result

```text
sensitivity scenarios:                  30
expected pass scenarios:                 1
observed pass scenarios:                 1
expected failure scenarios:              29
observed failure scenarios:              29
unexpected outcomes:                     0
validation sensitivity ready:            true
validator accepts exact run 398:         true
validator rejects damaged variants:      true
synthetic only:                          true
real packet files present:               false
provenance acceptance ready:             false
archive acceptance ready:                false
controlled field evidence ready:         false
field FWI ready:                         false
field 3D/HPC ready:                      false
gpu priority:                            none
```

The damaged variants cover claim-count drift, synthetic-smoke readiness drift,
metric drift, claim-support drift, downstream promotion, figure drift, and
missing script snapshots. The exact run `398` passes and all damaged variants
fail as expected.

## Decision

Use runs `398-400` as the current guarded field post-synthetic-acceptance
claim-boundary block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_synthetic_completion_acceptance_smoke_claim_boundary_validation_sensitivity.py
3 passed
```

Figure check:

```text
3581x886, dynamic range=255
```

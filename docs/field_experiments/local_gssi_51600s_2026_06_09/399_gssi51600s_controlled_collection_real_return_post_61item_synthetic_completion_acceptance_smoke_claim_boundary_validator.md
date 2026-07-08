# Field Experiment 399: Post-Synthetic Completion Smoke Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `398` post-synthetic-completion-smoke field claim
boundary from disk.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/399_gssi51600s_controlled_collection_real_return_post_61item_synthetic_completion_acceptance_smoke_claim_boundary_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_synthetic_completion_acceptance_smoke_claim_boundary_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_post_61item_synthetic_completion_acceptance_smoke_claim_boundary_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_synthetic_completion_acceptance_smoke_claim_boundary_validator.png
```

## Result

```text
validation checks:                       5
validation checks passed:                5
blocking failures:                       0
claim-boundary validation ready:         true
claims:                                  24
guarded claims:                          20
blocked claims:                          4
synthetic acceptance smoke ready:        true
synthetic parser accepted rows:          49
synthetic measured-evidence rows:        0
synthetic only:                          true
real packet files present:               false
provenance acceptance ready:             false
archive acceptance ready:                false
controlled field evidence ready:         false
field FWI ready:                         false
field 3D/HPC ready:                      false
gpu priority:                            none
```

The validator confirms the saved claim counts, synthetic acceptance-path
claim, metrics, downstream blocked states, figure, and script snapshots.

## Decision

Use this validator as the artifact guard for run `398`.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_synthetic_completion_acceptance_smoke_claim_boundary_validator.py
5 passed
```

Figure check:

```text
2645x839, dynamic range=255
```

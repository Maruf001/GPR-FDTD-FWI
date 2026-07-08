# Field Experiment 381: Post Operator-Handoff Claim-Boundary Validator

Date: 2026-06-29

## Purpose

Validate run `380` from saved artifacts.

The validator checks claim counts, handoff-claim support, handoff metrics,
blocked rows, downstream states, figure validation, and script snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/381_gssi51600s_controlled_collection_real_return_post_61item_operator_handoff_manifest_claim_boundary_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_operator_handoff_manifest_claim_boundary_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_post_61item_operator_handoff_manifest_claim_boundary_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_operator_handoff_manifest_claim_boundary_validator.png
```

## Result

```text
validation checks:                 5
validation passes:                 5
blocking failures:                 0
handoff-boundary validation ready: true
claims:                            21
guarded claims:                    17
blocked claims:                    4
handoff rows:                      49
direct operator items:             33
generated follow-up items:         16
packet requirements:               61
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
GPU priority:                      none
```

## Decision

Use this validator as the artifact guard for run `380`. Sensitivity testing
remains required before closing the post-handoff claim-boundary block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_operator_handoff_manifest_claim_boundary_validator.py
5 passed as part of the 12-test focused set
```

Figure check:

```text
2645x839, dynamic range=255
```

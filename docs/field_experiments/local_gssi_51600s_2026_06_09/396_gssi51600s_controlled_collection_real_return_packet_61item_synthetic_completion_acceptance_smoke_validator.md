# Field Experiment 396: Synthetic Completion Acceptance Smoke Validator

Date: 2026-06-29

## Purpose

Validate the saved run `395` synthetic completion-smoke artifacts from disk.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/396_gssi51600s_controlled_collection_real_return_packet_61item_synthetic_completion_acceptance_smoke_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_completion_acceptance_smoke_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_completion_acceptance_smoke_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_completion_acceptance_smoke_validator.png
```

## Result

```text
validation checks:                       5
validation checks passed:                5
blocking failures:                       0
synthetic smoke validation ready:        true
filled rows:                             49
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

The validator confirms the saved row counts, source blank non-evidence state,
synthetic completion syntax, downstream blocked states, figure, and script
snapshots.

## Decision

Use this validator as the artifact guard for run `395`.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_synthetic_completion_acceptance_smoke_validator.py
4 passed
```

Figure check:

```text
2645x839, dynamic range=255
```

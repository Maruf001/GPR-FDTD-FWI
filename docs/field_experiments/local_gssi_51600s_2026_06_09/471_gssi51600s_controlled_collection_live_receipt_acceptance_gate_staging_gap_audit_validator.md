# Field Experiment 471: Live Receipt Acceptance Gate Staging Gap Audit Validator

Date: 2026-06-30

## Purpose

Validate the run `470` live staging-gap audit from saved artifacts.

This run checks source-chain readiness, staging-directory shape, missing-file
state, family-level gap state, action/downstream blocking, and figure/script
artifacts.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/471_gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_audit_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_audit_validator_check_rows.csv
data/gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_audit_validator_summary.json
figures/gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_audit_validator.png
scripts/
```

## Result

```text
validation checks:                        6
passed checks:                            6
failed checks:                            0
required files:                           33
missing files:                            33
staging directories:                      5
families:                                 5
actions:                                  4
parser ready:                             false
provenance ready:                         false
archive ready:                            false
controlled field evidence ready:          false
field FWI ready:                          false
field 3D/HPC ready:                       false
gpu priority:                             none
```

The six validation checks all pass:

```text
source chain ready
staging directory shape
required files absent
family gap shape
actions and downstream blocked
figure and scripts exist
```

## Interpretation

The current field staging-gap audit is valid. The run confirms that the field
staging directories are ready for a data drop, but all 33 required receipt
files remain absent.

## Decision

Use run `471` as the artifact guard for the current live field staging state.
Do not rerun parser, provenance, archive, field FWI, or field 3D/HPC until real
receipt files exist and pass the verifier.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_acceptance_gate_staging_gap_audit.py
tests/test_gssi_field_controlled_collection_live_receipt_acceptance_gate_staging_gap_audit_validator.py

7 passed
```

Figure validation:

```text
2285x842, dynamic range=255
```

# Field Experiment 312: Real-Return Packet Intake Worksheet Validator

Date: 2026-06-29

## Purpose

Validate the saved run `311` field return-packet intake worksheet from
artifacts.

The validator checks worksheet counts, directory coverage, action-group
coverage, template non-evidence status, blocked measured-packet state,
downstream field guardrails, figure validation, and script snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/312_gssi51600s_controlled_collection_real_return_packet_intake_worksheet_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_intake_worksheet_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_packet_intake_worksheet_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_intake_worksheet_validator.png
scripts/
```

## Result

```text
validation checks:                   7
passed checks:                       7
failed checks:                       0
validation ready:                    true
packet items:                        57
measured DZT files:                  9
metadata requirements:               32
checksum rows:                       9
acceptance results:                  7
template files:                      58
real packet files present:           false
missing packet items:                57
provenance acceptance ready:         false
controlled field evidence ready:     false
field FWI ready:                     false
field 3D/HPC ready:                  false
gpu priority:                        none
```

## Interpretation

The saved field intake worksheet is internally consistent and remains
non-evidence: templates are present, but measured packet items are still
absent.

## Decision

Use run `312` as the validator for the run `311` field intake worksheet.
Provenance and field evidence remain blocked until measured packet files pass
the acceptance gate.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_intake_worksheet_validator.py
3 passed
```

Figure validation:

```text
3545x929, dynamic range=255
```

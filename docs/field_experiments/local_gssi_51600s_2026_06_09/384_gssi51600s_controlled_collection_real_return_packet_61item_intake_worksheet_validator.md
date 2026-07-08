# Field Experiment 384: Controlled Collection Real-Return Intake Worksheet Validator

Date: 2026-06-29

## Purpose

Validate the blank, non-evidence intake worksheet from run `383`.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/384_gssi51600s_controlled_collection_real_return_packet_61item_intake_worksheet_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_intake_worksheet_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_intake_worksheet_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_intake_worksheet_validator.png
```

## Result

```text
validation checks:                  6
validation checks passed:           6
blocking failures:                  0
intake worksheet validation ready:  true
worksheet rows:                     49
direct real-input rows:             33
generated follow-up rows:           16
blank completion cells:             294
completed intake rows:              0
measured-evidence rows:             0
collection-day intake form ready:   true
real packet files present:          false
provenance acceptance ready:        false
real archive acceptance ready:      false
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

The validator checks worksheet shape, blank completion fields, packet type
counts, default direct/generated statuses, downstream blocks, and figure/script
snapshots.

## Decision

Use this validator as the artifact guard for run `383`.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_intake_worksheet.py
tests/test_gssi_field_controlled_collection_real_return_packet_61item_intake_worksheet_validator.py
8 passed
```

Figure check:

```text
2645x866, dynamic range=255
```

# Field Experiment 470: Live Receipt Acceptance Gate Staging Gap Audit

Date: 2026-06-30

## Purpose

Audit the current live staging tree after the guarded live receipt acceptance
gate in runs `467-469`.

This run checks the existing external staging tree against the 33-file
collection-day bundle. It does not create, copy, or modify field files.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/470_gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_audit
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_audit_file_rows.csv
data/gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_audit_directory_rows.csv
data/gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_audit_family_rows.csv
data/gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_audit_action_rows.csv
data/gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_audit_summary.json
figures/gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_audit.png
scripts/
```

## Result

```text
source gate ready:                        true
source validation ready:                  true
source sensitivity ready:                 true
source bundle ready:                      true
staging directories:                      5
present staging directories:              5
unexpected files:                         0
required files:                           33
DZT files required:                       9
metadata JSON files required:             24
present files:                            0
nonempty files:                           0
JSON parse-ready files:                   0
SHA-256-ready files:                      0
receipt-ready files:                      0
missing files:                            33
missing DZT files:                        9
missing metadata JSON files:              24
families:                                 5
ready families:                           0
actions:                                  4
ready actions:                            0
parser ready:                             false
provenance ready:                         false
archive ready:                            false
controlled field evidence ready:          false
field FWI ready:                          false
field 3D/HPC ready:                       false
gpu priority:                             none
```

The five live staging directories are present:

```text
metadata/files
metadata/global
real_return/amplitude_reference
real_return/controlled_profile_repeat
real_return/time_zero_reference
```

## Interpretation

The field-side blocker is now confirmed against the current live staging tree,
not only against the earlier receipt manifest. The directories are ready for a
field-data drop, but no measured DZT files or completed metadata JSON files are
present.

## Decision

Keep parser reruns, provenance acceptance, archive acceptance, controlled field
evidence, field FWI, and field 3D/HPC blocked until all 33 live receipt files
exist and pass the receipt verifier.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_acceptance_gate.py
tests/test_gssi_field_controlled_collection_live_receipt_acceptance_gate_validator.py
tests/test_gssi_field_controlled_collection_live_receipt_acceptance_gate_validation_sensitivity.py
tests/test_gssi_field_controlled_collection_live_receipt_acceptance_gate_staging_gap_audit.py

14 passed
```

Figure validation:

```text
2465x846, dynamic range=255
```

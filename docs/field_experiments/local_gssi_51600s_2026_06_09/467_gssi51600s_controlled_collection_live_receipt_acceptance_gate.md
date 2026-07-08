# Field Experiment 467: Live Receipt Acceptance Gate

Date: 2026-06-30

## Purpose

Define the acceptance gate for the live receipt verifier.

Runs `464-466` showed that the verifier works and that the current live field
staging area still has zero of the 33 required files. This run converts that
state into a family-level gate:

```text
What must pass before parser, provenance, archive, field FWI, or field 3D/HPC
work can be rerun?
```

This is a gate and current-state audit. It does not copy field files, create
synthetic receipts, rerun the parser, rerun provenance, build an archive, run
field FWI, or start field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/467_gssi51600s_controlled_collection_live_receipt_acceptance_gate
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_acceptance_gate_family_gate_rows.csv
data/gssi51600s_controlled_collection_live_receipt_acceptance_gate_acceptance_check_rows.csv
data/gssi51600s_controlled_collection_live_receipt_acceptance_gate_action_rows.csv
data/gssi51600s_controlled_collection_live_receipt_acceptance_gate_summary.json
figures/gssi51600s_controlled_collection_live_receipt_acceptance_gate.png
scripts/
```

## Result

```text
source audit ready:                  true
source sensitivity ready:            true
receipt families:                    5
required receipts:                   33
DZT receipts:                        9
metadata JSON receipts:              24
required receipt checks:             183
present live files:                  0
nonempty live files:                 0
metadata JSON parse-ready files:     0
SHA-256-ready files:                 0
receipt-ready rows:                  0
accepted families:                   0
acceptance checks:                   6
ready acceptance checks:             0
ready to rerun parser:               false
parser ready:                        false
provenance ready:                    false
archive ready:                       false
controlled field evidence ready:     false
field FWI ready:                     false
field 3D/HPC ready:                  false
```

The five receipt families are:

| Family | File type | Required files | Required checks | Receipt-ready files |
| --- | --- | ---: | ---: | ---: |
| `amplitude_reference` | DZT | 3 | 18 | 0 |
| `controlled_profile_repeat` | DZT | 3 | 18 | 0 |
| `time_zero_reference` | DZT | 3 | 18 | 0 |
| `global_metadata` | metadata JSON | 15 | 75 | 0 |
| `per_file_metadata` | metadata JSON | 9 | 54 | 0 |

## Interpretation

The field-side blocker is now a strict receipt gate, not an ambiguous readiness
state. All 33 locked receipt paths must contain real files; all files must be
nonempty; all 24 metadata JSON files must parse; all rows must have nonempty
SHA-256 hashes; and all 33 receipt rows must pass before parser, provenance,
archive, field FWI, or field 3D/HPC work can proceed.

## Decision

Use run `467` as the live field receipt acceptance gate. Do not rerun parser,
provenance, archive, field FWI, GPU work, or field 3D/HPC until the gate reports
33 receipt-ready rows.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_verifier.py
tests/test_gssi_field_controlled_collection_live_receipt_verifier_current_state_audit.py
tests/test_gssi_field_controlled_collection_live_receipt_verifier_current_state_validator.py
tests/test_gssi_field_controlled_collection_live_receipt_verifier_current_state_validation_sensitivity.py
tests/test_gssi_field_controlled_collection_live_receipt_acceptance_gate.py

18 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```

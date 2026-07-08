# Field Experiment 468: Live Receipt Acceptance Gate Validator

Date: 2026-06-30

## Purpose

Validate run `467` from saved artifacts.

This run confirms that the live receipt acceptance gate has the expected family
shape, acceptance-check shape, zero current accepted receipts, and blocked
downstream states.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/468_gssi51600s_controlled_collection_live_receipt_acceptance_gate_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_acceptance_gate_validator_check_rows.csv
data/gssi51600s_controlled_collection_live_receipt_acceptance_gate_validator_summary.json
figures/gssi51600s_controlled_collection_live_receipt_acceptance_gate_validator.png
scripts/
```

## Result

```text
source gate ready:                  true
validation checks:                  6
failed checks:                      0
receipt families:                   5
required receipts:                  33
required receipt checks:            183
present live files:                 0
receipt-ready rows:                 0
accepted families:                  0
ready to rerun parser:              false
parser ready:                       false
provenance ready:                   false
archive ready:                      false
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
```

The six checks validate source readiness, five-family/33-file shape, six
acceptance checks, zero current live receipts, blocked actions/downstream
states, and figure/script artifacts.

## Interpretation

Run `467` is a valid field receipt gate. It preserves the current decision:
there is no controlled field evidence yet because no live receipt files are
present or accepted.

## Decision

Do not rerun parser, provenance, archive, field FWI, GPU work, or field 3D/HPC
until all 33 receipt rows pass the live receipt verifier.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_acceptance_gate.py
tests/test_gssi_field_controlled_collection_live_receipt_acceptance_gate_validator.py

7 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```

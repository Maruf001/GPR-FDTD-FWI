# Field Experiment 540: Measured DZT Live Receipt Signature Gate Validator

Date: 2026-07-01

## Purpose

Validate run `539` as a fail-closed measured-DZT live receipt boundary.

This run is validation only. It does not create or stage DZT files, run
parsers, rerun provenance/archive gates, run field FWI, run field 3D/HPC,
launch GPU work, or train neural networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/540_gssi51600s_controlled_collection_measured_dzt_live_receipt_signature_gate_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_measured_dzt_live_receipt_signature_gate_validator_check_rows.csv
data/gssi51600s_controlled_collection_measured_dzt_live_receipt_signature_gate_validator_summary.json
figures/gssi51600s_controlled_collection_measured_dzt_live_receipt_signature_gate_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                         7
passed checks:                  7
failed checks:                  0
DZT slots:                      9
DZT minimum size bytes:         65536
GSSI DZT header prefix hex:     ff07
live DZT files present:         0
live DZT signature passes:      0
live DZT SHA-256 hashes:        0
live receipt ready:             false
field FWI ready:                false
field 3D/HPC ready:             false
validation ready:               true
```

Validation checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source signature gate ready | pass |
| 2 | gate shape | pass |
| 3 | DZT guard contract | pass |
| 4 | live DZT files absent | pass |
| 5 | families and actions blocked | pass |
| 6 | downstream remains blocked | pass |
| 7 | figure and scripts exist | pass |

## Interpretation

The validator confirms that run `539` is a current receipt boundary, not a
field-evidence promotion. It verifies the nine-slot shape, exact DZT binary
guard, empty live-file state, blocked action/family completion, and blocked
downstream field work.

## Decision

Keep run `539` as the current live-DZT receipt gate. Do not promote receipt or
downstream field work until real measured files pass the binary guard.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_measured_dzt_live_receipt_signature_gate_validator.py
3 passed
```

Figure check:

```text
2285x858, dynamic range=255
```

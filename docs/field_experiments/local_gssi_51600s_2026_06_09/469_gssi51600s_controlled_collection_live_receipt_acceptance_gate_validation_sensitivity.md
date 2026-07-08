# Field Experiment 469: Live Receipt Acceptance Gate Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `468` validator with controlled damage to the run `467`
receipt-gate artifacts.

This run checks that the validator fails when receipt families, receipt
readiness, parser readiness, field FWI readiness, action readiness, figures, or
script snapshots are damaged.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/469_gssi51600s_controlled_collection_live_receipt_acceptance_gate_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_acceptance_gate_validation_sensitivity_cases.csv
data/gssi51600s_controlled_collection_live_receipt_acceptance_gate_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_live_receipt_acceptance_gate_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:              true
sensitivity cases:                   11
expected pass cases:                 1
expected fail cases:                 10
actual pass cases:                   1
actual fail cases:                   10
unexpected cases:                    0
damaged cases:                       10
ready to rerun parser:               false
parser ready:                        false
provenance ready:                    false
archive ready:                       false
controlled field evidence ready:     false
field FWI ready:                     false
field 3D/HPC ready:                  false
```

The exact source state passes. Damaged states fail for:

```text
source readiness removal
receipt-family removal
receipt-family acceptance promotion
acceptance-check removal
live receipt promotion
parser readiness promotion
field FWI readiness promotion
field action readiness promotion
missing figure
missing script snapshots
```

## Interpretation

The live receipt acceptance-gate validator is sensitive to the intended failure
modes. It does not allow partial receipt presence, action readiness, parser
promotion, field FWI promotion, or damaged artifacts to become field evidence.

## Decision

Keep parser, provenance, archive, controlled field evidence, field FWI, GPU
work, and field 3D/HPC blocked until all 33 live receipt rows pass.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_acceptance_gate_validation_sensitivity.py

3 passed
```

Field receipt-gate slice:

```text
tests/test_gssi_field_controlled_collection_live_receipt_acceptance_gate.py
tests/test_gssi_field_controlled_collection_live_receipt_acceptance_gate_validator.py
tests/test_gssi_field_controlled_collection_live_receipt_acceptance_gate_validation_sensitivity.py

10 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```

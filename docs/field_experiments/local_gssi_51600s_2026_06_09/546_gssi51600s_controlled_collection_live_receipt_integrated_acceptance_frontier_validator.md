# Field Experiment 546: Integrated Live Receipt Acceptance Frontier Validator

Date: 2026-07-01

## Purpose

Validate run `545` from saved artifacts.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/546_gssi51600s_controlled_collection_live_receipt_integrated_acceptance_frontier_validator
```

## Result

```text
checks:                           8
passed:                           8
failed:                           0
live receipt items required:       33
measured DZT slots:                9
metadata JSON slots:               24
required metadata value fields:    96
accepted live receipt items:       0
complete actions:                  0
live receipt ready:                false
field FWI ready:                   false
field 3D/HPC ready:                false
```

## Decision

Run `545` is valid as the integrated field live-receipt frontier. All
downstream field processing remains blocked.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_integrated_acceptance_frontier_validator.py
3 passed
```


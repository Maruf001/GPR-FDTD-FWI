# Field Experiment 547: Integrated Live Receipt Acceptance Frontier Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `546` validator.

The damaged cases cover missing groups, missing actions, count drift, false DZT
signature passes, false metadata schema passes, false accepted live items,
false complete actions, false receipt/parser/FWI/3D promotion, blank figure
output, and missing script snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/547_gssi51600s_controlled_collection_live_receipt_integrated_acceptance_frontier_validation_sensitivity
```

## Result

```text
cases:                            17
expected pass:                    1
expected fail:                    16
actual pass:                      1
actual fail:                      16
unexpected outcomes:              0
live receipt ready:               false
parser ready:                     false
field FWI ready:                  false
field 3D/HPC ready:               false
```

## Decision

Runs `545-547` are the guarded integrated field live-receipt frontier. The
validator rejects damaged receipt accounting and false downstream promotion.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_integrated_acceptance_frontier_validation_sensitivity.py
3 passed
```


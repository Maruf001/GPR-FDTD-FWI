# Field Experiment 489: Controlled Collection Live Receipt Collection-Day Route Incremental Acceptance Frontier Validator

Date: 2026-06-30

## Purpose

Validate run `488` from saved artifacts.

This run checks the family table, the 32-scenario frontier table, the
all-family-only completion rule, the current live-file blocker, and the
figure/script artifacts.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/489_gssi51600s_controlled_collection_live_receipt_collection_day_route_incremental_acceptance_frontier_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_incremental_acceptance_frontier_validator_check_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_incremental_acceptance_frontier_validator_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_route_incremental_acceptance_frontier_validator.png
scripts/
```

## Result

```text
checks:                               5
passed checks:                        5
failed checks:                        0
file families:                        5
family-completion scenarios:          32
partial scenarios:                    30
receipt-complete scenarios:           1
partial receipt-complete scenarios:   0
total required files:                 33
total required receipt checks:        183
minimum families for completion:      5
current live files present:           0
current live receipt-ready files:     0
controlled field evidence ready:      false
field FWI ready:                      false
field 3D/HPC ready:                   false
gpu priority:                         none
```

The five checks cover source readiness, family table shape, frontier table
shape, blocked current live/downstream state, and figure/script artifacts.

## Interpretation

Run `488` is a valid family-completion frontier. The saved artifacts support
the collection-day rule that only the all-family case closes the conservative
receipt gate.

## Decision

Use run `489` as the artifact validator for run `488`.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_route_incremental_acceptance_frontier_validator.py

3 passed
```

Figure validation:

```text
2285x839, dynamic range=255
```

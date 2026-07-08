# Field Experiment 641: First-Return Acceptance Rerun Decision Gate Validator

Date: 2026-07-02

## Purpose

Validate the run `640` decision gate from saved artifacts.

This run checks that the no-file receipt state defers the acceptance-gate
rerun, preserves the two blocking prerequisites, and keeps field evidence,
field FWI, field 3D/HPC, and GPU-priority promotion closed.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/641_gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_acceptance_rerun_decision_gate_validator
```

## Result

```text
validation checks:                     6
passed checks:                         6
failed checks:                         0
receipt rows:                          18
unique measured pairs:                 9
live files found:                      0
missing files:                         18
observed SHA-256 values:               0
observed file-size values:             0
ready for acceptance-gate rerun:       0
blocking decision checks:              2
acceptance-gate rerun needed:          false
acceptance-gate rerun authorized now:  false
controlled field evidence ready:       false
field FWI ready:                       false
field 3D/HPC ready:                    false
gpu priority:                          none
```

## Interpretation

The decision gate validates as a closed, no-rerun state. The acceptance gate is
not authorized because no live files or receipt observations exist.

## Decision

Keep the first-return acceptance rerun closed until all expected receipt
observations are populated.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_receipt_live_state_refresh.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_receipt_live_state_refresh_validator.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_receipt_live_state_refresh_validation_sensitivity.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_acceptance_rerun_decision_gate.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_acceptance_rerun_decision_gate_validator.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_acceptance_rerun_decision_gate_validation_sensitivity.py
24 passed
```

Figure check:

```text
2717x866, dynamic range=255
```

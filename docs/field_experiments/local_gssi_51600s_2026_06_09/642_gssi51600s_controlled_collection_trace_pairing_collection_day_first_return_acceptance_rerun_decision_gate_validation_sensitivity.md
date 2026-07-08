# Field Experiment 642: First-Return Acceptance Rerun Decision Gate Validation Sensitivity

Date: 2026-07-02

## Purpose

Stress-test the run `641` decision-gate validator.

This run verifies that the validator accepts only the exact no-file/no-rerun
decision state and rejects damaged or prematurely promoted states.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/642_gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_acceptance_rerun_decision_gate_validation_sensitivity
```

## Result

```text
source validator ready:                true
scenarios:                             24
expected pass scenarios:               1
expected fail scenarios:               23
observed pass scenarios:               1
observed fail scenarios:               23
unexpected outcomes:                   0
damaged scenarios:                     23
damaged scenarios rejected:            23
live files found:                      0
missing files:                         18
blocking decision checks:              2
acceptance-gate rerun needed:          false
acceptance-gate rerun authorized now:  false
controlled field evidence ready:       false
field FWI ready:                       false
field 3D/HPC ready:                    false
gpu priority:                          none
```

Rejected damaged states include:

```text
decision-not-ready state
source-refresh-not-ready state
decision-row removal
required-count damage
passed-required-count damage
blocking-count damage
false live-file promotion
observed hash promotion
observed size promotion
metadata-parse promotion
DZT signature-candidate promotion
ready-row promotion
acceptance-rerun-needed promotion
acceptance-rerun-authorized promotion
acceptance command promotion
next-action promotion
accepted-row promotion
field-evidence promotion
field FWI promotion
field 3D/HPC promotion
GPU-priority promotion
figure damage
script-snapshot damage
```

## Interpretation

The decision-gate validator is fail-closed. It rejects false receipt
completion, false acceptance-rerun authorization, and downstream compute or
field-evidence promotion.

## Decision

Use runs `640-642` as the guarded no-rerun block before any first-return
acceptance-gate launch. Keep field evidence, field FWI, and field 3D/HPC
blocked until real files are returned and the full receipt path passes.

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
3401x915, dynamic range=255
```

# Field Experiment 639: First-Return Receipt Live-State Refresh Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `638` live-state refresh validator.

This run checks that the validator accepts only the exact no-file live-state
refresh and rejects damaged or prematurely promoted states, including false file
presence, filled receipt fields, acceptance rerun promotion, field-evidence
promotion, field FWI promotion, field 3D/HPC promotion, GPU-priority promotion,
figure damage, and script-snapshot damage.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/639_gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_receipt_live_state_refresh_validation_sensitivity
```

## Result

```text
source validator ready:                true
scenarios:                             19
expected pass scenarios:               1
expected fail scenarios:               18
observed pass scenarios:               1
observed fail scenarios:               18
unexpected outcomes:                   0
damaged scenarios:                     18
damaged scenarios rejected:            18
live files found:                      0
missing files:                         18
acceptance-gate rerun required:        false
controlled field evidence ready:       false
field FWI ready:                       false
field 3D/HPC ready:                    false
gpu priority:                          none
```

Rejected damaged states include:

```text
refresh-not-ready state
row removal
stage-count damage
file-kind count damage
false live-file presence
filled observed SHA-256
filled observed file size
metadata-parse promotion
DZT signature-candidate promotion
acceptance-recheck promotion
acceptance-gate rerun promotion
accepted field-evidence row promotion
field-evidence promotion
field FWI promotion
field 3D/HPC promotion
GPU-priority promotion
figure damage
script-snapshot damage
```

## Interpretation

The live-state refresh validator is fail-closed. It accepts the exact no-file
receipt refresh and rejects every tested damaged or prematurely promoted state.

## Decision

Use runs `637-639` as the guarded live-state refresh block before any
first-return acceptance-gate rerun. Keep field evidence, field FWI, and field
3D/HPC blocked until real files appear and pass the acceptance path.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_receipt_live_state_refresh.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_receipt_live_state_refresh_validator.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_receipt_live_state_refresh_validation_sensitivity.py
12 passed
```

Figure check:

```text
3221x890, dynamic range=255
```

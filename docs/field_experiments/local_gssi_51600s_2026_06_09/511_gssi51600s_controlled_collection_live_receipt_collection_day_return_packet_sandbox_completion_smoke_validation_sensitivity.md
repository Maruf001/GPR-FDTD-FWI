# Field Experiment 511: Return-Packet Sandbox Completion Smoke Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `510` validator for the run `509` sandbox completion
smoke.

The audit checks whether the validator rejects damaged packet shape,
receipt-report, non-evidence-boundary, figure, and script states.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/511_gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_sandbox_completion_smoke_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_sandbox_completion_smoke_validation_sensitivity_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_sandbox_completion_smoke_validation_sensitivity_summary.json
data/figure_validation.csv
figures/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_sandbox_completion_smoke_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:            true
sensitivity cases:                 23
expected pass cases:               1
expected fail cases:               22
actual pass cases:                 1
actual fail cases:                 22
unexpected outcomes:               0
exact source passes:               true
damaged cases rejected:            true
packet-shape damage rejected:      true
receipt-report damage rejected:    true
boundary damage rejected:          true
live receipt ready:                false
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
```

Damage groups:

| Group | Damaged states | Result |
| --- | ---: | --- |
| Source readiness | 1 | rejected |
| Packet shape and family completion | 10 | rejected |
| Receipt report rows | 3 | rejected |
| Template/live/evidence/downstream boundary | 6 | rejected |
| Figure and script artifacts | 2 | rejected |

## Interpretation

Run `511` hardens the sandbox completion block. The exact run `509` smoke
passes through the run `510` validator, while all damaged alternatives fail.
The guarded result remains a receipt-mechanics pass case only; it is not live
measured field evidence.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_return_packet_sandbox_completion_smoke.py
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_return_packet_sandbox_completion_smoke_validator.py
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_return_packet_sandbox_completion_smoke_validation_sensitivity.py

9 passed
```

Figure check:

```text
2716x890, dynamic range=255
```

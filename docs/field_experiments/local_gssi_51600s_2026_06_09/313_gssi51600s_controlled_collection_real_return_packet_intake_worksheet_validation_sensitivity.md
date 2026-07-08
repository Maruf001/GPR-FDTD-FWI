# Field Experiment 313: Real-Return Packet Intake Worksheet Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `312` field intake worksheet validator with controlled
damaged variants.

This run checks that the validator accepts the exact run `311` worksheet and
rejects damaged variants covering count drift, action drift, template evidence
promotion, false measured packet presence, downstream promotion, GPU-priority
drift, figure drift, and script-snapshot drift.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/313_gssi51600s_controlled_collection_real_return_packet_intake_worksheet_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_intake_worksheet_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_intake_worksheet_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_intake_worksheet_validation_sensitivity.png
scripts/
```

## Result

```text
scenarios:                         16
expected pass:                     1
observed pass:                     1
expected failures:                 15
observed failures:                 15
unexpected outcomes:               0
sensitivity ready:                 true
accepts exact run 311:             true
rejects damaged variants:          true
real packet files present:         false
provenance acceptance ready:       false
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

## Interpretation

The run `312` validator accepts the exact run `311` worksheet and rejects
damaged variants. This protects the worksheet from being treated as measured
field evidence or as a substitute for the staged return packet.

## Decision

Use runs `311-313` as the guarded field return-packet intake worksheet block.
Field evidence remains blocked until measured packet files pass the acceptance
gate.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_intake_worksheet_validation_sensitivity.py
3 passed
```

Figure validation:

```text
3473x913, dynamic range=255
```

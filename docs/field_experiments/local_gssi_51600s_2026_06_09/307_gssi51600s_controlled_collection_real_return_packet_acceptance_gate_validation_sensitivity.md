# Field Experiment 307: Real-Return Packet Acceptance Gate Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `306` field return-packet acceptance-gate validator with
controlled damaged variants.

This run checks that the validator accepts the exact run `305` acceptance gate
and rejects damaged variants covering gate-count drift, measured-packet
promotion, gate-order drift, blocked-reason removal, packet-row drift,
action-count drift, downstream promotion, GPU-priority drift, figure validation
drift, and script-snapshot drift.

It does not stage packet files, run provenance acceptance, promote field
evidence, run field FWI, launch GPU work, or start field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/307_gssi51600s_controlled_collection_real_return_packet_acceptance_gate_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_acceptance_gate_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_acceptance_gate_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_acceptance_gate_validation_sensitivity.png
docs/GSSI51600S_CONTROLLED_COLLECTION_REAL_RETURN_PACKET_ACCEPTANCE_GATE_VALIDATION_SENSITIVITY.md
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
accepts exact run 305:             true
rejects damaged variants:          true
real packet files present:         false
provenance acceptance ready:       false
real archive acceptance ready:     false
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
GPU priority:                      none
```

## Interpretation

The run `306` validator accepts the exact run `305` acceptance gate and rejects
the damaged variants. The gate is now guarded as a future measured-packet
acceptance artifact, but the measured packet is still absent.

## Decision

Use runs `305-307` as the guarded field real-return packet acceptance gate.
Field evidence, field FWI, GPU work, and field 3D/HPC remain blocked until a
complete measured packet is present and passes this gate.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_acceptance_gate_validation_sensitivity.py
3 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_real_return_packet_acceptance_gate_validation_sensitivity.py: pass
tests/test_gssi_field_controlled_collection_real_return_packet_acceptance_gate_validation_sensitivity.py: pass
```

Figure validation:

```text
3473x913, dynamic range=255
```

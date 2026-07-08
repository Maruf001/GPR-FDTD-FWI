# Field Experiment 331: Antenna Metadata Acceptance Gate Refresh Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `330` validator for the run `329` antenna-aware field
return-packet acceptance gate.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/331_gssi51600s_controlled_collection_real_return_packet_acceptance_gate_antenna_metadata_refresh_validation_sensitivity
```

## Result

```text
scenario count:                     14
expected pass count:                1
observed pass count:                1
expected failure count:             13
observed failure count:             13
unexpected outcomes:                0
validation sensitivity ready:       true
validator accepts exact run 329:    true
validator rejects damaged variants: true
packet items:                       61
metadata requirements:              36
real packet files present:          false
provenance acceptance ready:        false
real archive acceptance ready:      false
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
GPU priority:                       none
```

The exact run `329` artifacts pass. Thirteen damaged variants fail as expected
for count drift, gate drift, packet-row drift, action-row drift, downstream
promotion, GPU-priority drift, figure drift, and script-snapshot drift.

## Decision

Use runs `329-331` as the guarded antenna-aware field return-packet acceptance
gate.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_acceptance_gate_antenna_metadata_refresh_validation_sensitivity.py
3 passed
```

Figure check:

```text
3581x895, dynamic range=255
```

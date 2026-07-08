# Field Experiment 330: Antenna Metadata Acceptance Gate Refresh Validator

Date: 2026-06-29

## Purpose

Validate the saved run `329` antenna-aware field return-packet acceptance gate
from artifacts.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/330_gssi51600s_controlled_collection_real_return_packet_acceptance_gate_antenna_metadata_refresh_validator
```

## Result

```text
validation checks:                 7
passed checks:                     7
failed checks:                     0
validation ready:                  true
acceptance gates:                  9
ready gates:                       2
blocked gates:                     7
packet items:                      61
missing packet items:              61
measured requirements:             54
metadata requirements:             36
antenna aperture metadata items:   4
real packet files present:         false
provenance acceptance ready:       false
real archive acceptance ready:     false
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
GPU priority:                      none
```

The validator checks source counts, gate order, packet-item rows, action-group
rows, downstream field blocked states, figure validation, and script snapshots.

## Decision

Use run `330` as the validator for run `329`. Sensitivity hardening remains
required before closing the refreshed gate.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_acceptance_gate_antenna_metadata_refresh_validator.py
3 passed
```

Figure check:

```text
3653x922, dynamic range=255
```

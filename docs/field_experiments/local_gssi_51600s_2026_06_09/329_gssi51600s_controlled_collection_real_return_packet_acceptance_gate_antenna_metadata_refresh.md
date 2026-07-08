# Field Experiment 329: Antenna Metadata Acceptance Gate Refresh

Date: 2026-06-29

## Purpose

Refresh the controlled-field real-return packet acceptance gate for the
61-item antenna-aware measured packet.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/329_gssi51600s_controlled_collection_real_return_packet_acceptance_gate_antenna_metadata_refresh
```

## Result

```text
acceptance gates:                 9
ready gates:                      2
blocked gates:                    7
packet items:                     61
present packet items:             0
missing packet items:             61
measured requirements:            54
missing measured DZT files:       9
metadata requirements:            36
missing metadata requirements:    36
global metadata requirements:     15
file metadata requirements:       21
antenna aperture metadata items:  4
missing checksum rows:            9
missing acceptance results:       7
required action groups:           7
open action groups:               7
real packet files present:        false
provenance acceptance ready:      false
real archive acceptance ready:    false
controlled field evidence ready:  false
field FWI ready:                  false
field 3D/HPC ready:               false
GPU priority:                     none
```

The first two gates pass because the antenna-aware source contracts and packet
inventory are known. The measured-data and execution gates remain blocked
because the measured return packet is absent.

## Interpretation

The acceptance gate now matches the current 61-item field packet target. The
older 57-item gate should not be used for future controlled-field return
packets.

## Decision

Use run `329` as the current rerunnable acceptance gate for future measured
field return packets. Do not run provenance acceptance, archive acceptance,
field evidence, field FWI, GPU work, or field 3D/HPC until it passes.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_acceptance_gate_antenna_metadata_refresh.py
3 passed
```

Figure check:

```text
3761x960, dynamic range=255
```

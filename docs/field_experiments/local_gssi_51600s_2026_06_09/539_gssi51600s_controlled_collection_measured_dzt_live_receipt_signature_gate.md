# Field Experiment 539: Measured DZT Live Receipt Signature Gate

Date: 2026-07-01

## Purpose

Bind the nine measured DZT live-return paths from run `536` to the current
binary receipt guard used for GSSI DZT files.

This run does not create DZT placeholders, copy measured files, run parsers,
rerun provenance/archive gates, run field FWI, run field 3D/HPC, launch GPU
work, or train neural networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/539_gssi51600s_controlled_collection_measured_dzt_live_receipt_signature_gate
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_measured_dzt_live_receipt_signature_gate_dzt_receipt_rows.csv
data/gssi51600s_controlled_collection_measured_dzt_live_receipt_signature_gate_family_rows.csv
data/gssi51600s_controlled_collection_measured_dzt_live_receipt_signature_gate_action_rows.csv
data/gssi51600s_controlled_collection_measured_dzt_live_receipt_signature_gate_summary.json
figures/gssi51600s_controlled_collection_measured_dzt_live_receipt_signature_gate.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source manifest ready:                    true
source manifest validation ready:         true
source manifest sensitivity ready:        true
DZT slots:                                9
controlled profile repeats:               3
time-zero references:                     3
amplitude references:                     3
DZT minimum size bytes:                   65536
GSSI DZT header prefix hex:               ff07
parent directories present:               9
.DZT extension slots:                     9
live DZT files present:                   0
live DZT signature passes:                0
live DZT SHA-256 hashes observed:         0
missing live DZT files:                   9
complete families:                        0
complete actions:                         0
live receipt ready:                       false
parser ready:                             false
provenance ready:                         false
archive ready:                            false
controlled field evidence ready:          false
field FWI ready:                          false
field 3D/HPC ready:                       false
gate artifact ready:                      true
```

The receipt guard for each required DZT file is:

```text
extension:      .DZT
minimum size:   65536 bytes
header prefix:  ff07
checksum:       SHA-256 after the file passes the binary guard
```

## Interpretation

The file destinations are now specific enough for collection-day receipt, and
the binary acceptance rule is explicit. The current live return state remains
empty: all nine DZT files are still missing, so none can be accepted as
measured field evidence.

## Decision

Use this run as the current measured-DZT live receipt boundary. Keep live
receipt, parser, provenance, archive acceptance, field FWI, field 3D/HPC, GPU
work, and neural-network training blocked until all nine real DZT files pass
this gate.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_measured_dzt_live_receipt_signature_gate.py
3 passed
```

Figure check:

```text
2896x852, dynamic range=255
```

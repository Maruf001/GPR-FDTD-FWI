# Field Experiment 365: 61-Item Real-Return Replacement Ledger

Date: 2026-06-29

## Purpose

Convert the guarded synthetic manifest anatomy into a file-level replacement
ledger for the future real field return packet.

This is a replacement-map run. It does not create measured field evidence,
accept provenance, accept a real archive, run field FWI, launch GPU work, or
run field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/365_gssi51600s_controlled_collection_real_return_packet_61item_replacement_ledger
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_replacement_ledger_ledger_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_replacement_ledger_action_summary.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_replacement_ledger_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_replacement_ledger.png
```

## Result

```text
replacement ledger ready:          true
unique packet files:               49
packet requirements:               61
duplicate-path requirements:       12
direct collection input files:     33
generated verification files:      16
measured DZT replacements:         9
metadata replacement files:        24
checksum regeneration files:       9
acceptance rerun files:            7
current synthetic payloads:        49
current measured-evidence payloads:0
field evidence ready:              false
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

The 49-file synthetic packet becomes a real return by replacing 33 direct
collection inputs: nine DZT files and 24 metadata files. The remaining 16
files are generated after the real inputs exist: nine checksums and seven
acceptance-result files.

## Decision

Use this ledger as the real-return replacement map. Keep provenance, archive
acceptance, controlled field evidence, field FWI, GPU work, and field 3D/HPC
blocked until the direct inputs are real and the generated outputs are
regenerated from them.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_replacement_ledger.py
4 passed
```

Figure check:

```text
2861x871, dynamic range=255
```

# Field Experiment 311: Real-Return Packet Intake Worksheet

Date: 2026-06-29

## Purpose

Create a non-evidence intake worksheet for the future measured controlled
collection return packet.

The worksheet converts the guarded 57-item return-packet contract and
acceptance gate into explicit templates. The generated files live inside this
run folder only and do not count as measured field evidence.

This run does not stage measured DZT files, run provenance acceptance, promote
controlled field evidence, run field FWI, launch GPU work, or start field
3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/311_gssi51600s_controlled_collection_real_return_packet_intake_worksheet
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_intake_worksheet_intake_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_intake_worksheet_directory_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_intake_worksheet_template_file_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_intake_worksheet_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_intake_worksheet.png
template_return_inbox/
docs/GSSI51600S_CONTROLLED_COLLECTION_REAL_RETURN_PACKET_INTAKE_WORKSHEET.md
scripts/
```

## Result

```text
packet items:                         57
measured DZT templates:               9
metadata templates:                   32
checksum templates:                   9
acceptance-result templates:          7
template files written:               58
expected packet root:                 outputs/field_experiments/local_gssi_51600s_2026_06_09/263_gssi51600s_controlled_collection_real_return_empty_intake_layout/return_inbox
real packet files present:            false
present packet items:                 0
missing packet items:                 57
provenance acceptance ready:          false
real archive acceptance ready:        false
controlled field evidence ready:      false
field FWI ready:                      false
field 3D/HPC ready:                   false
gpu priority:                         none
```

## Interpretation

The worksheet improves collection handoff clarity without changing the evidence
state. It makes the exact nine measured DZT files, 32 metadata values, nine
checksum rows, and seven acceptance results explicit, but no measured packet
items are staged.

## Decision

Use run `311` as the intake worksheet for future controlled field packet
intake. Provenance acceptance, archive acceptance, controlled field evidence,
field FWI, and field 3D/HPC remain blocked until measured files are staged and
the return-packet acceptance gate passes.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_intake_worksheet.py
4 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_real_return_packet_intake_worksheet.py: pass
tests/test_gssi_field_controlled_collection_real_return_packet_intake_worksheet.py: pass
```

Figure validation:

```text
3652x967, dynamic range=255
```

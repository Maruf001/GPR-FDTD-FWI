# Field Experiment 395: Synthetic Completion Acceptance Smoke

Date: 2026-06-29

## Purpose

Test the acceptance path for the 61-item field intake parser using a fully
filled synthetic worksheet.

The upstream worksheet and parser contract deliberately keep the current rows
blank and rejected. This run answers a narrower implementation question:

```text
If every required completion field is syntactically filled, can the parser
accept the 49-row packet shape?
```

This is synthetic parser testing only. It does not create measured field
evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/395_gssi51600s_controlled_collection_real_return_packet_61item_synthetic_completion_acceptance_smoke
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_completion_acceptance_smoke_filled_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_completion_acceptance_smoke_parser_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_completion_acceptance_smoke_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_completion_acceptance_smoke.png
```

## Result

```text
source worksheet ready:                  true
source parser contract ready:            true
synthetic acceptance smoke ready:        true
worksheet rows:                          49
filled rows:                             49
direct real-input rows:                  33
generated follow-up rows:                16
required completion columns:             5
required completion cells:               245
required completion cells filled:        245
optional note cells filled:              49
synthetic parser accepted rows:          49
synthetic parser rejected rows:          0
synthetic measured-evidence rows:        0
source blank accepted current rows:      0
source blank measured-evidence rows:     0
valid synthetic hashes:                  49
valid synthetic sizes:                   49
valid synthetic timestamps:              49
valid synthetic operators:               49
synthetic only:                          true
real packet files present:               false
provenance acceptance ready:             false
archive acceptance ready:                false
controlled field evidence ready:         false
field FWI ready:                         false
field 3D/HPC ready:                      false
gpu priority:                            none
```

The parser acceptance path works on a completely filled synthetic worksheet:
all 49 rows pass syntax checks. The result is not field evidence because the
paths, hashes, sizes, timestamps, and operator values are synthetic.

## Decision

Use this as an acceptance-path smoke only. Real provenance acceptance, archive
acceptance, field FWI, GPU work, and field 3D/HPC remain blocked until real
files and measured metadata are returned.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_synthetic_completion_acceptance_smoke.py
3 passed
```

Figure check:

```text
3221x881, dynamic range=255
```

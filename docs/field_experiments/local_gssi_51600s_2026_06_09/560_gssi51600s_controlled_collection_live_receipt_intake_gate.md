# Field Experiment 560: Live Receipt Intake Gate

Date: 2026-07-01

## Purpose

Create a reusable intake gate for the thirty-three controlled-collection live
receipt files defined by run `559`.

This run does not create measured field evidence, accept live field files, run
DZT parsing, promote provenance/archive state, launch field FWI, or launch
field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/560_gssi51600s_controlled_collection_live_receipt_intake_gate
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_intake_gate_stage_rows.csv
data/gssi51600s_controlled_collection_live_receipt_intake_gate_file_rows.csv
data/gssi51600s_controlled_collection_live_receipt_intake_gate_summary.json
figures/gssi51600s_controlled_collection_live_receipt_intake_gate.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source ledger ready:                 true
stages:                              6
expected live files:                 33
live parent directories present:     33
live files present:                  0
missing live files:                  33
measured DZT files required:         9
metadata files required:             24
metadata value fields required:      96
observed metadata value fields:      0
missing metadata value fields:       96
DZT signature passes:                0
metadata schema passes:              0
accepted files:                      0
accepted stages:                     0
stage item counts:                   7;4;6;6;6;4
stage metadata field counts:         28;16;12;12;12;16
stage missing file counts:           7;4;6;6;6;4
field live receipt intake accepted:  false
live receipt ready:                  false
parser ready:                        false
provenance ready:                    false
archive ready:                       false
controlled field evidence ready:     false
field FWI ready:                     false
field 3D/HPC ready:                  false
```

Stage intake state:

| Stage | Contract block | Items | DZT files | Metadata files | Present files | Missing metadata values |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | pre-collection records | 7 | 0 | 7 | 0 | 28 |
| 2 | setup measurement controls | 4 | 0 | 4 | 0 | 16 |
| 3 | controlled profile repeats | 6 | 3 | 3 | 0 | 12 |
| 4 | time-zero references | 6 | 3 | 3 | 0 | 12 |
| 5 | amplitude references | 6 | 3 | 3 | 0 | 12 |
| 6 | session closeout | 4 | 0 | 4 | 0 | 16 |

## Interpretation

The controlled field collection now has a direct receipt intake gate. When
field files arrive, this gate classifies each receipt item as missing, empty,
extension-mismatched, JSON-parse-failed, metadata-incomplete,
DZT-signature-failed, or accepted.

The current state is still pre-return. All thirty-three parent directories
exist, but none of the thirty-three live files exists. The nine measured DZT
files and twenty-four metadata JSON files are therefore still required before
parser, provenance, archive, or field FWI work can proceed.

## Decision

Use this intake gate when controlled-collection files arrive. Keep live
receipt, parser/provenance/archive promotion, controlled field evidence, field
FWI, and field 3D/HPC blocked until all thirty-three files pass intake.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_intake_gate.py
4 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_live_receipt_intake_gate.py: pass
tests/test_gssi_field_controlled_collection_live_receipt_intake_gate.py: pass
```

Figure check:

```text
2212x854, dynamic range=255
```

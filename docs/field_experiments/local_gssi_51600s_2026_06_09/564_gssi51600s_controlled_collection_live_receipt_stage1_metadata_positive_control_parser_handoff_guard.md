# Field Experiment 564: Stage-1 Metadata Parser Handoff Guard

Date: 2026-07-01

## Purpose

Check whether the accepted stage-1 metadata positive control from run `563`
can be handed to the next parser-level field path.

This run verifies that the positive-control metadata files are readable and
internally complete, while still blocking parser/provenance/archive promotion
because the full controlled-collection return is incomplete.

This is CPU-only validation. It does not parse measured DZT files, accept live
field evidence, run field FWI, run field 3D/HPC, or launch neural-network
training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/564_gssi51600s_controlled_collection_live_receipt_stage1_metadata_positive_control_parser_handoff_guard
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_stage1_metadata_positive_control_parser_handoff_guard_handoff_rows.csv
data/gssi51600s_controlled_collection_live_receipt_stage1_metadata_positive_control_parser_handoff_guard_summary.json
figures/gssi51600s_controlled_collection_live_receipt_stage1_metadata_positive_control_parser_handoff_guard.png
scripts/script_snapshot_manifest.json
```

## Result

```text
handoff checks:                          5
passed handoff checks:                   5
failed handoff checks:                   0
accepted positive-control files:         7
accepted metadata values:                28
full live receipt files required:        33
full metadata values required:           96
measured DZT files required:             9
positive-control file fraction:          0.212121
positive-control metadata fraction:      0.291667
handoff to parser ready:                 false
field live receipt intake accepted:      false
live receipt ready:                      false
parser ready:                            false
provenance ready:                        false
archive ready:                           false
controlled field evidence ready:         false
field FWI ready:                         false
field 3D/HPC ready:                      false
gpu priority:                            none
```

The five handoff checks are:

| Order | Check | Observed | Required | Passed |
| ---: | --- | ---: | ---: | --- |
| 1 | stage-1 metadata positive control passes intake | 7 | 7 | true |
| 2 | full live receipt remains incomplete | 7 | 33 | true |
| 3 | measured DZT files are still required | 0 | 9 | true |
| 4 | metadata coverage remains partial | 28 | 96 | true |
| 5 | parser remains blocked | false | false | true |

## Interpretation

The stage-1 metadata positive control is useful only as a parser mechanics
check. It confirms that seven pre-collection metadata JSON files can be read,
counted, and rejected as insufficient for field evidence.

The result does not change the field decision boundary. A complete controlled
field return still requires thirty-three live files: nine measured GSSI DZT
files and twenty-four metadata JSON files with ninety-six required metadata
values.

## Decision

Use run `564` as the parser-handoff guard for stage-1 metadata mechanics. Keep
live receipt, measured DZT parsing, provenance/archive promotion, controlled
field evidence, field FWI, and field 3D/HPC blocked until all thirty-three
controlled-collection live files arrive and pass intake.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_stage1_metadata_positive_control_parser_handoff_guard.py
3 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_live_receipt_stage1_metadata_positive_control_parser_handoff_guard.py: pass
tests/test_gssi_field_controlled_collection_live_receipt_stage1_metadata_positive_control_parser_handoff_guard.py: pass
```

Figure check:

```text
1672x844, dynamic range=255
```

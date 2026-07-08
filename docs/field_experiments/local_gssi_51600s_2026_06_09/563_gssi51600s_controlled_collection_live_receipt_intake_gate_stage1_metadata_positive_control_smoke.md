# Field Experiment 563: Stage-1 Metadata Intake Positive Control Smoke

Date: 2026-07-01

## Purpose

Exercise the positive path of the controlled-collection live receipt intake
gate using seven output-local stage-1 metadata JSON files.

This run does not create measured field evidence, accept live field files, run
DZT parsing, promote provenance/archive state, launch field FWI, or launch
field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/563_gssi51600s_controlled_collection_live_receipt_intake_gate_stage1_metadata_positive_control_smoke
```

Key artifacts:

```text
data/stage1_metadata_positive_control/*.json
data/gssi51600s_controlled_collection_live_receipt_intake_gate_stage1_metadata_positive_control_smoke_file_rows.csv
data/gssi51600s_controlled_collection_live_receipt_intake_gate_stage1_metadata_positive_control_smoke_summary.json
figures/gssi51600s_controlled_collection_live_receipt_intake_gate_stage1_metadata_positive_control_smoke.png
scripts/script_snapshot_manifest.json
```

## Result

```text
positive-control files:                   7
positive-control files present:           7
positive-control accepted files:          7
required metadata values:                 28
observed metadata values:                 28
missing metadata values:                  0
JSON parse passes:                        7
positive-control statuses:                accepted;accepted;accepted;accepted;accepted;accepted;accepted
field live receipt intake accepted as real:false
live receipt ready:                       false
parser ready:                             false
provenance ready:                         false
archive ready:                            false
controlled field evidence ready:          false
field FWI ready:                          false
field 3D/HPC ready:                       false
```

Accepted output-local metadata files:

| Metadata item | Required values | Observed values | Intake status |
| --- | ---: | ---: | --- |
| antenna model, serial, and nominal frequency | 4 | 4 | accepted |
| antenna serial | 4 | 4 | accepted |
| material | 4 | 4 | accepted |
| software version | 4 | 4 | accepted |
| survey method | 4 | 4 | accepted |
| system | 4 | 4 | accepted |
| truth source | 4 | 4 | accepted |

## Interpretation

The field intake gate's positive path works for the first collection stage.
Seven output-local metadata JSON files pass the same parse and value-count
checks used by the live intake gate.

This is mechanics coverage only. It does not replace live field files and does
not make controlled field evidence, parser/provenance/archive promotion, field
FWI, or field 3D/HPC ready.

## Decision

Use this as a stage-1 positive-control smoke for the field intake gate. Keep
live receipt, controlled field evidence, parser/provenance/archive promotion,
field FWI, and field 3D/HPC blocked until real controlled-collection files
arrive and pass the guarded intake path.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_intake_gate_stage1_metadata_positive_control_smoke.py
2 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_live_receipt_intake_gate_stage1_metadata_positive_control_smoke.py: pass
tests/test_gssi_field_controlled_collection_live_receipt_intake_gate_stage1_metadata_positive_control_smoke.py: pass
```

Figure check:

```text
1996x847, dynamic range=255
```

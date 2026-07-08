# Field Experiment 562: Live Receipt Intake Gate Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `561` validator for the controlled-collection live receipt
intake gate.

This run does not create measured field evidence, accept live field files, run
DZT parsing, promote provenance/archive state, launch field FWI, or launch
field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/562_gssi51600s_controlled_collection_live_receipt_intake_gate_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_intake_gate_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_live_receipt_intake_gate_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_live_receipt_intake_gate_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:             true
sensitivity scenarios:              9
expected pass scenarios:            1
expected fail scenarios:            8
observed pass scenarios:            1
observed fail scenarios:            8
unexpected outcomes:                0
damaged scenarios:                  8
damaged scenarios rejected:         8
```

Sensitivity scenarios:

| Scenario | Expected | Observed | First failed check |
| --- | --- | --- | --- |
| exact | pass | pass |  |
| source not ready | fail | fail | source intake gate ready |
| missing count drift | fail | fail | current live state remains absent |
| file status damage | fail | fail | current live state remains absent |
| stage shape damage | fail | fail | stage shape is preserved |
| false acceptance | fail | fail | receipt acceptance remains blocked |
| downstream promotion | fail | fail | receipt acceptance remains blocked |
| figure damage | fail | fail | figure and script snapshots are present |
| snapshot damage | fail | fail | figure and script snapshots are present |

## Interpretation

The validator accepts only the exact saved field intake-gate state. It rejects
damaged source readiness, live-file counts, per-file status, stage shape, false
receipt acceptance, downstream promotion, damaged figure validation, and
missing script snapshots.

## Decision

Use runs `560-562` as the guarded controlled-collection live receipt intake
block. The current field path remains blocked on real measured files and
metadata, but the intake side is now ready to classify future files and reject
damaged states.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_intake_gate_validation_sensitivity.py
3 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_live_receipt_intake_gate_validation_sensitivity.py: pass
tests/test_gssi_field_controlled_collection_live_receipt_intake_gate_validation_sensitivity.py: pass
```

Figure check:

```text
2212x847, dynamic range=255
```

# Field Experiment 561: Live Receipt Intake Gate Validator

Date: 2026-07-01

## Purpose

Validate the saved run `560` controlled-collection live receipt intake gate
from its output artifacts.

This run does not create measured field evidence, accept live field files, run
DZT parsing, promote provenance/archive state, launch field FWI, or launch
field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/561_gssi51600s_controlled_collection_live_receipt_intake_gate_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_intake_gate_validator_check_rows.csv
data/gssi51600s_controlled_collection_live_receipt_intake_gate_validator_summary.json
figures/gssi51600s_controlled_collection_live_receipt_intake_gate_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source intake gate ready:          true
validation checks:                 7
passed validation checks:          7
failed validation checks:          0
expected live files:               33
missing live files:                33
measured DZT files required:       9
metadata files required:           24
metadata value fields required:    96
missing metadata value fields:     96
field live receipt intake accepted:false
live receipt ready:                false
parser ready:                      false
provenance ready:                  false
archive ready:                     false
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
```

Validation checks:

| Check | Result |
| --- | --- |
| Source intake gate ready | pass |
| Thirty-three live files represented | pass |
| Current live state remains absent | pass |
| Stage shape preserved | pass |
| Receipt acceptance remains blocked | pass |
| Downstream states remain blocked | pass |
| Figure and script snapshots present | pass |

## Interpretation

The saved field intake gate is internally consistent. It sees all
thirty-three expected controlled-collection files, preserves the six-stage
collection shape, confirms that all files are still absent, and keeps live
receipt, parser/provenance/archive promotion, controlled field evidence, field
FWI, and field 3D/HPC blocked.

## Decision

Use run `560` as the live receipt intake gate and run `561` as its
saved-artifact validator. Sensitivity hardening remains the next useful step
before relying on the gate for damaged future field returns.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_intake_gate_validator.py
3 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_live_receipt_intake_gate_validator.py: pass
tests/test_gssi_field_controlled_collection_live_receipt_intake_gate_validator.py: pass
```

Figure check:

```text
1492x846, dynamic range=255
```

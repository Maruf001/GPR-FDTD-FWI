# Field Experiment 465: Live Receipt Verifier Current-State Validator

Date: 2026-06-30

## Purpose

Validate the run `464` live receipt verifier current-state audit.

Run `464` added a reusable receipt verifier and wrote a current-state receipt
report for the locked 33-row field manifest. This run checks that the report is
structurally valid and that it does not promote field evidence while all live
files remain missing.

This run does not copy measured files, accept field evidence, rerun the parser,
rerun provenance, rerun archive acceptance, launch field FWI, launch GPU work,
or launch field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/465_gssi51600s_controlled_collection_live_receipt_verifier_current_state_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_verifier_current_state_validator_check_rows.csv
data/gssi51600s_controlled_collection_live_receipt_verifier_current_state_validator_summary.json
figures/gssi51600s_controlled_collection_live_receipt_verifier_current_state_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source audit ready:                    true
checks:                                6
passed checks:                         6
failed checks:                         0
required receipt rows:                 33
missing files:                         33
receipt-ready rows:                    0
controlled field evidence rows:        0
parser ready:                          false
provenance ready:                      false
archive ready:                         false
field FWI ready:                       false
field 3D/HPC ready:                    false
validation ready:                      true
```

Validation checks:

| Check | Passed |
| --- | --- |
| source audit ready | true |
| receipt report shape | true |
| all live files missing | true |
| zero receipt readiness | true |
| downstream remains blocked | true |
| figure and scripts exist | true |

## Interpretation

The live receipt report is valid and remains a current-state report only. It
confirms the expected 33-row manifest shape, with nine DZT rows and 24 metadata
JSON rows, but no live files and no receipt-ready rows.

## Decision

Use runs `464` and `465` as the guarded live receipt verifier checkpoint. Do
not rerun parser, provenance, archive acceptance, field FWI, GPU work, or field
3D/HPC until all 33 receipt rows pass.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_verifier_current_state_validator.py
3 passed
```

Figure check:

```text
2105x847, dynamic range=255
```

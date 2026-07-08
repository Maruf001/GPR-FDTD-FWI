# Field Experiment 267: Controlled Collection Real-Return Inbox Current Scan Validator

Date: 2026-06-28

## Purpose

Validate the saved run `266` real-return inbox scan.

This run does not create placeholder DZT files, ingest real data into an
accepted archive, run DZT preprocessing, run field FWI, launch GPU/HPC work, or
promote controlled field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/267_gssi51600s_controlled_collection_real_return_inbox_current_scan_validator
```

Key artifacts:

```text
data/field_controlled_collection_real_return_inbox_current_scan_validation_checks.csv
data/field_controlled_collection_real_return_inbox_current_scan_validator_summary.json
figures/field_controlled_collection_real_return_inbox_current_scan_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                         8
passed checks:                  8
failed checks:                  0
validation ready:               true
source real files present:      0
source metadata values present: 0
source checksums present:       0
provenance acceptance ready:    false
real archive acceptance ready:  false
field FWI ready:                false
gpu priority:                   none
```

Validated checks:

| Check | Result |
| --- | --- |
| Policy and source guard | pass |
| Required file scan counts | pass |
| Metadata scan counts | pass |
| Checksum scan counts | pass |
| Unexpected files absent | pass |
| Acceptance and downstream blocked | pass |
| Figure validation present | pass |
| Script snapshots present | pass |

## Interpretation

The saved inbox scan is internally consistent. The validator confirms that the
real-return inbox has no required DZT files, no filled metadata values, no
checksums, and no unexpected files, while all provenance, archive, evidence,
FWI, 3D/HPC, and GPU gates remain blocked.

## Decision

Use run `266` as the current field intake status checkpoint. Sensitivity
remains required before treating the scan validator as guarded.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_inbox_current_scan_validator.py
2 passed
```

Figure validation:

```text
2825x896, dynamic range=255
```

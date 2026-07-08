# Field Experiment 531: Controlled Collection Metadata Live-Path Rescan Validator

Date: 2026-06-30

## Purpose

Validate run `530` from written artifacts.

The validator checks that the live-path rescan has the expected 33-item shape,
that all live files are absent, that the metadata and measured-DZT split is
preserved, and that field evidence, field FWI, and field 3D/HPC remain blocked.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/531_gssi51600s_controlled_collection_metadata_live_path_rescan_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_metadata_live_path_rescan_validator_check_rows.csv
data/gssi51600s_controlled_collection_metadata_live_path_rescan_validator_summary.json
figures/gssi51600s_controlled_collection_metadata_live_path_rescan_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                         6
passed checks:                  6
failed checks:                  0
live items:                     33
live actions:                   4
live files present:             0
global metadata missing:        15
per-file metadata missing:      9
paired DZT missing:             9
final receipt missing items:    33
live receipt ready:             false
field FWI ready:                false
field 3D/HPC ready:             false
GPU priority:                   none
```

## Interpretation

Run `530` validates as an empty live-return root with all expected parent
directories present.

## Decision

Keep field evidence, field FWI, and field 3D/HPC blocked until real metadata
and DZT files are supplied.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_metadata_live_path_rescan_validator.py
3 passed
```

Figure check:

```text
2357x836, dynamic range=255
```

# Field Experiment 532: Controlled Collection Metadata Live-Path Rescan Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `531` validator.

The validator should accept only the exact empty live-path rescan and reject
fake live files, fake acceptance, damaged item counts, damaged dependency
counts, and premature parser/provenance/field-readiness promotion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/532_gssi51600s_controlled_collection_metadata_live_path_rescan_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_metadata_live_path_rescan_validation_sensitivity_case_rows.csv
data/gssi51600s_controlled_collection_metadata_live_path_rescan_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_metadata_live_path_rescan_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:          true
sensitivity cases:               21
expected pass cases:             1
expected fail cases:             20
actual pass cases:               1
actual fail cases:               20
unexpected cases:                0
live receipt ready:              false
field FWI ready:                 false
field 3D/HPC ready:              false
GPU priority:                    none
```

The exact run `530` rescan passes. The twenty damaged states fail as expected
for source readiness, item/action shape, group-count damage, fake live-file
presence, fake nonempty files, fake acceptance, missing-count damage,
premature per-file metadata start, final receipt damage, action completion
promotion, live-receipt promotion, parser/provenance promotion, field-FWI
promotion, field-3D/HPC promotion, figure damage, and missing script snapshots.

## Interpretation

The validator is sensitive to the failure modes that would make the field
archive look more complete than it is.

## Decision

Keep the current field archive blocked until real metadata and measured DZT
files are supplied.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_metadata_live_path_rescan.py
tests/test_gssi_field_controlled_collection_metadata_live_path_rescan_validator.py
tests/test_gssi_field_controlled_collection_metadata_live_path_rescan_validation_sensitivity.py
9 passed
```

Figure check:

```text
2897x855, dynamic range=255
```

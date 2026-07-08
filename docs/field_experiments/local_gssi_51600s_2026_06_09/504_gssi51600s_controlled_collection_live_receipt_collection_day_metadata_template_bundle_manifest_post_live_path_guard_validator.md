# Field Experiment 504: Controlled Collection Metadata Template Bundle Manifest Post-Live-Path Guard Validator

Date: 2026-06-30

## Purpose

Validate run `503` from saved artifacts.

The validator checks source readiness, the 24-row template guard table, empty
and separated live paths, blocked receipt/downstream states, and figure/script
artifacts.

This is an artifact validation run. It does not stage measured DZT files,
create live receipt files, run parsers, rerun provenance/archive gates, run
field FWI, launch GPU work, or start field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/504_gssi51600s_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_post_live_path_guard_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_post_live_path_guard_validator_check_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_post_live_path_guard_validator_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_post_live_path_guard_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                              5
passed checks:                       5
failed checks:                       0
guard rows:                         24
template files exist:               24
output-local templates:             24
live files exist:                    0
manifest live-file-present rows:     0
manifest live-receipt-ready rows:    0
computed template/live path equals:  0
templates under live root:           0
live paths under live root:         24
templates accepting as live receipt: 0
live receipt ready:              false
parser ready:                    false
provenance ready:                false
archive ready:                   false
controlled field evidence ready: false
field FWI ready:                 false
field 3D/HPC ready:              false
validation ready:                 true
```

Validator checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source post-live-path guard ready | pass |
| 2 | template guard rows preserve bundle shape | pass |
| 3 | live paths remain empty and separated | pass |
| 4 | receipt and downstream remain blocked | pass |
| 5 | figure and scripts exist | pass |

## Interpretation

Run `503` validates as an output-local metadata preparation guard. The live
external-return paths remain empty and separated from the generated templates.

## Decision

Use this validator as the artifact guard for run `503`.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_post_live_path_guard.py
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_post_live_path_guard_validator.py

6 passed
```

Figure validation:

```text
2285x834, dynamic range=255
```

# Field Experiment 505: Controlled Collection Metadata Template Bundle Manifest Post-Live-Path Guard Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `504` post-live-path guard validator.

The sensitivity run mutates the run `503` artifacts in memory and checks
whether the validator rejects damaged source readiness, guard-row shape,
template output-local state, live-file promotion, path overlap, template-under-
live-root promotion, live-root damage, receipt/downstream promotion, figure
damage, and missing script snapshots.

This is a CPU-only artifact sensitivity run. It does not stage measured DZT
files, create live receipt files, run parsers, rerun provenance/archive gates,
run field FWI, launch GPU work, or start field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/505_gssi51600s_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_post_live_path_guard_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_post_live_path_guard_validation_sensitivity_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_post_live_path_guard_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_post_live_path_guard_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
cases:                         19
expected pass cases:            1
expected fail cases:           18
actual pass cases:              1
actual fail cases:             18
unexpected outcomes:            0
exact source passes:          true
damaged cases rejected:       true
live receipt ready:          false
field FWI ready:             false
field 3D/HPC ready:          false
sensitivity ready:            true
```

Damage cases cover source readiness, row removal, template-family damage,
template-existence damage, output-local damage, live-file existence, manifest
live-file promotion, manifest receipt-readiness promotion, live-path overlap,
template-under-live-root promotion, live-root damage, false receipt acceptance,
live-receipt promotion, parser promotion, field-FWI promotion, field-3D/HPC
promotion, figure damage, and missing script snapshots.

## Interpretation

The validator accepts only the exact post-live-path guard and rejects damaged
live-path, output-local, downstream, figure, and script states.

## Decision

Keep run `504` as the validator guard for run `503`.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_post_live_path_guard.py
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_post_live_path_guard_validator.py
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_post_live_path_guard_validation_sensitivity.py

9 passed
```

Figure validation:

```text
2500x876, dynamic range=255
```

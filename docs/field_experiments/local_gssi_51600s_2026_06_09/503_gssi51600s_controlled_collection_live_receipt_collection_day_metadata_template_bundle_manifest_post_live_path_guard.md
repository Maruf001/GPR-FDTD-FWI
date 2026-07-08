# Field Experiment 503: Controlled Collection Metadata Template Bundle Manifest Post-Live-Path Guard

Date: 2026-06-30

## Purpose

Audit the locked live external-return paths after the run `500` metadata
template bundle manifest and its run `501-502` validator/sensitivity block.

This guard checks that the 24 metadata templates remain output-local
preparation files and did not become live receipt files, overlap live staging
paths, or sit under the live staging root.

This is a CPU-only artifact guard. It does not stage measured DZT files, create
live receipt files, run parsers, rerun provenance/archive gates, run field FWI,
launch GPU work, or start field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/503_gssi51600s_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_post_live_path_guard
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_post_live_path_guard_guard_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_post_live_path_guard_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_post_live_path_guard.png
scripts/script_snapshot_manifest.json
```

## Result

```text
guard rows:                         24
global metadata templates:          15
per-file metadata templates:         9
pre-collection templates:           15
post-measurement templates:          9
template files exist:               24
output-local templates:             24
live files exist:                    0
manifest live-file-present rows:     0
manifest live-receipt-ready rows:    0
manifest live-path overlaps:         0
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
guard ready:                      true
```

## Interpretation

The metadata bundle is still preparation inventory only. The templates exist in
the dataset-local output tree, while the locked live external-return paths
remain empty. No parser, provenance, archive, controlled-evidence, field FWI,
or field 3D/HPC state is promoted.

## Decision

Keep the metadata bundle as collection-day preparation inventory. Live receipt
and downstream field evidence remain blocked until real measured files are
staged under the locked live paths and pass the receipt gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_post_live_path_guard.py

3 passed
```

Figure validation:

```text
2285x846, dynamic range=255
```

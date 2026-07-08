# Field Experiment 500: Controlled Collection Live Receipt Collection-Day Metadata Template Bundle Manifest

Date: 2026-06-30

## Purpose

Combine the validated global metadata and per-file metadata template streams
into one collection-day metadata template inventory.

This run reads the output-local templates from runs `494` and `497`, guarded by
their validators and sensitivity runs. It does not copy templates into the live
external return path and it does not count any template as a receipt-ready
field file.

This is a CPU-only manifest run. It does not create live measured files, parse
DZT data, promote measured evidence, run provenance acceptance, build an
archive, launch field FWI, launch GPU work, or start field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/500_gssi51600s_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest.png
scripts/
```

## Result

```text
source global pack ready:              true
source global validation ready:        true
source global sensitivity ready:       true
source per-file pack ready:            true
source per-file validation ready:      true
source per-file sensitivity ready:     true
templates:                              24
global metadata templates:              15
per-file metadata templates:             9
pre-collection templates:               15
post-measurement templates:              9
paired DZT templates:                    9
templates requiring measured DZT:        9
template files written:                 24
output-local templates:                 24
total required receipt checks:         129
value placeholders:                     66
current live files present:              0
current live receipt-ready files:         0
template/live path overlaps:             0
templates accepted as live receipt:       0
live receipt ready:                    false
parser ready:                          false
provenance ready:                      false
archive ready:                         false
controlled field evidence ready:       false
field FWI ready:                       false
field 3D/HPC ready:                    false
gpu priority:                          none
bundle manifest ready:                 true
```

## Interpretation

The field metadata preparation work is now easier to use on collection day.
There is one manifest with 24 templates:

| Template family | Count | Timing | Measured DZT required |
| --- | ---: | --- | --- |
| Global metadata | 15 | before collection | no |
| Per-file metadata | 9 | after measurement | yes |

The split matters. The 15 global templates can be drafted before field
collection. The nine per-file templates are tied to expected DZT files and only
become meaningful after those measured files exist.

## Decision

Use this manifest as the collection-day metadata template inventory. Keep live
receipt, parser, provenance, archive, field FWI, and field 3D/HPC blocked until
real measured files and completed metadata files are copied to the live
external return path and pass receipt.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest.py

3 passed
```

Figure validation:

```text
2357x848, dynamic range=255
```

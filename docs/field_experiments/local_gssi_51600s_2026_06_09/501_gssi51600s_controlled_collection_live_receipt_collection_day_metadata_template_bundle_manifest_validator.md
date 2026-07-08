# Field Experiment 501: Controlled Collection Live Receipt Collection-Day Metadata Template Bundle Manifest Validator

Date: 2026-06-30

## Purpose

Validate the run `500` metadata template bundle manifest from generated
artifacts.

The validator checks the 24-row template inventory, the 15/9 global/per-file
split, the pre-collection/post-measurement timing split, the paired DZT
requirements, template hashes, receipt-check totals, and the blocked live
receipt boundary.

This is a CPU-only artifact validation. It does not create live measured files,
parse DZT data, promote measured evidence, run provenance acceptance, build an
archive, launch field FWI, launch GPU work, or start field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/501_gssi51600s_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_validator_check_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_validator_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_validator.png
scripts/
```

## Result

```text
checks:                         5
passed checks:                  5
failed checks:                  0
templates:                     24
global metadata templates:     15
per-file metadata templates:    9
pre-collection templates:      15
post-measurement templates:     9
templates requiring DZT:        9
total receipt checks:         129
value placeholders:            66
current live files present:     0
current live receipt-ready:     0
live receipt ready:            false
parser ready:                  false
provenance ready:              false
archive ready:                 false
field FWI ready:               false
field 3D/HPC ready:            false
gpu priority:                  none
validation ready:              true
```

Validator checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source bundle manifest ready | pass |
| 2 | template family and timing shape match | pass |
| 3 | template accounting and hashes match | pass |
| 4 | live receipt and downstream remain blocked | pass |
| 5 | figure and scripts exist | pass |

## Interpretation

The bundle manifest validates as a single collection-day metadata inventory.
It gives a clean handoff list but remains preparation-only. It does not close
live receipt and does not make the field archive ready for parser,
provenance, field FWI, or 3D/HPC work.

## Decision

Use this validator as the artifact guard for run `500`.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest.py
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_validator.py

6 passed
```

Figure validation:

```text
2285x834, dynamic range=255
```

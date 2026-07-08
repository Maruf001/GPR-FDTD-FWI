# Field Experiment 495: Controlled Collection Live Receipt Collection-Day Global Metadata Prefill Template-Pack Validator

Date: 2026-06-30

## Purpose

Validate the run `494` global metadata prefill template pack from generated
artifacts.

The validator checks that all 15 templates exist, match the global metadata
route, have the expected placeholder schema, remain output-local, and do not
count as live receipt files.

This is a CPU-only artifact validation. It does not create live measured files,
parse DZT data, promote measured evidence, run provenance acceptance, build an
archive, launch field FWI, launch GPU work, or start field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/495_gssi51600s_controlled_collection_live_receipt_collection_day_global_metadata_prefill_template_pack_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_global_metadata_prefill_template_pack_validator_check_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_global_metadata_prefill_template_pack_validator_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_global_metadata_prefill_template_pack_validator.png
scripts/
```

## Result

```text
checks:                              5
passed checks:                       5
failed checks:                       0
templates:                          15
template files written:             15
total required receipt checks:      75
value placeholders:                 30
current live files present:          0
current live receipt-ready files:     0
template/live path overlaps:         0
templates accepted as live receipt:   0
live receipt ready:                 false
parser ready:                       false
provenance ready:                   false
archive ready:                      false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
validation ready:                   true
```

Validator checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source template pack ready | pass |
| 2 | template table matches global metadata route | pass |
| 3 | template payloads have placeholder schema | pass |
| 4 | templates remain output-local and non-receipt | pass |
| 5 | figure and scripts exist | pass |

## Interpretation

The template pack validates as a preparation artifact. It can help draft the
global metadata before collection, but it does not close receipt, does not
promote parser/provenance/archive readiness, and does not support field FWI.

## Decision

Use this validator as the artifact guard for run `494`.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_global_metadata_prefill_template_pack.py
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_global_metadata_prefill_template_pack_validator.py
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_global_metadata_prefill_template_pack_validation_sensitivity.py

9 passed
```

Figure validation:

```text
2285x840, dynamic range=255
```

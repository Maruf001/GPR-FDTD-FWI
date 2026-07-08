# Field Experiment 496: Controlled Collection Live Receipt Collection-Day Global Metadata Prefill Template-Pack Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `495` validator by mutating the run `494` global metadata
prefill template-pack artifacts.

The sensitivity audit checks that the validator accepts the exact template pack
and rejects damaged metadata identity, check counts, template written flags,
placeholder schema counts, live-file promotion, receipt promotion, field-FWI
promotion, figure damage, and missing script snapshots.

This is a CPU-only artifact sensitivity audit. It does not create live measured
files, parse DZT data, promote measured evidence, run provenance acceptance,
build an archive, launch field FWI, launch GPU work, or start field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/496_gssi51600s_controlled_collection_live_receipt_collection_day_global_metadata_prefill_template_pack_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_global_metadata_prefill_template_pack_validation_sensitivity_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_global_metadata_prefill_template_pack_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_global_metadata_prefill_template_pack_validation_sensitivity.png
scripts/
```

## Result

```text
cases:                    17
expected pass cases:       1
expected fail cases:      16
actual pass cases:         1
actual fail cases:        16
unexpected cases:          0
exact source passes:       true
damaged cases rejected:    true
live receipt ready:        false
field FWI ready:           false
field 3D/HPC ready:        false
gpu priority:              none
sensitivity ready:         true
```

Sensitivity cases:

| Case | Expected | Actual |
| --- | --- | --- |
| exact_source | pass | pass |
| source_ready_false | fail | fail |
| template_row_removed | fail | fail |
| metadata_name_damage | fail | fail |
| required_check_damage | fail | fail |
| template_written_damage | fail | fail |
| template_key_count_damage | fail | fail |
| placeholder_count_damage | fail | fail |
| live_file_promotion | fail | fail |
| receipt_ready_promotion | fail | fail |
| path_overlap | fail | fail |
| template_accepts_live_receipt | fail | fail |
| live_receipt_ready | fail | fail |
| field_fwi_promotion | fail | fail |
| field_3d_promotion | fail | fail |
| figure_damage | fail | fail |
| script_snapshot_damage | fail | fail |

## Interpretation

The validator rejects the important failure modes. In particular, an
output-local template cannot be mistaken for a live receipt file, cannot
overlap a live return path, and cannot promote field FWI or field 3D/HPC.

## Decision

Keep global metadata templates as preparation artifacts, not live field
evidence.

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
2284x857, dynamic range=255
```

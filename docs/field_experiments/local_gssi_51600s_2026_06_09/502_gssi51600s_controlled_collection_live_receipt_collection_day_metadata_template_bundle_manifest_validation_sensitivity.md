# Field Experiment 502: Controlled Collection Live Receipt Collection-Day Metadata Template Bundle Manifest Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `501` metadata template bundle manifest validator.

The sensitivity run mutates the validated manifest artifacts in memory and
checks whether the validator rejects damaged states. The damage cases cover
template-family shape, collection timing, paired DZT identity, receipt-check
accounting, placeholder accounting, template written flags, template hashes,
live-receipt promotion, field-FWI promotion, field-3D/HPC promotion, figure
damage, and missing script snapshots.

This is a CPU-only artifact sensitivity run. It does not create live measured
files, parse DZT data, promote measured evidence, run provenance acceptance,
build an archive, launch field FWI, launch GPU work, or start field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/502_gssi51600s_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_validation_sensitivity_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_validation_sensitivity.png
scripts/
```

## Result

```text
cases:                  19
expected pass cases:     1
expected fail cases:    18
actual pass cases:       1
actual fail cases:      18
unexpected outcomes:     0
exact source passes:   true
damaged cases rejected: true
live receipt ready:    false
field FWI ready:       false
field 3D/HPC ready:    false
gpu priority:          none
sensitivity ready:     true
```

Sensitivity cases:

| Case | Expected | Actual |
| --- | --- | --- |
| exact source | pass | pass |
| source readiness false | fail | fail |
| manifest row removed | fail | fail |
| template family damaged | fail | fail |
| preparation timing damaged | fail | fail |
| paired DZT identity damaged | fail | fail |
| receipt check count damaged | fail | fail |
| placeholder count damaged | fail | fail |
| template written flag damaged | fail | fail |
| template hash damaged | fail | fail |
| live file promoted | fail | fail |
| receipt ready promoted | fail | fail |
| template overlaps live path | fail | fail |
| template accepted as live receipt | fail | fail |
| live receipt ready | fail | fail |
| field FWI promoted | fail | fail |
| field 3D/HPC promoted | fail | fail |
| figure dynamic range removed | fail | fail |
| script snapshots removed | fail | fail |

## Interpretation

The validator is sensitive to the failure modes that would make the bundle
manifest inaccurate or allow preparation templates to look like live field
evidence.

## Decision

Keep the metadata bundle manifest as preparation inventory only. Do not treat
it as live field evidence or as a field FWI/3D readiness signal.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest.py
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_validator.py
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_metadata_template_bundle_manifest_validation_sensitivity.py

9 passed
```

Figure validation:

```text
2356x868, dynamic range=255
```

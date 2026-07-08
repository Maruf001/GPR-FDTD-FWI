# Field Experiment 499: Controlled Collection Live Receipt Collection-Day Per-File Metadata Template-Pack Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `498` per-file metadata template-pack validator.

The sensitivity run mutates the validated template artifacts in memory and
checks whether the validator rejects damaged states. The damage cases cover
template identity, paired DZT identity, required receipt checks, template
creation flags, placeholder counts, measured-DZT dependency, live-receipt
promotion, field-FWI promotion, figure damage, and missing script snapshots.

This is a CPU-only artifact sensitivity run. It does not create live measured
files, parse DZT data, promote measured evidence, run provenance acceptance,
build an archive, launch field FWI, launch GPU work, or start field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/499_gssi51600s_controlled_collection_live_receipt_collection_day_per_file_metadata_template_pack_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_per_file_metadata_template_pack_validation_sensitivity_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_per_file_metadata_template_pack_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_per_file_metadata_template_pack_validation_sensitivity.png
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
| template row removed | fail | fail |
| metadata identity damaged | fail | fail |
| paired DZT identity damaged | fail | fail |
| required check damaged | fail | fail |
| template written flag damaged | fail | fail |
| template key count damaged | fail | fail |
| placeholder count damaged | fail | fail |
| measured-DZT dependency removed | fail | fail |
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

The validator is not only passing the current artifact set. It also rejects the
important failure modes that would make the per-file metadata templates look
like real field receipt files or allow incomplete measured-file dependencies to
promote downstream readiness.

## Decision

Keep the per-file metadata templates as post-measurement preparation artifacts.
The field stream still needs real measured DZT files and completed metadata in
the live external return path before receipt, parser, provenance, archive,
field FWI, or field 3D/HPC can proceed.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_per_file_metadata_template_pack.py
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_per_file_metadata_template_pack_validator.py
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_per_file_metadata_template_pack_validation_sensitivity.py

9 passed
```

Figure validation:

```text
2356x871, dynamic range=255
```

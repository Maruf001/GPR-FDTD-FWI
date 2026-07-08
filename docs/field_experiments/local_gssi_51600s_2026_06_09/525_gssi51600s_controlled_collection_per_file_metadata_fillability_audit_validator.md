# Field Experiment 525: Per-File Metadata Fillability Audit Validator

Date: 2026-06-30

## Purpose

Validate run `524`, the per-file metadata fillability audit for the controlled
collection return packet.

This is an output-local validation wrapper around saved run `524` artifacts. It
does not create live field receipt files, parse DZT files, promote controlled
field evidence, run field FWI, launch GPU/HPC work, or run field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/525_gssi51600s_controlled_collection_per_file_metadata_fillability_audit_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_per_file_metadata_fillability_audit_validator_check_rows.csv
data/gssi51600s_controlled_collection_per_file_metadata_fillability_audit_validator_summary.json
figures/gssi51600s_controlled_collection_per_file_metadata_fillability_audit_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         6
passed checks:                             6
failed checks:                             0
per-file metadata rows:                    9
metadata field rows:                       36
measurement families:                      3
files requiring measured DZT:              9
paired DZT live files present:             0
metadata live files present:               0
field values ready:                        0
field FWI ready:                           false
field 3D/HPC ready:                        false
validation ready:                          true
```

The checks cover source readiness, metadata/field/family shape, family
accounting, measured-DZT dependency preservation, downstream boundary
preservation, figure output, and frozen script snapshots.

## Interpretation

Run `524` validates as a post-measurement preparation artifact.

## Decision

Use run `524` to structure per-file metadata entry after measured DZT receipt.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_per_file_metadata_fillability_audit.py
tests/test_gssi_field_controlled_collection_per_file_metadata_fillability_audit_validator.py
tests/test_gssi_field_controlled_collection_per_file_metadata_fillability_audit_validation_sensitivity.py
9 passed
```

Figure check:

```text
2357x836, dynamic range=255
```


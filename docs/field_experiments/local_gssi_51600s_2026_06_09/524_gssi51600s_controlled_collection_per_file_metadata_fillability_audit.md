# Field Experiment 524: Per-File Metadata Fillability Audit

Date: 2026-06-30

## Purpose

Expand the nine post-measurement per-file metadata templates into a
family-level and field-level fillability audit.

This run answers:

```text
What must be filled after each measured DZT file is returned?
```

This is an output-local preparation audit. It does not create live field
receipt files, parse DZT files, promote controlled field evidence, run field
FWI, launch GPU/HPC work, or run field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/524_gssi51600s_controlled_collection_per_file_metadata_fillability_audit
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_per_file_metadata_fillability_audit_metadata_rows.csv
data/gssi51600s_controlled_collection_per_file_metadata_fillability_audit_metadata_field_rows.csv
data/gssi51600s_controlled_collection_per_file_metadata_fillability_audit_family_rows.csv
data/gssi51600s_controlled_collection_per_file_metadata_fillability_audit_summary.json
figures/gssi51600s_controlled_collection_per_file_metadata_fillability_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
per-file metadata rows:                    9
metadata field rows:                       36
measurement families:                      3
controlled profile metadata files:         3
time-zero metadata files:                  3
amplitude-reference metadata files:        3
files requiring measured DZT:              9
paired DZT live files present:             0
metadata live files present:               0
metadata receipt-ready files:              0
field values ready:                        0
required receipt checks:                   54
template value placeholders:               36
field FWI ready:                           false
field 3D/HPC ready:                        false
fillability audit ready:                   true
```

Family table:

| Measurement family | Metadata files | Required fields | Receipt checks | DZT files present | Metadata files present |
| --- | ---: | ---: | ---: | ---: | ---: |
| controlled profile repeat | 3 | 12 | 18 | 0 | 0 |
| time-zero reference | 3 | 12 | 18 | 0 | 0 |
| amplitude reference | 3 | 12 | 18 | 0 | 0 |

Each per-file metadata JSON needs four post-measurement values:

```text
acquisition_file_sha256
trace_count
time_zero_pick_ns
notes
```

## Interpretation

All nine per-file metadata files remain post-measurement items because each one
depends on its paired measured DZT file. The templates are useful for
collection preparation, but none of them is live evidence or receipt-ready.

## Decision

Use this audit to structure per-file metadata entry after measured DZT receipt.
Keep live receipt, parser/provenance/archive readiness, field FWI, and field
3D/HPC blocked until real DZT and metadata files are returned.

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
2572x842, dynamic range=255
```


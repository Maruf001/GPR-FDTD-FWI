# Field Experiment 263: Controlled Collection Real-Return Empty Intake Layout

Date: 2026-06-28

## Purpose

Materialize an empty intake directory layout for the real measured files
required by run `260`.

This run creates directories and CSV templates only. It does not create
placeholder DZT files, fabricate metadata, accept an archive, promote controlled
field evidence, run field FWI, launch field 3D/HPC, or use GPU work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/263_gssi51600s_controlled_collection_real_return_empty_intake_layout
```

Key artifacts:

```text
return_inbox/README.md
return_inbox/metadata/global_metadata_template.csv
return_inbox/metadata/file_metadata_template.csv
return_inbox/checksums/checksum_template.csv
data/field_controlled_collection_real_return_empty_intake_required_files.csv
data/field_controlled_collection_real_return_empty_intake_layout_summary.json
figures/field_controlled_collection_real_return_empty_intake_layout.png
docs/FIELD_CONTROLLED_COLLECTION_REAL_RETURN_EMPTY_INTAKE_LAYOUT.md
scripts/run_gssi_field_controlled_collection_real_return_empty_intake_layout.py
scripts/test_gssi_field_controlled_collection_real_return_empty_intake_layout.py
scripts/script_snapshot_manifest.json
```

## Result

```text
directories expected:                   6
directories created:                    6
required file slots:                    9
global metadata template rows:         11
file metadata template rows:           21
checksum template rows:                 9
acceptance gates:                       7
placeholder DZT files created:          0
empty intake layout ready:           true
real files present:                  false
provenance acceptance ready:         false
real archive acceptance ready:       false
controlled field evidence ready:     false
field FWI ready:                     false
field 3D/HPC ready:                  false
gpu priority:                        none
```

## Interpretation

The real-return staging contract now has a concrete empty inbox: required
directories, required-file manifest, global metadata template, per-file
metadata template, checksum template, and gate visibility are present. No
placeholder DZT files were created, so real files and measured metadata remain
required.

## Decision

Use run `263` as the empty intake layout for future controlled collection
returns. Do not promote provenance, archive acceptance, controlled field
evidence, field FWI, field 3D/HPC, or GPU work until real files, metadata, and
checksums are staged and validated.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_empty_intake_layout.py
3 passed
```

Figure validation:

```text
2825x844, dynamic range=255
```

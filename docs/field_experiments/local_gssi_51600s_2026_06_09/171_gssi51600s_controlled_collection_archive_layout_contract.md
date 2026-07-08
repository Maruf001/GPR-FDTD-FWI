# Field Experiment 171: Controlled Collection Archive Layout Contract

Date: 2026-06-25

## Purpose

Define the archive folder layout for future real controlled-collection files
and metadata.

This is CPU-only collection logistics. It does not create measured field
evidence, copy DZT files, run DZT preprocessing, launch field FWI, use GPU/HPC,
or train neural networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/171_gssi51600s_controlled_collection_archive_layout_contract
```

Key artifacts:

```text
data/field_controlled_collection_archive_file_layout.csv
data/field_controlled_collection_archive_metadata_artifacts.csv
data/field_controlled_collection_archive_directories.csv
data/field_controlled_collection_archive_command_templates.csv
data/field_controlled_collection_archive_layout_contract_summary.json
figures/field_controlled_collection_archive_layout_contract.png
docs/FIELD_COLLECTION_ARCHIVE_LAYOUT_CONTRACT.md
```

## Result

```text
real file layout rows:              9
metadata artifact rows:             6
archive directories:                7
command templates:                  31
controlled profile files:           3
time-zero reference files:          3
amplitude reference files:          3
ready for collection-day use:       true
ready for provenance acceptance:    false
ready for structural rerun:         false
field FWI ready:                    false
GPU/HPC ready:                      false
```

Archive root template:

```text
controlled_collection_<YYYYMMDD>_<session_id>
```

Real-file layout:

```text
raw/profiles/controlled_profile_repeat_01.DZT
raw/profiles/controlled_profile_repeat_02.DZT
raw/profiles/controlled_profile_repeat_03.DZT
raw/references/time_zero/time_zero_reference_01.DZT
raw/references/time_zero/time_zero_reference_02.DZT
raw/references/time_zero/time_zero_reference_03.DZT
raw/references/amplitude/amplitude_reference_01.DZT
raw/references/amplitude/amplitude_reference_02.DZT
raw/references/amplitude/amplitude_reference_03.DZT
```

Metadata artifacts:

```text
metadata/session_log.csv
metadata/target_truth.csv
metadata/profile_geometry.csv
metadata/intake_manifest.csv
metadata/checksum_ledger.csv
metadata/provenance_notes.md
```

## Interpretation

The real controlled-collection files now have a deterministic archive-layout
contract. This reduces collection-day path ambiguity and gives the checksum,
intake, structural, and provenance gates stable paths to refer to.

This does not create measured field evidence. The layout must still be filled
with real files and real metadata.

## Decision

Use this layout when real files are archived. Keep provenance acceptance,
structural rerun, field FWI, heavy GPU work, field 3D/HPC, and neural-network
training blocked until real files and metadata fill this layout and pass
checksum, intake, structural, and provenance gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_archive_layout_contract.py
3 passed
```

Figure check:

```text
1888x807, dynamic range=255
```

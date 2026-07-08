# Field Experiment 239: Controlled Archive Real Return Archive Skeleton Pack

Date: 2026-06-28

## Purpose

Create an empty archive skeleton for future measured real-return files.

Run `236` defined the guarded real-return intake contract. This run turns that
contract into a concrete empty directory/template pack so real measured files
can later be staged at the expected paths without creating fake DZT files.

It creates directories and blank CSV templates only. It does not create
placeholder DZT files, contain real measured files, accept an archive, run
field FWI, launch GPU/HPC work, or promote field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/239_gssi51600s_controlled_archive_real_return_archive_skeleton_pack
```

Key artifacts:

```text
templates/real_return_archive_root/
templates/REAL_RETURN_ARCHIVE_README.md
data/field_controlled_archive_real_return_expected_files.csv
data/field_controlled_archive_real_return_blank_signoff.csv
data/field_controlled_archive_real_return_provenance_placeholders.csv
data/field_controlled_archive_real_return_template_directories.csv
data/field_controlled_archive_real_return_archive_skeleton_pack_summary.json
figures/field_controlled_archive_real_return_archive_skeleton_pack.png
```

## Result

```text
expected files:                     9
template directories:               3
blank signoff rows:                 9
provenance placeholder rows:        6
placeholder files created:          0
skeleton ready:                     true
real files present:                 false
real signoff values present:        false
provenance acceptance ready:        false
checksum intake ready:              false
controlled evidence ready:          false
real archive acceptance ready:      false
field FWI ready:                    false
field 3D/HPC ready:                 false
```

Created archive-root directories:

```text
raw/profiles
raw/references/amplitude
raw/references/time_zero
```

No files were created inside `templates/real_return_archive_root/`.

## Interpretation

The future real-return archive now has a concrete empty directory skeleton and
blank collection templates. No fake DZT placeholders were created; real archive
acceptance remains blocked until measured files and measured metadata are
staged.

## Decision

Use run `239` as the directory/template pack for future measured field returns.
Do not treat the empty skeleton as real field evidence.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_real_return_archive_skeleton_pack.py
5 passed
```

Figure validation:

```text
figures/field_controlled_archive_real_return_archive_skeleton_pack.png
2644x843, dynamic range=255
```

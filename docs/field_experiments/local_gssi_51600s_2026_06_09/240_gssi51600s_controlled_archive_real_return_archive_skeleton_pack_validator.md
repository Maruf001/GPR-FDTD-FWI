# Field Experiment 240: Controlled Archive Real Return Archive Skeleton Pack Validator

Date: 2026-06-28

## Purpose

Validate the run `239` empty archive skeleton pack from a consumer perspective.

Run `239` created a directory and template pack for future measured field
returns. This validator checks that it has the expected directories, blank
templates, no placeholder files, and blocked real archive/downstream states.

It does not create placeholder DZT files, contain real measured files, accept
an archive, run field FWI, launch GPU/HPC work, or promote field evidence.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/240_gssi51600s_controlled_archive_real_return_archive_skeleton_pack_validator
```

Key artifacts:

```text
data/field_controlled_archive_real_return_archive_skeleton_pack_validator_checks.csv
data/field_controlled_archive_real_return_archive_skeleton_pack_validator_summary.json
figures/field_controlled_archive_real_return_archive_skeleton_pack_validator.png
docs/FIELD_CONTROLLED_ARCHIVE_REAL_RETURN_ARCHIVE_SKELETON_PACK_VALIDATOR.md
scripts/run_gssi_field_controlled_archive_real_return_archive_skeleton_pack_validator.py
scripts/test_gssi_field_controlled_archive_real_return_archive_skeleton_pack_validator.py
```

## Result

```text
validation checks:                  5
validation passes:                  5
blocking failures:                  0
validation ready:                   true
source expected files:              9
source template directories:        3
real files present:                 false
real signoff values present:        false
provenance acceptance ready:        false
checksum intake ready:              false
controlled evidence ready:          false
real archive acceptance ready:      false
field FWI ready:                    false
field 3D/HPC ready:                 false
```

The validator checks:

| Check | Result |
| --- | --- |
| Skeleton summary counts are consistent | pass |
| Template directories are expected and empty | pass |
| Expected file rows are slots not fake files | pass |
| Blank signoff and provenance templates are not accepted | pass |
| Real archive and downstream states blocked | pass |

## Interpretation

The archive skeleton pack is internally consistent: it has the expected
directories, blank templates, no placeholder files, and blocked real
archive/downstream states.

## Decision

Use run `240` as the positive validator for the empty real-return archive
skeleton. Sensitivity remains required before treating the skeleton pack as
fully guarded.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_real_return_archive_skeleton_pack_validator.py
5 passed
```

Figure validation:

```text
figures/field_controlled_archive_real_return_archive_skeleton_pack_validator.png
2645x830, dynamic range=255
```

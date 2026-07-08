# Field Experiment 221: Controlled Archive Operator Manifest Pack

Date: 2026-06-28

## Purpose

Turn the controlled-archive execution packet, command-plan templates, and
real-intake boundary into one operator-facing manifest pack.

This run answers a practical field-side question:

```text
What exact files, archive paths, and intake checks must be satisfied before the
controlled archive can move beyond the current dry-run state?
```

This is CPU-only synthesis. It does not ingest real field files, execute shell
commands, accept a real archive, run field FWI, launch GPU/HPC work, or run
field 3D validation.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/221_gssi51600s_controlled_archive_operator_manifest_pack
```

Key artifacts:

```text
data/field_controlled_archive_operator_manifest_file_rows.csv
data/field_controlled_archive_operator_manifest_directory_rows.csv
data/field_controlled_archive_operator_manifest_check_rows.csv
data/field_controlled_archive_operator_manifest_pack_summary.json
figures/field_controlled_archive_operator_manifest_pack.png
docs/FIELD_CONTROLLED_ARCHIVE_OPERATOR_MANIFEST_PACK.md
```

## Result

```text
operator file slots:               9
archive directories:               3
planned acceptance checks:          27
checks per file slot:               3
controlled profile files:           3
time-zero reference files:          3
amplitude reference files:          3
DZT minimum size bytes:             65536
GSSI DZT header prefix:             ff07
real-intake boundary items:         9
real acceptance blockers:           7
collection-day execution ready:     true
evaluator contract ready:           true
operator manifest pack ready:       true
ready for operator collection:      true
real files present:                 false
commands executed:                  false
real archive acceptance ready:      false
checksum intake ready:              false
controlled evidence ready:          false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

The manifest keeps the file requirements explicit:

| Role | Files | Archive directory |
| --- | ---: | --- |
| controlled profile repeat | 3 | `raw/profiles` |
| time-zero reference | 3 | `raw/references/time_zero` |
| amplitude reference | 3 | `raw/references/amplitude` |

Each file has three planned intake checks:

| Check group | Count | Meaning |
| --- | ---: | --- |
| file exists | 9 | file must exist at the expected archive path |
| DZT signature guard | 9 | file must meet the DZT size/header rule |
| SHA-256 checksum | 9 | file must have a recorded checksum |

## Interpretation

The field side now has a single manifest for the nine real DZT files: three
controlled profile repeats, three time-zero references, and three amplitude
references. The required archive paths and planned intake checks are fixed.

This is a collection and intake manifest, not measured field evidence. The
archive still needs real files and measured provenance values before acceptance.

## Decision

Use run `221` as the current collection and archive-intake manifest pack. Keep
real archive acceptance, checksum intake, controlled evidence, field FWI, GPU
work, and field 3D/HPC blocked until real measured files are placed at these
paths and all checks pass.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_operator_manifest_pack.py
5 passed
```

Compile check:

```text
run_gssi_field_controlled_archive_operator_manifest_pack.py: pass
tests/test_gssi_field_controlled_archive_operator_manifest_pack.py: pass
```

Figure check:

```text
field_controlled_archive_operator_manifest_pack.png
3076x865, dynamic range=255
```

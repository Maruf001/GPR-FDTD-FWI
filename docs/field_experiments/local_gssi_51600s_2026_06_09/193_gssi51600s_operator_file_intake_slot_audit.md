# Field Experiment 193: Operator File Intake Slot Audit

Date: 2026-06-27

## Purpose

Audit the concrete real-file intake slots in the controlled-collection operator
worksheet.

Runs `187` through `192` showed that the current archive is useful as QC
context only and that field FWI remains blocked until nine real measured files,
11 metadata items, and all checksum/intake/structural/provenance gates pass.
This run checks whether the nine required real files already have unique,
role-correct intake slots for collection-day handoff.

This is a CPU-only worksheet audit. It does not create real measured files,
close metadata gaps, run field FWI, launch GPU/HPC work, run field 3D, or
train neural networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/193_gssi51600s_operator_file_intake_slot_audit
```

Key artifacts:

```text
data/field_operator_file_intake_slot_rows.csv
data/field_operator_file_intake_slot_checks.csv
data/field_operator_file_intake_slot_audit_summary.json
figures/field_operator_file_intake_slot_audit.png
docs/FIELD_OPERATOR_FILE_INTAKE_SLOT_AUDIT.md
scripts/run_gssi_field_operator_file_intake_slot_audit.py
scripts/test_gssi_field_operator_file_intake_slot_audit.py
```

## Result

```text
file slots:                         9
controlled profile repeat slots:    3
time-zero reference slots:           3
amplitude-reference slots:          3
unique archive paths:               9
checksum template slots:            9
ledger-ready template slots:        9
slot audit checks:                  13
slot audit passes:                  13
blocking failures:                  0
file-intake slot template ready:    true
real files present:                 false
checksum preflight ready:           false
controlled evidence ready:          false
real archive acceptance ready:      false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

Slot checks:

| Check | Status | Detail |
| --- | --- | --- |
| file_slots_nonempty | pass | 9 file slots |
| file_slot_count_matches_required | pass | 9 slots / 9 required files |
| required_role_counts_match | pass | controlled profile repeats = 3, time-zero references = 3, amplitude references = 3 |
| manifest_ids_unique | pass | 9 unique / 9 total |
| target_artifacts_unique | pass | 9 unique / 9 total |
| archive_paths_unique | pass | 9 unique / 9 total |
| all_slots_are_dzt_files | pass | 9 DZT slots |
| archive_prefixes_match_roles | pass | 9 prefix matches |
| copy_and_checksum_templates_point_to_archive_paths | pass | 9 template pairs |
| ledger_fields_present_for_all_slots | pass | 9 ledger-ready slots |
| all_slots_block_field_fwi_if_missing | pass | 9 blocking slots |
| current_archive_not_reused_as_controlled_file | pass | 0 file gaps allow current-archive reuse |
| staged_completion_still_blocks_field_fwi | pass | real files and gate reruns still absent |

## Interpretation

The operator worksheet has a clean nine-slot real-file intake template: three
controlled profile repeats, three time-zero references, and three amplitude
references. Each slot has a unique archive path, copy/checksum command
template, required ledger fields, and field-FWI blocking status.

This improves the collection-day handoff but does not supply real measured
files. The current archive is still QC context only.

## Decision

Use this slot table as the checksum/intake handoff map. Keep controlled
evidence, real archive acceptance, field FWI, GPU work, and field 3D/HPC
blocked until the nine real files are collected, hashed, recorded, and the
checksum/intake/structural/provenance gates pass.

## Validation

Focused tests:

```text
tests/test_gssi_field_operator_file_intake_slot_audit.py
6 passed
```

Figure validation:

```text
field_operator_file_intake_slot_audit.png
2896x864, dynamic range=255
```

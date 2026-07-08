# Field Experiment 195: Operator Slot And Checksum Ledger Consistency Audit

Date: 2026-06-27

## Purpose

Check whether the run `193` operator file-intake slots match the older run
`168` checksum ledger template.

Run `193` created a concrete nine-slot file handoff map. Run `168` already
created the checksum ledger template for the same nine real files. This run
verifies that the two artifacts are consistent, so the existing ledger can be
reused rather than duplicated.

This is a CPU-only consistency audit. It does not create real measured files,
close metadata gaps, run field FWI, launch GPU/HPC work, run field 3D, or
train neural networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/195_gssi51600s_operator_slot_checksum_ledger_consistency_audit
```

Key artifacts:

```text
data/field_operator_slot_checksum_ledger_consistency_rows.csv
data/field_operator_slot_checksum_ledger_consistency_checks.csv
data/field_operator_slot_checksum_ledger_consistency_audit_summary.json
figures/field_operator_slot_checksum_ledger_consistency_audit.png
docs/FIELD_OPERATOR_SLOT_CHECKSUM_LEDGER_CONSISTENCY_AUDIT.md
scripts/run_gssi_field_operator_slot_checksum_ledger_consistency_audit.py
scripts/test_gssi_field_operator_slot_checksum_ledger_consistency_audit.py
```

## Result

```text
joined manifest rows:              9
consistency checks:                9
consistency passes:                9
blocking failures:                 0
slot-ledger consistency ready:     true
real files present:                false
controlled evidence ready:         false
real archive acceptance ready:     false
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

Consistency checks:

| Check | Status | Detail |
| --- | --- | --- |
| slot_and_ledger_rows_nonempty | pass | 9 slots / 9 ledger rows |
| slot_and_ledger_row_counts_match | pass | 9 slots / 9 ledger rows / 9 joined rows |
| manifest_ids_match | pass | 9 shared ids |
| file_roles_match | pass | 9 matching roles |
| target_filenames_match | pass | 9 matching filenames |
| closure_groups_match | pass | 9 matching groups |
| pending_status_matches | pass | 9 pending rows |
| ledger_commands_name_expected_files | pass | 9 command rows |
| blocking_flags_match | pass | 9 blocking rows |

## Interpretation

The operator file-slot map and checksum ledger template are consistent. They
contain the same nine manifest IDs, roles, filenames, closure groups, pending
statuses, checksum command targets, and blocking flags.

## Decision

Reuse the existing checksum ledger with the run `193` slot map. Keep controlled
evidence, real archive acceptance, field FWI, GPU work, and field 3D/HPC
blocked until real files are collected, hashed, recorded, and all gates pass.

## Validation

Focused tests:

```text
tests/test_gssi_field_operator_slot_checksum_ledger_consistency_audit.py
4 passed
```

Figure validation:

```text
field_operator_slot_checksum_ledger_consistency_audit.png
2249x839, dynamic range=255
```

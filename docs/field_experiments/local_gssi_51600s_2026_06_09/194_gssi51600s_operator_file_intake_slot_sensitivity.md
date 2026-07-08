# Field Experiment 194: Operator File Intake Slot Sensitivity

Date: 2026-06-27

## Purpose

Stress-test the run `193` file-intake slot audit with controlled worksheet
mutations.

Run `193` showed that the operator worksheet has a clean nine-slot real-file
handoff map. This run checks that the audit rejects practical damaged-template
cases before any real collection-day data are accepted.

This is a CPU-only sensitivity smoke. It does not create real measured files,
close metadata gaps, run field FWI, launch GPU/HPC work, run field 3D, or
train neural networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/194_gssi51600s_operator_file_intake_slot_sensitivity
```

Key artifacts:

```text
data/field_operator_file_intake_slot_sensitivity_rows.csv
data/field_operator_file_intake_slot_sensitivity_summary.json
figures/field_operator_file_intake_slot_sensitivity.png
docs/FIELD_OPERATOR_FILE_INTAKE_SLOT_SENSITIVITY.md
scripts/run_gssi_field_operator_file_intake_slot_sensitivity.py
scripts/test_gssi_field_operator_file_intake_slot_sensitivity.py
```

## Result

```text
scenarios:                         6
expected passes:                   1
expected failures:                 5
observed passes:                   1
observed failures:                 5
unexpected outcomes:               0
slot sensitivity ready:            true
file-intake slot template ready:   true
real files present:                false
controlled evidence ready:         false
real archive acceptance ready:     false
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

Scenario results:

| Scenario | Expected pass | Observed pass | Failing checks |
| --- | --- | --- | --- |
| exact_slot_template | true | true | none |
| missing_profile_slot | false | false | file_slot_count_matches_required; required_role_counts_match |
| duplicate_archive_path | false | false | archive_paths_unique |
| wrong_time_zero_prefix | false | false | archive_prefixes_match_roles |
| missing_ledger_field | false | false | ledger_fields_present_for_all_slots |
| current_archive_reuse_allowed | false | false | current_archive_not_reused_as_controlled_file |

## Interpretation

The file-intake slot audit behaves as expected. The exact template passes.
Removing a profile slot, duplicating an archive path, placing a time-zero file
under the wrong archive prefix, removing ledger fields, or allowing current
archive reuse all fail validation.

This validates the handoff map as a guard. It still does not supply the nine
real measured files or the metadata required for controlled evidence.

## Decision

Use this sensitivity smoke as the guard for the run `193` file-intake handoff
map. Keep controlled evidence, real archive acceptance, field FWI, GPU work,
and field 3D/HPC blocked until real files and gates pass.

## Validation

Focused tests:

```text
tests/test_gssi_field_operator_file_intake_slot_sensitivity.py
4 passed
```

Figure validation:

```text
field_operator_file_intake_slot_sensitivity.png
2861x842, dynamic range=255
```

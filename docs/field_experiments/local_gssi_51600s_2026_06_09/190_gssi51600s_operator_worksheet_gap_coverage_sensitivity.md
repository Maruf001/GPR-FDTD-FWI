# Field Experiment 190: Operator Worksheet Gap Coverage Sensitivity

Date: 2026-06-27

## Purpose

Check whether the run `189` worksheet coverage audit catches missing and stale
worksheet rows.

Run `189` showed that the current operator worksheet covers all six current
gap-matrix groups. This run mutates the worksheet and asks:

```text
Does the coverage audit fail when important worksheet rows are removed,
misclassified, or stale?
```

This is a CPU-only sensitivity smoke. It does not promote current files to
controlled evidence, run field FWI, launch GPU/HPC work, run field 3D, or train
neural networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/190_gssi51600s_operator_worksheet_gap_coverage_sensitivity
```

Key artifacts:

```text
data/field_operator_worksheet_gap_coverage_sensitivity_rows.csv
data/field_operator_worksheet_gap_coverage_sensitivity_summary.json
figures/field_operator_worksheet_gap_coverage_sensitivity.png
docs/FIELD_OPERATOR_WORKSHEET_GAP_COVERAGE_SENSITIVITY.md
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                  5
expected passes:            1
expected failures:          4
observed passes:            1
observed failures:          4
unexpected outcomes:        0
sensitivity smoke ready:    true
controlled evidence ready:  false
real archive ready:         false
field FWI ready:            false
field 3D/HPC ready:         false
gpu priority:               none
```

Scenario rows:

| Scenario | Expected pass | Observed pass | Matches |
| --- | --- | --- | --- |
| exact_control | true | true | true |
| missing_profile_file_row | false | false | true |
| missing_session_metadata_group | false | false | true |
| stale_unmapped_role_row | false | false | true |
| time_zero_role_misclassified | false | false | true |

## Interpretation

The sensitivity smoke behaves as expected. The exact worksheet passes. Removing
a required profile-file row, removing a metadata group, adding a stale unmapped
row, or misclassifying a time-zero row causes the coverage audit to fail.

This strengthens the worksheet coverage audit itself. It does not close the
real-data evidence gap.

## Decision

Use run `190` as the sensitivity guard for the field worksheet coverage audit.
Controlled evidence, real archive acceptance, field FWI, GPU work, and field
3D/HPC remain blocked until real measured files and metadata pass the gates.

## Validation

Focused test:

```text
tests/test_gssi_field_operator_worksheet_gap_coverage_sensitivity.py
5 passed
```

Figure validation:

```text
field_operator_worksheet_gap_coverage_sensitivity.png
2285x847, dynamic range=255
```

Script snapshots:

```text
run_gssi_field_operator_worksheet_gap_coverage_sensitivity.py
sha256=ff11f6ec7a22a6f3a3b6891de9276c14baba7ecb6486db0c40c0f15a61f64f12

tests/test_gssi_field_operator_worksheet_gap_coverage_sensitivity.py
sha256=c486d17a457a46632d65a53637c1c7942de63f0a18ac6716596d11c09007af95
```

# Field Experiment 189: Operator Worksheet Gap Coverage Audit

Date: 2026-06-27

## Purpose

Check whether the operator worksheet from run `177` still covers the current
current-to-controlled gap matrix from runs `187` and `188`.

This run asks:

```text
Is the existing collection-day worksheet still complete for the latest field
gap matrix?
```

This is a CPU-only audit. It does not promote current files to controlled
evidence, run field FWI, launch GPU/HPC work, run field 3D, or train neural
networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/189_gssi51600s_operator_worksheet_gap_coverage_audit
```

Key artifacts:

```text
data/field_operator_worksheet_gap_coverage_rows.csv
data/field_operator_worksheet_gap_coverage_audit_summary.json
figures/field_operator_worksheet_gap_coverage_audit.png
docs/FIELD_OPERATOR_WORKSHEET_GAP_COVERAGE_AUDIT.md
scripts/script_snapshot_manifest.json
```

## Result

```text
gap groups:                         6
covered gap groups:                 6
missing or stale gap groups:        0
file gap groups:                    3
metadata gap groups:                3
remaining required real files:      9
worksheet items:                    20
covered worksheet items:            20
unmapped worksheet items:           0
operator gate phases:               8
source gap matrix valid:            true
worksheet covers current gaps:      true
current archive QC context ready:   true
controlled evidence ready:          false
real archive acceptance ready:      false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

Coverage rows:

| Priority | Closure group | Gap status | Worksheet rows | Status |
| ---: | --- | --- | ---: | --- |
| 1 | session_metadata_real_values | open_metadata_gap | 8 | covered |
| 2 | target_truth_provenance | open_metadata_gap | 2 | covered |
| 3 | profile_geometry_provenance | open_metadata_gap | 1 | covered |
| 4 | acquisition_profile_files | open_file_gap | 3 | covered |
| 5 | time_zero_reference_files | open_file_gap | 3 | covered |
| 6 | amplitude_reference_files | open_file_gap | 3 | covered |

## Interpretation

The older 20-row operator worksheet still covers the latest current-to-controlled
gap matrix. It covers all six closure groups, all nine required real files, and
all 11 metadata rows. No worksheet rows are unmapped.

This is a handoff-quality result, not a data-acceptance result. The worksheet is
complete, but the real measured files and measured metadata are still absent.

## Decision

Keep using the run `177` worksheet as the collection-day operator worksheet.
Controlled evidence, measured-field claims, field FWI, GPU work, and field
3D/HPC remain blocked until the worksheet is filled with real data and the
archive, checksum, intake, structural, and provenance gates pass.

## Validation

Focused test:

```text
tests/test_gssi_field_operator_worksheet_gap_coverage_audit.py
4 passed
```

Figure validation:

```text
field_operator_worksheet_gap_coverage_audit.png
2860x847, dynamic range=255
```

Script snapshots:

```text
run_gssi_field_operator_worksheet_gap_coverage_audit.py
sha256=f028e11d37eb9ff030274e3937b9057521ab739ab578c428673a4bdf8ebb7434

tests/test_gssi_field_operator_worksheet_gap_coverage_audit.py
sha256=4ca71a32c9bf36910e6edd4931756c200d4bf595832a0e75324ca33add9d1aa8
```

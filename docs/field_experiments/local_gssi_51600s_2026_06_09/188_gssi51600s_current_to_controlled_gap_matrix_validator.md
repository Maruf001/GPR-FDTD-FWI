# Field Experiment 188: Current-To-Controlled Gap Matrix Validator

Date: 2026-06-27

## Purpose

Validate the run `187` current-to-controlled field gap matrix from a consumer
perspective.

This run does not relabel current files as controlled evidence, run field FWI,
launch GPU/HPC work, make a measured-field claim, or train neural networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/188_gssi51600s_current_to_controlled_gap_matrix_validator
```

Key artifacts:

```text
data/field_current_to_controlled_gap_matrix_validation_checks.csv
data/field_current_to_controlled_gap_matrix_validator_summary.json
figures/field_current_to_controlled_gap_matrix_validator.png
docs/FIELD_CURRENT_TO_CONTROLLED_GAP_MATRIX_VALIDATOR.md
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:             9
validation passes:             9
blocking failures:             0
gap matrix valid:              true
validated closure groups:      6
validated open metadata gaps:  3
validated open file gaps:      3
validated remaining files:     9
current archive QC ready:      true
controlled evidence ready:     false
measured-field claim ready:    false
field FWI ready:               false
field 3D/HPC ready:            false
gpu priority:                  none
```

Validation checks:

| Check | Status | Detail |
| --- | --- | --- |
| gap_matrix_rows_nonempty | pass | 6 rows |
| closure_group_count_matches_summary | pass | 6 observed / 6 summary |
| open_metadata_gap_count_matches_summary | pass | 3 observed / 3 summary |
| open_file_gap_count_matches_summary | pass | 3 observed / 3 summary |
| remaining_real_file_count_matches_summary | pass | 9 remaining files |
| no_current_file_promoted_to_controlled | pass | 0 promoted matrix rows |
| file_gaps_remain_open | pass | 0 file gaps have zero remaining files |
| qc_context_does_not_unlock_controlled_evidence | pass | QC context ready, controlled evidence blocked |
| no_field_fwi_or_3d_hpc_promotion | pass | field FWI and field 3D/HPC remain blocked |

## Interpretation

The run `187` gap matrix is internally consistent. All three metadata gaps and
all three file gaps remain open, nine real files remain required, and current
archive QC context does not unlock controlled evidence.

## Decision

Use run `188` as the consumer-side validator for the field gap matrix. Keep
measured-field claims, field FWI, heavy GPU work, field 3D/HPC, and
neural-network training blocked until the controlled archive is filled and
passes the gates.

## Validation

Focused test:

```text
tests/test_gssi_field_current_to_controlled_gap_matrix_validator.py
4 passed
```

Figure validation:

```text
field_current_to_controlled_gap_matrix_validator.png
1960x772, dynamic range=255
```

Script snapshots:

```text
run_gssi_field_current_to_controlled_gap_matrix_validator.py
sha256=ca945c800f97baa7e4a7ec7584bfc114a405ef3314a6d61c89d79ecee973bf9f

tests/test_gssi_field_current_to_controlled_gap_matrix_validator.py
sha256=c9b7f1339a3fbd5aa73b0d1e20bcdc50e250b79e10322cc978ed05e464bc6ac2
```

# Field Experiment 192: Operator Worksheet Staged Completion Validator

Date: 2026-06-27

## Purpose

Validate the run `191` staged-completion audit from a consumer perspective.

Run `191` showed that partial worksheet completion never reaches field-FWI
input readiness and that all rows still require checksum, intake, structural,
and provenance gate reruns before acceptance. This run validates those
conditions directly from the generated scenario table.

This is a CPU-only validation audit. It does not create real measured files,
close real metadata gaps, run field FWI, launch GPU/HPC work, run field 3D, or
train neural networks.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/192_gssi51600s_operator_worksheet_staged_completion_validator
```

Key artifacts:

```text
data/field_operator_worksheet_staged_completion_validation_checks.csv
data/field_operator_worksheet_staged_completion_validator_summary.json
figures/field_operator_worksheet_staged_completion_validator.png
docs/FIELD_OPERATOR_WORKSHEET_STAGED_COMPLETION_VALIDATOR.md
scripts/run_gssi_field_operator_worksheet_staged_completion_validator.py
scripts/test_gssi_field_operator_worksheet_staged_completion_validator.py
```

## Result

```text
validation checks:            7
validation passes:            7
blocking failures:            0
source scenarios:             7
source required files:        9
source required metadata:     11
partial scenarios ready:      0
staged completion valid:      true
controlled evidence ready:    false
real archive acceptance ready:false
field FWI ready:              false
```

Validation checks:

| Check | Status | Detail |
| --- | --- | --- |
| scenario_rows_nonempty | pass | 7 rows |
| row_count_matches_summary | pass | 7 observed / 7 summary |
| no_partial_scenario_ready | pass | 0 partial ready rows |
| all_rows_without_gate_rerun_blocked | pass | all worksheet rows need gate reruns before readiness |
| synthetic_full_completion_only_ready_row | pass | synthetic_full_completion_with_gate_pass ready row only |
| current_archive_not_promoted | pass | current archive remains QC context only |
| no_real_field_or_gpu_promotion | pass | real archive, field FWI, field 3D/HPC, and GPU remain blocked |

## Interpretation

The staged-completion map is consumer-valid. No partial completion scenario is
ready. A fully filled worksheet is still blocked until gate reruns pass. Only
the synthetic full-completion row with successful gate reruns reaches field-FWI
input readiness.

This validates the collection-day readiness logic without promoting the
current archive.

## Decision

Use run `192` as the consumer guard for the collection-day staged-completion
map. Keep the current archive as QC context only and keep real archive
acceptance, field FWI, GPU work, and field 3D/HPC blocked until real files and
metadata pass every gate.

## Validation

Focused tests:

```text
tests/test_gssi_field_operator_worksheet_staged_completion_validator.py
3 passed
```

Figure validation:

```text
field_operator_worksheet_staged_completion_validator.png
2249x839, dynamic range=255
```

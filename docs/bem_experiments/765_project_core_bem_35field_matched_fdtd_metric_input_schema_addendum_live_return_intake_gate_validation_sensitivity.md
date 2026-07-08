# BEM Experiment 765: Metric Addendum Intake Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `764` complex metric intake validator.

The sensitivity set checks that the exact saved intake state passes and that
damaged states fail when the source flag, file count, required row count, live
file count, acceptance state, missing-column count, comparison state, figure,
or script snapshot is changed.

This run does not use real BEM/FDTD values, run FDTD, make a real comparison
claim, run 3D validation, launch GPU/HPC work, transfer to field data, or run
field FWI.

## Output

```text
outputs/bem_experiments/765_project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_live_return_intake_gate_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_live_return_intake_gate_validation_sensitivity_scenario_rows.csv
data/project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_live_return_intake_gate_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_live_return_intake_gate_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:              true
scenarios:                           10
expected pass count:                 1
expected fail count:                 9
observed pass count:                 1
observed fail count:                 9
unexpected outcomes:                 0
damaged scenarios rejected:          9
gpu priority:                        none
```

Sensitivity scenarios:

| Scenario | Expected | Observed | First failed check |
| --- | --- | --- | --- |
| exact | pass | pass |  |
| source_not_ready | fail | fail | source intake gate ready |
| file_count_damage | fail | fail | five expected addendum files are represented |
| required_row_damage | fail | fail | required rows and cells are preserved |
| live_file_promotion | fail | fail | five expected addendum files are represented |
| false_acceptance | fail | fail | current state remains pre-return |
| missing_column_count_damage | fail | fail | missing columns are explicit while files are absent |
| comparison_promotion | fail | fail | real comparison remains blocked |
| figure_damage | fail | fail | figure and script snapshots are present |
| snapshot_damage | fail | fail | figure and script snapshots are present |

## Interpretation

The complex metric intake validator rejects the main failure modes that would
make incomplete or damaged addendum return files appear acceptable.

## Decision

Use runs `763-765` as the guarded complex metric intake block. Keep real
comparison, 3D validation, GPU/HPC, field transfer, and field FWI blocked until
all five complex metric files pass intake.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_live_return_intake_gate_validation_sensitivity.py
3 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_live_return_intake_gate_validation_sensitivity.py: pass
tests/test_project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_live_return_intake_gate_validation_sensitivity.py: pass
```

Figure check:

```text
2212x847, dynamic range=255
```

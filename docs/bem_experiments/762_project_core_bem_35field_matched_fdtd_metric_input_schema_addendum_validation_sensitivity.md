# BEM Experiment 762: Metric Input Schema Addendum Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `761` addendum validator.

The sensitivity set checks that the exact saved addendum state passes and that
damaged states fail when the source flag, file count, stage row shape, required
columns, required cell counts, filled/comparison state, figure, or script
snapshot is changed.

This run does not use real BEM/FDTD values, run FDTD, make a real comparison
claim, run 3D validation, launch GPU/HPC work, transfer to field data, or run
field FWI.

## Output

```text
outputs/bem_experiments/762_project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_validation_sensitivity_scenario_rows.csv
data/project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_validation_sensitivity.png
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
| source_not_ready | fail | fail | source addendum ready |
| file_count_damage | fail | fail | five addendum files are represented |
| stage_row_shape_damage | fail | fail | stage row shape covers all pairs |
| required_column_damage | fail | fail | all required columns are present in each addendum file |
| cell_count_damage | fail | fail | required cell counts are preserved |
| schema_filled_promotion | fail | fail | schema remains unfilled and comparison blocked |
| comparison_promotion | fail | fail | schema remains unfilled and comparison blocked |
| figure_damage | fail | fail | figure and script snapshots are present |
| snapshot_damage | fail | fail | figure and script snapshots are present |

## Interpretation

The addendum validator rejects the main failure modes that would make an
incomplete or damaged real numeric schema appear acceptable.

## Decision

Use runs `759-762` as the guarded real numeric return-schema block. Keep real
comparison, 3D validation, GPU/HPC, field transfer, and field FWI blocked until
the addendum files contain accepted real numeric values.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_validation_sensitivity.py
3 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_validation_sensitivity.py: pass
tests/test_project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_validation_sensitivity.py: pass
```

Figure check:

```text
2212x847, dynamic range=255
```

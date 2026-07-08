# BEM Experiment 758: Stage-1 Metric Definition Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `757` metric-definition validator.

The sensitivity set checks that the exact saved metric state passes and that
damaged states fail when the source flag, row count, phase formula, metric
maxima, real-value status, comparison status, strict row boundary, downstream
state, figure, or script snapshot is changed.

This run does not use real BEM/FDTD values, run FDTD, make a real comparison
claim, run 3D validation, launch GPU/HPC work, transfer to field data, or run
field FWI.

## Output

```text
outputs/bem_experiments/758_project_core_bem_35field_matched_fdtd_stage1_metric_definition_smoke_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_stage1_metric_definition_smoke_validation_sensitivity_scenario_rows.csv
data/project_core_bem_35field_matched_fdtd_stage1_metric_definition_smoke_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_stage1_metric_definition_smoke_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:              true
scenarios:                           11
expected pass count:                 1
expected fail count:                 10
observed pass count:                 1
observed fail count:                 10
unexpected outcomes:                 0
damaged scenarios rejected:          10
gpu priority:                        none
```

Sensitivity scenarios:

| Scenario | Expected | Observed | First failed check |
| --- | --- | --- | --- |
| exact | pass | pass |  |
| source_not_ready | fail | fail | source metric smoke ready |
| row_count_damage | fail | fail | synthetic rows remain synthetic |
| formula_damage | fail | fail | metric formulas recompute |
| metric_max_damage | fail | fail | metric maxima are preserved |
| real_value_promotion | fail | fail | synthetic rows remain synthetic |
| comparison_promotion | fail | fail | strict comparison boundary is preserved |
| strict_boundary_damage | fail | fail | strict comparison boundary is preserved |
| downstream_promotion | fail | fail | downstream states remain blocked |
| figure_damage | fail | fail | figure and script snapshots are present |
| snapshot_damage | fail | fail | figure and script snapshots are present |

## Interpretation

The metric validator is not only passing the exact saved state; it rejects the
main failure modes that would make a synthetic metric smoke look like real
BEM/FDTD comparison evidence.

## Decision

Use runs `756-758` as the synthetic-only metric-definition block before real
BEM/FDTD comparison. Keep real comparison, 3D validation, GPU/HPC, field
transfer, and field FWI blocked until all strict real-return files contain
accepted real numeric values.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_stage1_metric_definition_smoke_validation_sensitivity.py
3 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_stage1_metric_definition_smoke_validation_sensitivity.py: pass
tests/test_project_core_bem_35field_matched_fdtd_stage1_metric_definition_smoke_validation_sensitivity.py: pass
```

Figure check:

```text
2428x847, dynamic range=255
```

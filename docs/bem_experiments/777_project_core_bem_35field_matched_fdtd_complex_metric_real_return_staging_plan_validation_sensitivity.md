# BEM Experiment 777: Complex Metric Real-Return Staging Plan Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `776` staging-plan validator against controlled damaged
states.

This run does not create real solver-return files, does not stage files into
the live intake area, does not execute copy commands, does not accept template
files as real returns, and does not promote real BEM/FDTD comparison.

## Output

```text
outputs/bem_experiments/777_project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan_validation_sensitivity_scenario_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:       true
validation scenarios:         16
expected pass scenarios:      1
expected fail scenarios:      15
observed pass scenarios:      1
observed fail scenarios:      15
unexpected outcomes:          0
damaged scenarios:            15
damaged scenarios rejected:   15
gpu priority:                 none
```

Sensitivity scenarios:

| Scenario | Expected | Observed | Outcome |
| --- | --- | --- | --- |
| exact | pass | pass | expected |
| source not ready | fail | fail | expected |
| file count damage | fail | fail | expected |
| row count damage | fail | fail | expected |
| template copy allowed | fail | fail | expected |
| missing not-template guard | fail | fail | expected |
| real producer file promotion | fail | fail | expected |
| live file promotion | fail | fail | expected |
| ready-to-stage promotion | fail | fail | expected |
| executed command | fail | fail | expected |
| copy command damage | fail | fail | expected |
| action count damage | fail | fail | expected |
| ready action promotion | fail | fail | expected |
| real comparison promotion | fail | fail | expected |
| figure damage | fail | fail | expected |
| snapshot damage | fail | fail | expected |

## Interpretation

The staging-plan validator accepts the exact non-executed state and rejects
damaged source, count, template-copy, producer-file, live-file, execution,
action, comparison, figure, and script-snapshot states.

This closes the guarded BEM/FDTD complex metric real-return staging-plan block.
The next real comparison step remains external to this run: five real complex
metric CSV files must be produced, preflighted, staged, and then passed through
the live intake and comparison gates.

## Decision

Use runs `775-777` as the guarded BEM/FDTD complex metric real-return
staging-plan block. Keep real BEM/FDTD comparison blocked until all five real
CSV files are staged and accepted by the live intake gate.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan_validator.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan_validation_sensitivity.py
10 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan.py: pass
run_project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan_validator.py: pass
run_project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan_validation_sensitivity.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan_validator.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_staging_plan_validation_sensitivity.py: pass
```

Figure check:

```text
3040x855, dynamic range=255
```

# BEM Experiment 774: Complex Metric Real-Return Package Live Intake Reconciliation Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `773` validator for the BEM/FDTD complex metric live-intake
reconciliation table.

This run does not create real solver-return files, does not move templates into
the live intake area, does not accept template files as real returns, and does
not promote real BEM/FDTD comparison.

## Output

```text
outputs/bem_experiments/774_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation_validation_sensitivity_scenario_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:                true
validation scenarios:                  15
expected pass scenarios:               1
expected fail scenarios:               14
observed pass scenarios:               1
observed fail scenarios:               14
unexpected outcomes:                   0
damaged scenarios:                     14
damaged scenarios rejected:            14
gpu priority:                          none
```

Sensitivity scenarios:

| Scenario | Expected | Observed | Result |
| --- | --- | --- | --- |
| exact | pass | pass | expected |
| source not ready | fail | fail | expected |
| file count damage | fail | fail | expected |
| row count damage | fail | fail | expected |
| template missing | fail | fail | expected |
| blank value damage | fail | fail | expected |
| live parent damage | fail | fail | expected |
| live file promotion | fail | fail | expected |
| ready for intake promotion | fail | fail | expected |
| false file acceptance | fail | fail | expected |
| real return acceptance | fail | fail | expected |
| status split damage | fail | fail | expected |
| real comparison promotion | fail | fail | expected |
| figure damage | fail | fail | expected |
| snapshot damage | fail | fail | expected |

## Interpretation

The BEM/FDTD complex metric reconciliation validator accepts the exact saved
pre-return state and rejects damaged source, count, template, blank-value,
live-file, acceptance, comparison, figure, and snapshot states.

This closes the guarded BEM/FDTD complex metric live-intake reconciliation
block. The current physical next step remains external: all five real complex
metric CSV files must arrive and pass intake before real BEM/FDTD comparison
can proceed.

## Decision

Use runs `772-774` as the guarded BEM/FDTD complex metric live-intake
reconciliation block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation_validator.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation_validation_sensitivity.py
10 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation.py: pass
run_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation_validator.py: pass
run_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation_validation_sensitivity.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation_validator.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_live_intake_reconciliation_validation_sensitivity.py: pass
```

Figure check:

```text
2896x860, dynamic range=255
```

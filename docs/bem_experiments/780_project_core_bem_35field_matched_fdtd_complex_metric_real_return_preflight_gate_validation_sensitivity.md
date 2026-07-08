# BEM Experiment 780: Complex Metric Real-Return Preflight Gate Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `779` preflight-gate validator against controlled damaged
states.

This run does not create real solver-return files, does not stage files into
the live intake area, does not execute copy commands, does not accept template
files as real returns, and does not promote real BEM/FDTD comparison.

## Output

```text
outputs/bem_experiments/780_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate_validation_sensitivity_scenario_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:       true
validation scenarios:         15
expected pass scenarios:      1
expected fail scenarios:      14
observed pass scenarios:      1
observed fail scenarios:      14
unexpected outcomes:          0
damaged scenarios:            14
damaged scenarios rejected:   14
gpu priority:                 none
```

Sensitivity scenarios:

| Scenario | Expected | Observed | Outcome |
| --- | --- | --- | --- |
| exact | pass | pass | expected |
| source not ready | fail | fail | expected |
| file count damage | fail | fail | expected |
| row count damage | fail | fail | expected |
| required column damage | fail | fail | expected |
| required columns promotion | fail | fail | expected |
| producer file promotion | fail | fail | expected |
| observed row promotion | fail | fail | expected |
| row match promotion | fail | fail | expected |
| preflight passed promotion | fail | fail | expected |
| ready-to-stage promotion | fail | fail | expected |
| executed command | fail | fail | expected |
| real comparison promotion | fail | fail | expected |
| figure damage | fail | fail | expected |
| snapshot damage | fail | fail | expected |

## Interpretation

The preflight validator accepts the exact absent-producer state and rejects
damaged source, count, schema, producer-file, pass/readiness, execution,
comparison, figure, and script-snapshot states.

This closes the guarded BEM/FDTD complex metric real-return preflight block.
The next BEM/FDTD comparison state change must come from real producer CSV
files that pass the preflight gate.

## Decision

Use runs `778-780` as the guarded BEM/FDTD complex metric real-return preflight
block. Keep staging, live intake acceptance, and real comparison blocked until
all five producer CSV files pass preflight.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate_validator.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate_validation_sensitivity.py
9 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate.py: pass
run_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate_validator.py: pass
run_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate_validation_sensitivity.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate_validator.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate_validation_sensitivity.py: pass
```

Figure check:

```text
2824x860, dynamic range=255
```

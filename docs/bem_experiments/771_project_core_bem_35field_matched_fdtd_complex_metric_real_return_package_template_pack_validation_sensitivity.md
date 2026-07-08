# BEM Experiment 771: Complex Metric Real-Return Package Template Pack Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `770` validator for the BEM/FDTD complex metric
real-return template pack.

This run does not use real BEM values, does not use real FDTD exports, does not
accept templates as real returns, and does not promote real BEM/FDTD comparison.

## Output

```text
outputs/bem_experiments/771_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack_validation_sensitivity_scenario_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:               true
validation scenarios:                 13
expected pass scenarios:              1
expected fail scenarios:              12
observed pass scenarios:              1
observed fail scenarios:              12
unexpected outcomes:                  0
damaged scenarios:                    12
damaged scenarios rejected:           12
blank required value cells:           3348
gpu priority:                         none
```

Sensitivity scenarios:

| Scenario | Expected | Observed | Result |
| --- | --- | --- | --- |
| exact | pass | pass | expected |
| source not ready | fail | fail | expected |
| file count damage | fail | fail | expected |
| row count damage | fail | fail | expected |
| required column damage | fail | fail | expected |
| blank value damage | fail | fail | expected |
| pair id damage | fail | fail | expected |
| output location damage | fail | fail | expected |
| false acceptance | fail | fail | expected |
| real export promotion | fail | fail | expected |
| real comparison promotion | fail | fail | expected |
| figure damage | fail | fail | expected |
| snapshot damage | fail | fail | expected |

## Interpretation

The template-pack validator accepts the exact saved run `769` state and rejects
damaged source, count, schema, blank-value, identity, location,
false-acceptance, real-export, real-comparison, figure, and snapshot states.

This closes the producer-facing complex metric real-return template block. It
provides a concrete five-file return shape for future BEM/FDTD complex-valued
comparison while keeping real comparison blocked until measured solver exports
pass live intake.

## Decision

Use runs `769-771` as the guarded BEM/FDTD complex metric real-return
template-pack block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack_validator.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack_validation_sensitivity.py
12 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack.py: pass
run_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack_validator.py: pass
run_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack_validation_sensitivity.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack_validator.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_package_template_pack_validation_sensitivity.py: pass
```

Figure check:

```text
2716x861, dynamic range=255
```

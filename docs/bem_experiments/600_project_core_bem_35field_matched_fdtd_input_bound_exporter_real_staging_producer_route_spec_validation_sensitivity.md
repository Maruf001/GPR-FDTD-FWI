# BEM Experiment 600: Matched FDTD Input-Bound Exporter Real Staging Producer Route Spec Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the validator from run `599`.

This run checks that the validator accepts the exact run `598` route and
rejects damaged states that would change route shape, row counts, value fields,
file readiness, comparison readiness, downstream readiness, or artifacts.

## Output

```text
outputs/bem_experiments/600_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_spec_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_spec_validation_sensitivity_cases.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_spec_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_spec_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:        true
cases:                         16
expected pass cases:           1
expected fail cases:           15
actual pass cases:             1
actual fail cases:             15
unexpected outcomes:           0
damaged cases:                 15
real BEM/FDTD comparison ready: false
GPU/HPC ready:                 false
field transfer ready:          false
field FWI ready:               false
gpu priority:                  none
```

The damaged states cover source readiness removal, route removal, phase
removal, input/return route-count damage, input/return row-count damage,
value-field damage, file-presence promotion, file-acceptance promotion,
phase-readiness promotion, real-comparison promotion, GPU/HPC promotion, figure
damage, and script-snapshot damage.

## Interpretation

The route-spec validator is sensitive to the failure modes that would matter
before permitting real BEM/FDTD comparison.

## Decision

Use runs `598-600` as the current closed BEM/FDTD producer-route block. Keep
real BEM/FDTD comparison blocked until the full route passes acceptance.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_spec_validation_sensitivity.py

3 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```

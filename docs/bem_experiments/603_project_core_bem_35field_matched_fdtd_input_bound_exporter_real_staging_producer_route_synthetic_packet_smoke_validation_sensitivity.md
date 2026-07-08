# BEM Experiment 603: Matched FDTD Input-Bound Exporter Real Staging Producer Route Synthetic Packet Smoke Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the validator from run `602`.

This run checks that the validator accepts the exact run `601` synthetic packet
smoke and rejects damaged states that would change packet shape, row counts,
file acceptance, real-file status, evidence status, downstream readiness, or
artifacts.

## Output

```text
outputs/bem_experiments/603_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_synthetic_packet_smoke_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_synthetic_packet_smoke_validation_sensitivity_cases.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_synthetic_packet_smoke_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_synthetic_packet_smoke_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:         true
cases:                          16
expected pass cases:            1
expected fail cases:            15
actual pass cases:              1
actual fail cases:              15
unexpected outcomes:            0
damaged cases:                  15
real BEM/FDTD comparison ready: false
GPU/HPC ready:                  false
field transfer ready:           false
field FWI ready:                false
gpu priority:                   none
```

The damaged states cover source readiness removal, packet route removal,
input/return count damage, accepted-file count damage, accepted-row count
damage, validation-error promotion, packet-row acceptance failure, external
real-file promotion, real-evidence promotion, real-route readiness promotion,
real-comparison readiness promotion, GPU/HPC readiness promotion, figure
damage, and script-snapshot damage.

## Interpretation

The packet-smoke validator is sensitive to the failure modes that matter before
real BEM/FDTD comparison. It accepts only the exact non-evidence synthetic
packet state.

## Decision

Use runs `601-603` as the current closed producer-route synthetic-packet block.
Keep real BEM/FDTD comparison blocked until real external route files pass
acceptance.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_synthetic_packet_smoke_validation_sensitivity.py

3 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```

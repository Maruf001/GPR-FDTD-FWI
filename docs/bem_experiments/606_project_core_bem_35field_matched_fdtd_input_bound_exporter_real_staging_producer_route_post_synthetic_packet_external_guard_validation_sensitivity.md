# BEM Experiment 606: Matched FDTD Input-Bound Exporter Real Staging Producer Route Post-Synthetic Packet External Guard Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the validator from run `605`.

This run checks that the validator accepts the exact run `604` external guard
and rejects damaged states that would promote real external files, create
packet/external path overlap, place packet files under the external root,
promote real evidence, promote real BEM/FDTD comparison, promote downstream
readiness, or damage artifacts.

## Output

```text
outputs/bem_experiments/606_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_post_synthetic_packet_external_guard_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_post_synthetic_packet_external_guard_validation_sensitivity_cases.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_post_synthetic_packet_external_guard_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_post_synthetic_packet_external_guard_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:         true
cases:                          15
expected pass cases:            1
expected fail cases:            14
actual pass cases:              1
actual fail cases:              14
unexpected outcomes:            0
damaged cases:                  14
real BEM/FDTD comparison ready: false
GPU/HPC ready:                  false
field transfer ready:           false
field FWI ready:                false
gpu priority:                   none
```

The damaged states cover source readiness removal, guard-row removal, external
path-count damage, packet-file count damage, external-file presence or
acceptance promotion, packet/external path overlap, packet-under-external-root
promotion, packet-acceptance damage, packet real-evidence promotion,
real-comparison promotion, GPU/HPC promotion, figure damage, and
script-snapshot damage.

## Interpretation

The post-synthetic-packet external guard validator is sensitive to the failure
modes that would falsely promote synthetic packet files into real BEM/FDTD
staging evidence.

## Decision

Use runs `604-606` as the current closed post-synthetic-packet external guard
block. Keep real BEM/FDTD comparison blocked until actual external files are
supplied and accepted.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_post_synthetic_packet_external_guard_validation_sensitivity.py

3 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```

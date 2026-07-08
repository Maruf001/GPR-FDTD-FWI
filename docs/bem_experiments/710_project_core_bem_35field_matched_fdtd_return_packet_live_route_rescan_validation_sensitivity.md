# BEM Experiment 710: Matched BEM/FDTD Return-Packet Live Route Rescan Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `709` validator.

The validator should accept only the exact run `708` live-route state and
reject fake external files, fake file acceptance, changed route shape, changed
root blocker state, and downstream promotion.

## Output

```text
outputs/bem_experiments/710_project_core_bem_35field_matched_fdtd_return_packet_live_route_rescan_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_packet_live_route_rescan_validation_sensitivity_case_rows.csv
data/project_core_bem_35field_matched_fdtd_return_packet_live_route_rescan_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_return_packet_live_route_rescan_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:          true
sensitivity cases:               20
expected pass cases:             1
expected fail cases:             19
actual pass cases:               1
actual fail cases:               19
unexpected cases:                0
real BEM/FDTD comparison ready:  false
new FDTD executed:               false
GPU priority:                    none
```

The exact live-route rescan passes. The nineteen damaged states fail as
expected for source readiness, row/action shape, parent-directory damage,
external-file promotion, external-file acceptance promotion, producer-input
missing-count damage, return missing-count damage, producer/exporter action
readiness damage, comparison-gate damage, critical-path drift, exporter
promotion, comparison promotion, FDTD-executed promotion, downstream
promotion, figure damage, and missing script snapshots.

## Interpretation

The live-route validator is sensitive to the failure modes that would make the
current route look more complete than it is.

## Decision

Keep the live BEM/FDTD route blocked at the two missing matched-FDTD producer
input files.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_packet_live_route_rescan.py
tests/test_project_core_bem_35field_matched_fdtd_return_packet_live_route_rescan_validator.py
tests/test_project_core_bem_35field_matched_fdtd_return_packet_live_route_rescan_validation_sensitivity.py
9 passed
```

Figure check:

```text
2825x852, dynamic range=255
```

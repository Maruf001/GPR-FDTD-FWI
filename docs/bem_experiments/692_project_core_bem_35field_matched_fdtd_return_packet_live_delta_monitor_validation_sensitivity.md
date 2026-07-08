# BEM Experiment 692: Matched BEM/FDTD Return-Packet Live Delta Monitor Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `691` validator.

The sensitivity set keeps one exact source case and applies controlled damage
to source readiness, component shape, phase shape, BEM acceptance, BEM row
count, matched-FDTD file presence, matched-FDTD acceptance, matched-FDTD row
count, phase readiness, exporter readiness, comparison readiness, downstream
readiness, figure validation, and script snapshots.

This run does not create matched-FDTD files or promote BEM/FDTD comparison.

## Output

```text
outputs/bem_experiments/692_project_core_bem_35field_matched_fdtd_return_packet_live_delta_monitor_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_packet_live_delta_monitor_validation_sensitivity_case_rows.csv
data/project_core_bem_35field_matched_fdtd_return_packet_live_delta_monitor_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_return_packet_live_delta_monitor_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:                    true
sensitivity cases:                         15
expected pass cases:                       1
expected fail cases:                       14
actual pass cases:                         1
actual fail cases:                         14
unexpected cases:                          0
damaged cases:                             14
real BEM/FDTD comparison ready:            false
exporter execution ready:                  false
3D validation claim ready:                 false
field transfer ready:                      false
field FWI ready:                           false
GPU priority:                              none
```

## Interpretation

The validator accepts only the exact current state: accepted BEM files plus
missing matched-FDTD files. It rejects damaged states and rejects premature
promotion of exporter execution, BEM/FDTD comparison, downstream 3D claims,
GPU/HPC work, field transfer, and field FWI.

## Decision

Treat runs `690-692` as the current guarded live-delta block for the 35-field
BEM/FDTD return packet. The next comparison-enabling action is still to supply
and accept the four matched-FDTD files.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_packet_live_delta_monitor.py
tests/test_project_core_bem_35field_matched_fdtd_return_packet_live_delta_monitor_validator.py
tests/test_project_core_bem_35field_matched_fdtd_return_packet_live_delta_monitor_validation_sensitivity.py

10 passed
```

Figure check:

```text
2573x853, dynamic range=255
```

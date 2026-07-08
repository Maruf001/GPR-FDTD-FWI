# BEM Experiment 707: Matched BEM/FDTD Return-Packet Critical-Path Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `706` validator.

The validator should accept only the exact run `705` critical-path state and
reject damaged row shapes, fake matched-FDTD input closure, fake exporter
closure, fake final-comparison readiness, and downstream promotion.

## Output

```text
outputs/bem_experiments/707_project_core_bem_35field_matched_fdtd_return_packet_critical_path_audit_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_packet_critical_path_audit_validation_sensitivity_case_rows.csv
data/project_core_bem_35field_matched_fdtd_return_packet_critical_path_audit_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_return_packet_critical_path_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:          true
sensitivity cases:               18
expected pass cases:             1
expected fail cases:             17
actual pass cases:               1
actual fail cases:               17
unexpected cases:                0
real BEM/FDTD comparison ready:  false
new FDTD executed:               false
GPU priority:                    none
```

The exact critical-path audit passes. The seventeen damaged states fail as
expected for source readiness, file/action shape, dependency-level damage, BEM
baseline damage, fake matched-FDTD input closure, producer-start demotion, fake
exporter return closure, final-gate damage, action-count promotion, exporter
promotion, comparison promotion, FDTD-executed promotion, downstream
promotion, figure damage, and missing script snapshots.

## Interpretation

The critical-path validator is sensitive to the failure modes that would make
the current packet look more complete than it is.

## Decision

Keep the BEM/FDTD bridge rooted at the two missing matched-FDTD producer input
files until real inputs exist.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_packet_critical_path_audit.py
tests/test_project_core_bem_35field_matched_fdtd_return_packet_critical_path_audit_validator.py
tests/test_project_core_bem_35field_matched_fdtd_return_packet_critical_path_audit_validation_sensitivity.py
9 passed
```

Figure check:

```text
2753x849, dynamic range=255
```

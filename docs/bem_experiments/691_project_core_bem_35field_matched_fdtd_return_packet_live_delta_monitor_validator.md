# BEM Experiment 691: Matched BEM/FDTD Return-Packet Live Delta Monitor Validator

Date: 2026-06-30

## Purpose

Validate run `690`, the current live-delta monitor for the 35-field BEM/FDTD
comparison packet.

The validator checks source-chain readiness, component and phase shape, BEM-side
acceptance, matched-FDTD absence, downstream claim blocking, figure output, and
frozen script snapshots.

This run does not produce matched-FDTD files, execute the exporter, run
BEM/FDTD comparison, promote 3D validation, or launch GPU/HPC work.

## Output

```text
outputs/bem_experiments/691_project_core_bem_35field_matched_fdtd_return_packet_live_delta_monitor_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_packet_live_delta_monitor_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_return_packet_live_delta_monitor_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_return_packet_live_delta_monitor_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         7
passed checks:                             7
failed checks:                             0
comparison component files:                6
BEM accepted files:                        2
BEM accepted rows:                         558
matched-FDTD files present:                0
matched-FDTD files accepted:               0
matched-FDTD files missing:                4
expected matched-FDTD input rows:          558
expected matched-FDTD return rows:         558
real BEM/FDTD comparison ready:            false
exporter execution ready:                  false
3D validation claim ready:                 false
field transfer ready:                      false
field FWI ready:                           false
GPU priority:                              none
```

## Interpretation

The live-delta monitor is internally consistent. It preserves the two-file BEM
accepted state and the four-file matched-FDTD missing state.

## Decision

Use run `691` as the validator for the current return-packet live-delta monitor.
Do not use the accepted BEM files alone as BEM/FDTD comparison evidence.

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
2429x838, dynamic range=255
```

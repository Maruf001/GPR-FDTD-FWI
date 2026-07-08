# BEM Experiment 694: Matched BEM/FDTD Return-Packet Live Delta Closure Sequence Validator

Date: 2026-06-30

## Purpose

Validate run `693`, the BEM/FDTD comparison closure sequence.

The validator checks source readiness, file and action shape, the accepted BEM
baseline, the matched-FDTD closure gap, downstream blocking, figure output, and
frozen script snapshots.

This run does not create matched-FDTD files or promote comparison readiness.

## Output

```text
outputs/bem_experiments/694_project_core_bem_35field_matched_fdtd_return_packet_live_delta_closure_sequence_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_packet_live_delta_closure_sequence_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_return_packet_live_delta_closure_sequence_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_return_packet_live_delta_closure_sequence_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         6
passed checks:                             6
failed checks:                             0
sequence files:                            6
sequence actions:                          4
BEM accepted files:                        2
matched-FDTD missing files:                4
accepted BEM rows:                         558
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

The closure sequence validates as one accepted BEM baseline plus a four-file
matched-FDTD gap.

## Decision

Use run `694` as the validator for the BEM/FDTD closure checklist.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_packet_live_delta_closure_sequence.py
tests/test_project_core_bem_35field_matched_fdtd_return_packet_live_delta_closure_sequence_validator.py
tests/test_project_core_bem_35field_matched_fdtd_return_packet_live_delta_closure_sequence_validation_sensitivity.py

10 passed
```

Figure check:

```text
2357x839, dynamic range=255
```

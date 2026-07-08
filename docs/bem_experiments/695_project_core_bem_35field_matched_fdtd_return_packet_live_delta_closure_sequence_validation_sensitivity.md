# BEM Experiment 695: Matched BEM/FDTD Return-Packet Live Delta Closure Sequence Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `694` validator.

The sensitivity set keeps one exact source case and applies controlled damage
to source readiness, file count, action count, BEM acceptance, BEM row count,
matched-FDTD file presence, matched-FDTD acceptance, matched-FDTD row count,
closure action completion, exporter readiness, comparison readiness,
downstream readiness, figure validation, and script snapshots.

This run does not create matched-FDTD files or promote comparison readiness.

## Output

```text
outputs/bem_experiments/695_project_core_bem_35field_matched_fdtd_return_packet_live_delta_closure_sequence_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_packet_live_delta_closure_sequence_validation_sensitivity_case_rows.csv
data/project_core_bem_35field_matched_fdtd_return_packet_live_delta_closure_sequence_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_return_packet_live_delta_closure_sequence_validation_sensitivity.png
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

The validator accepts only the exact current sequence and rejects BEM demotion,
fake matched-FDTD closure, and premature downstream promotion.

## Decision

Treat runs `693-695` as the current guarded BEM/FDTD closure-sequence block.
The next comparison-enabling action is still to supply and accept the four
matched-FDTD files.

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
2573x855, dynamic range=255
```

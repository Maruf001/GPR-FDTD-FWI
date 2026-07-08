# BEM Experiment 825: Complex FDTD Adapter Input Staged Handoff Packet Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `824` validator with damaged versions of the run `823`
staged handoff packet.

The damaged cases include policy-label damage, stage-shape damage, cumulative
shape damage, packet-manifest damage, missing packet files, accidental
external-path promotion, final row-count damage, final blank-count damage,
false external-input presence, false acceptance, comparison promotion, figure
damage, and script-snapshot damage.

## Output

```text
outputs/bem_experiments/825_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_staged_handoff_packet_validation_sensitivity
```

## Result

```text
scenarios:                         14
expected pass scenarios:           1
expected fail scenarios:           13
observed pass scenarios:           1
observed fail scenarios:           13
unexpected outcomes:               0
damaged scenarios:                 13
damaged scenarios rejected:        13
gpu priority:                      none
```

## Interpretation

The validator fails closed. The exact saved packet passes, while all damaged
packet and false-promotion states are rejected.

## Decision

Use this sensitivity block to guard the staged complex FDTD handoff. Do not
promote comparison from altered row counts, missing packet files, external-path
confusion, or false real-input acceptance.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_staged_handoff_packet_validation_sensitivity.py
```

Figure check:

```text
3689x920, dynamic range=255
```

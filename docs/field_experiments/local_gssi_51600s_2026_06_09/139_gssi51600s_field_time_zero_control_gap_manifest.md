# Field Experiment 139: Time-Zero Control Gap Manifest

Date: 2026-06-18

## Purpose

Consolidate the existing field timing evidence from runs `090`, `105`, `121`,
and `138` into one current absolute-time-zero control-gap manifest.

This is CPU-only synthesis of saved field outputs. It does not run FDTD, FWI,
GPU kernels, 3D/HPC work, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/139_gssi51600s_field_time_zero_control_gap_manifest
```

Key artifacts:

```text
data/field_time_zero_control_gap_summary.json
data/field_time_zero_control_gap_timing_sources.csv
data/field_time_zero_control_gap_gates.csv
```

## Result

```text
timing sources:                         5
absolute time-zero candidates:          0
relative short timing supported:        true
early common-mode negative control:     true
short content offset:                   0.12770137524557956 ns
early common-mode offset:               0.0 ns
short-vs-early delta:                   0.12770137524557956 ns
conservative half-width:                0.058939096267190516 ns
delta exceeds conservative half-width:  true
must-have controls satisfied:           0/5
absolute time-zero ready:               false
field FWI ready:                        false
gpu priority:                           none
```

## Interpretation

Existing field timing evidence supports relative short-profile timing QC, not
absolute time-zero. The early/direct component is a common-mode negative
control, raw uncorrected timing is rejected, and long profiles remain
pattern-only. The next useful field timing measurement is an external
air/direct-wave or metal-plate reference recorded per session and propagated
against the short content-backed relative timing ladder.

Current field FWI, heavy field GPU work, and field 3D/HPC remain blocked.

## Validation

Focused tests:

```text
tests/test_gssi_field_time_zero_control_gap_manifest.py
tests/test_gssi_field_existing_data_control_manifest.py
4 passed
```

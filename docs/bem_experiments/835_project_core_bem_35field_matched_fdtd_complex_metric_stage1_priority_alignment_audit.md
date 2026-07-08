# BEM Experiment 835: Stage-1 Priority Alignment Audit

Date: 2026-07-01

## Purpose

Audit whether the current stage-1 live-return contract aligns with the existing
matched-FDTD producer execution-priority map.

## Output

```text
outputs/bem_experiments/835_project_core_bem_35field_matched_fdtd_complex_metric_stage1_priority_alignment_audit
```

## Result

```text
alignment checks:                  5
passed alignment checks:           5
failed alignment checks:           0
priority pair count:             279
priority batch count:              5
priority stage shape:              1;8;30;120;120
stage-1 receiver index:           15
stage-1 frequency:                 1.0 GHz
stage-1 contract rows:             1
stage-1 live partial present:      false
full external input present:       false
real BEM/FDTD comparison ready:    false
field transfer ready:              false
3D/HPC ready:                      false
```

## Interpretation

The current stage-1 live-return contract matches the older producer priority
map's center-pair smoke: receiver `15` at `1.0 GHz`.

## Decision

Use the existing priority map to schedule the first producer return, but keep
comparison blocked until a real stage-1 partial file passes intake.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_priority_alignment_audit.py
2 passed
```

Figure check:

```text
3221x893, dynamic range=255
```

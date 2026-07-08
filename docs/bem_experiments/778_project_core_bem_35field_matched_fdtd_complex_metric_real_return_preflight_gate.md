# BEM Experiment 778: Complex Metric Real-Return Preflight Gate

Date: 2026-07-01

## Purpose

Define the preflight gate for the five real BEM/FDTD complex metric CSV files
before any file is staged into the live intake path.

This run does not create real solver-return files, does not stage files into
the live intake area, does not execute copy commands, does not accept template
files as real returns, and does not promote real BEM/FDTD comparison.

## Output

```text
outputs/bem_experiments/778_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate_preflight_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source staging plan ready:          true
source validation ready:            true
source sensitivity ready:           true
preflight files:                    5
required metric rows:               279
required columns:                   13
producer files present:             0
required columns present:           0
row-count matches:                  0
preflight-passed files:             0
ready-to-stage files:               0
executed commands:                  0
real BEM/FDTD comparison ready:     false
gpu priority:                       none
```

Required file checks:

```text
not template path
CSV exists
all required columns present
row count matches
no blank required value cells
real FDTD exported is true
solver status is completed
finite complex BEM/FDTD values
```

## Interpretation

The real-return preflight gate is now explicit. It checks the five planned
producer CSV files against the thirteen-column complex metric schema and the
required row counts of 1, 8, 30, 120, and 120.

The current state remains pre-return. No producer CSV file is present, no file
passes preflight, no file is ready to stage, and no command is executed.

## Decision

Use run `778` as the preflight gate before staging any BEM/FDTD complex metric
CSV file. Keep real comparison blocked until all five producer CSV files pass
preflight, are staged through the guarded intake path, and are accepted as real
returns.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate.py
3 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate.py: pass
```

Figure check:

```text
2212x846, dynamic range=255
```

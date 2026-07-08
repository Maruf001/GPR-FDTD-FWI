# BEM Experiment 763: Metric Addendum Live-Return Intake Gate

Date: 2026-07-01

## Purpose

Define the intake gate for the five complex-valued BEM/FDTD metric addendum
files from run `760`.

This run checks the current file state and encodes the acceptance checks needed
when real numeric files arrive: row count, required columns, finite numeric
fields, finite complex components, real FDTD export flags, and completed solver
status.

This run does not use real BEM/FDTD values, run FDTD, make a real comparison
claim, run 3D validation, launch GPU/HPC work, transfer to field data, or run
field FWI.

## Output

```text
outputs/bem_experiments/763_project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_live_return_intake_gate
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_live_return_intake_gate_file_rows.csv
data/project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_live_return_intake_gate_summary.json
figures/project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_live_return_intake_gate.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source addendum ready:                   true
expected addendum files:                 5
live parent directories present:         5
live files present:                      0
missing live files:                      5
accepted files:                          0
required metric rows:                    279
observed metric rows:                    0
required metric cells:                   3627
required complex component cells:        1116
accepted metric rows:                    0
metric addendum intake accepted:         false
real BEM/FDTD comparison ready:          false
gpu priority:                            none
```

File statuses:

| Stage | Required rows | Required complex cells | Status |
| ---: | ---: | ---: | --- |
| 1 | 1 | 4 | missing_addendum_file |
| 2 | 8 | 32 | missing_addendum_file |
| 3 | 30 | 120 | missing_addendum_file |
| 4 | 120 | 480 | missing_addendum_file |
| 5 | 120 | 480 | missing_addendum_file |

## Interpretation

The complex-valued metric addendum now has an intake gate. The gate is ready to
reject missing, malformed, incomplete, nonnumeric, synthetic, or incomplete
solver-return files.

The current state remains pre-return: all five expected addendum files are
absent.

## Decision

Use run `763` as the live-return intake gate for future BEM/FDTD complex-value
files. Keep real comparison, 3D validation, GPU/HPC, field transfer, and field
FWI blocked until all five files pass intake.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_live_return_intake_gate.py
4 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_live_return_intake_gate.py: pass
tests/test_project_core_bem_35field_matched_fdtd_metric_input_schema_addendum_live_return_intake_gate.py: pass
```

Figure check:

```text
1708x846, dynamic range=255
```

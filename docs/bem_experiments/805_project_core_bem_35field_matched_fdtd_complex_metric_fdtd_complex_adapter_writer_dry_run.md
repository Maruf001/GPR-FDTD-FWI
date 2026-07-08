# BEM Experiment 805: Complex FDTD Adapter Writer Dry Run

Date: 2026-07-01

## Purpose

Add a fail-closed writer dry run for the complex FDTD adapter needed by the
matched BEM/FDTD complex-field comparison.

Runs `799-804` defined and guarded the adapter contract. This run exercises the
writer-side logic against the five BEM partial stage files from run `790` and
checks whether a real FDTD complex input file is present and acceptable.

## Output

```text
outputs/bem_experiments/805_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_writer_dry_run
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_writer_dry_run_stage_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_writer_dry_run_input_validation_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_writer_dry_run_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_writer_dry_run.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source interface guard ready:              true
source interface sensitivity ready:        true
partial stage files:                       5
partial metric rows:                       279
candidate FDTD complex input present:      false
adapter input rows:                        0
accepted FDTD rows:                        0
rejected FDTD rows:                        0
missing FDTD identity rows:                279
completed stage files written:             0
writer dry run ready:                      true
full input valid:                          false
would write completed stage files:         false
completed stage files ready:               false
real BEM/FDTD comparison ready:            false
field transfer ready:                      false
3D/HPC ready:                              false
gpu priority:                              none
```

The required contract hash remains:

```text
8c0e4be114e3c7d8703aa8b0afaa468c6dd33968c62742fdff01bc52a736339a
```

## Interpretation

The writer path now has an executable gate. It sees all five BEM partial stage
files but accepts zero FDTD rows because the real complex FDTD input file is not
present.

The missing rows are distributed across the five stages as follows:

| Stage | BEM partial rows | Accepted FDTD rows | Missing FDTD rows |
| ---: | ---: | ---: | ---: |
| 1 | 1 | 0 | 1 |
| 2 | 8 | 0 | 8 |
| 3 | 30 | 0 | 30 |
| 4 | 120 | 0 | 120 |
| 5 | 120 | 0 | 120 |

## Decision

Keep the real BEM/FDTD complex comparison blocked until a complete real FDTD
input file is available with matching contract hash, finite real and imaginary
field values, successful solver status, real export flag, source hash, and
solver-log hash.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_writer_dry_run.py

4 passed
```

Figure check:

```text
2968x918, dynamic range=255
```

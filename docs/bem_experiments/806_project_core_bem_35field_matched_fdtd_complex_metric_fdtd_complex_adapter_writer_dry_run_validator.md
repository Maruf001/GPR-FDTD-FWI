# BEM Experiment 806: Complex FDTD Adapter Writer Dry Run Validator

Date: 2026-07-01

## Purpose

Validate the saved run `805` complex FDTD adapter writer dry run.

Run `805` added an executable fail-closed writer path for the matched BEM/FDTD
complex-field comparison. This validator checks that the saved dry-run state is
internally consistent and does not promote completed stage files or comparison.

## Output

```text
outputs/bem_experiments/806_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_writer_dry_run_validator
```

## Result

```text
validation checks:                         8
passed checks:                             8
failed checks:                             0
partial stage files:                       5
partial metric rows:                       279
adapter input rows:                        0
accepted FDTD rows:                        0
missing FDTD identity rows:                279
completed stage files:                     0
candidate input file present:              false
completed stage files ready:               false
real BEM/FDTD comparison ready:            false
3D/HPC ready:                              false
gpu priority:                              none
```

## Interpretation

The saved writer dry run is stable. It preserves the five-stage partial BEM
packet shape, confirms that no real FDTD complex input is present, accepts zero
FDTD rows, and writes zero completed comparison files.

## Decision

Use this validator before any non-dry-run complex FDTD adapter writer is added.
Keep the real BEM/FDTD complex comparison blocked until real FDTD complex input
passes the full row and provenance checks.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_writer_dry_run_validator.py

3 passed
```

Figure check:

```text
2861x936, dynamic range=255
```

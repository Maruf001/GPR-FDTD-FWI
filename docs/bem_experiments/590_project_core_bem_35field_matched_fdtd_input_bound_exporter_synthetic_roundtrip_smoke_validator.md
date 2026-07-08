# BEM Experiment 590: Matched FDTD Input-Bound Exporter Synthetic Roundtrip Smoke Validator

Date: 2026-06-30

## Purpose

Validate run `589` from its saved artifacts.

This run checks that the synthetic roundtrip has four cases, writes two
synthetic return files, accepts 558 synthetic rows, preserves zero real
evidence, and keeps all downstream states blocked.

## Output

```text
outputs/bem_experiments/590_project_core_bem_35field_matched_fdtd_input_bound_exporter_synthetic_roundtrip_smoke_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_synthetic_roundtrip_smoke_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_synthetic_roundtrip_smoke_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_synthetic_roundtrip_smoke_validator.png
scripts/
```

## Result

```text
check count:                             5
passed checks:                           5
failed checks:                           0
roundtrip cases:                         4
return files written:                    2
roundtrip accepted rows:                 558
real evidence files:                     0
real BEM/FDTD comparison ready:          false
field transfer ready:                    false
field FWI ready:                         false
gpu priority:                            none
```

## Interpretation

The output-local synthetic exporter roundtrip validates and remains
non-evidence.

## Decision

Use run `590` as the artifact validator for run `589`.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_synthetic_roundtrip_smoke_validator.py

3 passed
```

Figure validation:

```text
2285x839, dynamic range=255
```

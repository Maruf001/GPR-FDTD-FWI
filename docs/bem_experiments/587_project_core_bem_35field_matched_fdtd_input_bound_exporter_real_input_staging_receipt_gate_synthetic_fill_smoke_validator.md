# BEM Experiment 587: Matched FDTD Input-Bound Exporter Real-Input Staging Receipt Gate Synthetic Fill Smoke Validator

Date: 2026-06-30

## Purpose

Validate run `586` from its saved artifacts.

This run checks that the synthetic smoke has four cases, accepts exactly the
two valid synthetic files, rejects exactly the two invalid synthetic files,
accepts 558 synthetic rows, preserves zero real evidence, keeps the external
staging area empty, and keeps all downstream states blocked.

## Output

```text
outputs/bem_experiments/587_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_gate_synthetic_fill_smoke_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_gate_synthetic_fill_smoke_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_gate_synthetic_fill_smoke_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_gate_synthetic_fill_smoke_validator.png
scripts/
```

## Result

```text
check count:                             5
passed checks:                           5
failed checks:                           0
synthetic cases:                         4
actual accepted cases:                   2
actual rejected cases:                   2
unexpected cases:                        0
synthetic accepted rows:                 558
real evidence files:                     0
external staged files:                   0
external accepted files:                 0
real BEM/FDTD comparison ready:          false
field transfer ready:                    false
field FWI ready:                         false
```

## Interpretation

The synthetic smoke validates as a gate exercise only. It proves the receipt
logic can accept and reject rows, but it remains non-evidence.

## Decision

Use run `587` as the artifact validator for run `586`.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_input_staging_receipt_gate_synthetic_fill_smoke_validator.py

3 passed
```

Figure validation:

```text
2285x841, dynamic range=255
```

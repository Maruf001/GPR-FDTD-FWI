# BEM Experiment 593: Matched FDTD Input-Bound Exporter Post-Synthetic-Roundtrip External Staging Guard Validator

Date: 2026-06-30

## Purpose

Validate the external staging guard from run `592`.

Run `592` checked that the output-local synthetic exporter roundtrip did not
write into the locked external real staging paths. This run verifies the guard
with explicit checks for source readiness, staging-path shape, zero promoted
external files, zero synthetic pollution, blocked downstream states, and
artifact presence.

## Output

```text
outputs/bem_experiments/593_project_core_bem_35field_matched_fdtd_input_bound_exporter_post_synthetic_roundtrip_external_staging_guard_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_post_synthetic_roundtrip_external_staging_guard_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_post_synthetic_roundtrip_external_staging_guard_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_post_synthetic_roundtrip_external_staging_guard_validator.png
scripts/
```

## Result

```text
checks:                         5
passed checks:                  5
failed checks:                  0
synthetic return files:         2
synthetic accepted rows:        558
external paths checked:         4
external files present:         0
external files accepted:        0
synthetic pollution count:      0
real BEM/FDTD comparison ready: false
field transfer ready:           false
field FWI ready:                false
gpu priority:                   none
```

## Interpretation

The synthetic roundtrip remains isolated from the real external staging area.
Run `593` verifies that run `592` is a valid guard artifact rather than a
plot-only assertion.

## Decision

Use run `593` as the validator for run `592`. Keep real BEM/FDTD comparison
blocked until actual external staged files are supplied and accepted.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_post_synthetic_roundtrip_external_staging_guard_validator.py

3 passed
```

Figure validation:

```text
2285x839, dynamic range=255
```

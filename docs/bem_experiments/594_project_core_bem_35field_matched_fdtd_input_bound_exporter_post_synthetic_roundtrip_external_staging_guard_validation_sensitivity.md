# BEM Experiment 594: Matched FDTD Input-Bound Exporter Post-Synthetic-Roundtrip External Staging Guard Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the validator from run `593`.

This run checks that the validator accepts the exact run `592` guard and
rejects damaged states that would falsely promote missing real files, synthetic
pollution, downstream readiness, or damaged artifacts.

## Output

```text
outputs/bem_experiments/594_project_core_bem_35field_matched_fdtd_input_bound_exporter_post_synthetic_roundtrip_external_staging_guard_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_post_synthetic_roundtrip_external_staging_guard_validation_sensitivity_cases.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_post_synthetic_roundtrip_external_staging_guard_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_post_synthetic_roundtrip_external_staging_guard_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:         true
cases:                          14
expected pass cases:            1
expected fail cases:            13
actual pass cases:              1
actual fail cases:              13
unexpected outcomes:            0
damaged cases:                  13
real BEM/FDTD comparison ready: false
field transfer ready:           false
field FWI ready:                false
gpu priority:                   none
```

The damaged states cover source-chain damage, synthetic return-count damage,
accepted-row damage, external-row removal, missing parent-directory damage,
external file promotion, external nonempty-file promotion, external acceptance
promotion, synthetic pollution promotion, downstream promotion, figure damage,
and script-snapshot damage.

## Interpretation

The external staging guard validator is sensitive to the failure modes that
would matter for the next real BEM/FDTD comparison step. It does not accept
premature file promotion or synthetic contamination of the real staging path.

## Decision

Use runs `592-594` as the closed post-synthetic-roundtrip boundary. Keep real
BEM/FDTD comparison blocked until actual external staged files pass receipt and
exporter gates.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_post_synthetic_roundtrip_external_staging_guard_validation_sensitivity.py

3 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```

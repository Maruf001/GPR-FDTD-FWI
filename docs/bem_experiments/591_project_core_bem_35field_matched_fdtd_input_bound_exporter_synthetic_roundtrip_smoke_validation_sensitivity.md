# BEM Experiment 591: Matched FDTD Input-Bound Exporter Synthetic Roundtrip Smoke Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `590` validator with controlled damage to the run `589`
synthetic roundtrip artifacts.

This run checks that the validator fails when case shape, return-file state,
success state, accepted-row state, real-evidence state, downstream state,
figure metadata, or script snapshots are damaged.

## Output

```text
outputs/bem_experiments/591_project_core_bem_35field_matched_fdtd_input_bound_exporter_synthetic_roundtrip_smoke_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_synthetic_roundtrip_smoke_validation_sensitivity_cases.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_synthetic_roundtrip_smoke_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_synthetic_roundtrip_smoke_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:                  true
sensitivity cases:                       13
expected pass cases:                     1
expected fail cases:                     12
actual pass cases:                       1
actual fail cases:                       12
unexpected cases:                        0
damaged cases:                           12
real BEM/FDTD comparison ready:          false
field transfer ready:                    false
field FWI ready:                         false
gpu priority:                            none
```

Damaged states fail for:

```text
source readiness removal
roundtrip case removal
valid case-count damage
return file-count damage
success-count damage
accepted-row count damage
valid-row acceptance damage
unexpected-case promotion
real-evidence promotion
BEM/FDTD comparison promotion
figure damage
missing script snapshots
```

## Interpretation

The synthetic roundtrip validator is sensitive to the intended failure modes.
It does not silently promote synthetic exporter output into real comparison
evidence.

## Decision

Use runs `589-591` as the guarded output-local exporter roundtrip smoke block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_synthetic_roundtrip_smoke_validation_sensitivity.py

3 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```

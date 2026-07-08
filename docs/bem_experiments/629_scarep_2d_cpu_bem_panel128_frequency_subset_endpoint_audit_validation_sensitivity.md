# BEM Experiment 629: 128-Panel Frequency-Subset Endpoint Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `628` validator for the run `627` 128-panel frequency-subset
endpoint audit.

Run `627` showed that 128 panels closes the high-frequency-only failure observed
at 64 panels. This run checks that the validator rejects damaged states that
erase the endpoint boundary, damage saved-array consistency, or promote the
result into unsupported project FDTD, field, GPU/HPC, or three-dimensional
claims.

## Output

```text
outputs/bem_experiments/629_scarep_2d_cpu_bem_panel128_frequency_subset_endpoint_audit_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel128_frequency_subset_endpoint_audit_validation_sensitivity_rows.csv
data/scarep_2d_cpu_bem_panel128_frequency_subset_endpoint_audit_validation_sensitivity_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel128_frequency_subset_endpoint_audit_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:                  true
sensitivity cases:                       27
expected pass cases:                     1
expected fail cases:                     26
actual pass cases:                       1
actual fail cases:                       26
unexpected outcomes:                     0
exact source passes:                     true
damaged cases rejected:                  true
endpoint boundary damage rejected:       true
array consistency damage rejected:       true
claim-promotion cases rejected:          true
project FDTD comparison ready:           false
real 3D validation ready:                false
GPU/HPC ready:                           false
field transfer ready:                    false
field FWI ready:                         false
```

The rejected damage cases cover:

| Group | Examples |
| --- | --- |
| Source readiness | endpoint readiness, 128-panel repeatability, and 64-panel frequency-sensitivity readiness set false |
| Frequency design | row removal, high-band subset rename, zero frequency count |
| Endpoint boundary | 128-panel high-band error above target, erased 64-panel high-band failure, damaged improvement factor |
| Summary consistency | pass-count, fail-count, max-error, panel-count, and endpoint-flag damage |
| Saved arrays | response hash, time-B-scan hash, complex-error summary, and time-error summary damage |
| Claim boundary | project FDTD, 3D, GPU/HPC, field-transfer, and field-FWI promotion |
| Artifact integrity | figure damage and missing script snapshots |

## Interpretation

The 128-panel endpoint result now has an audit, validator, and sensitivity test.
The guarded result is:

```text
64-panel high-band relative L2:   0.001736291511432671
128-panel high-band relative L2:  0.0004276569548253307
improvement factor:               4.060009995960033
```

This supports 128 panels as the high-frequency endpoint for the
two-dimensional scarep analytic-cylinder BEM setup. It remains a bounded BEM
validation result, not a project FDTD comparison, not a field-data result, not a
three-dimensional Maxwell validation, and not a GPU/HPC readiness result.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel128_frequency_subset_endpoint_audit_validator.py
tests/test_scarep_2d_cpu_bem_panel128_frequency_subset_endpoint_audit_validation_sensitivity.py

6 passed
```

Figure check:

```text
2860x928, dynamic range=255
```

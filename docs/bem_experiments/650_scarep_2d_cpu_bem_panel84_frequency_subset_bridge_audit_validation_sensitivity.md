# BEM Experiment 650: 84-Panel Frequency-Subset Bridge Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `649` validator for the narrow-margin 84-panel
high-frequency bridge result.

Run `649` validated the 84-panel pass, but the high-band error was only
`4.437414146502028e-6` below the `1e-3` target. This run damages the validator
inputs one case at a time to confirm that bridge drift, threshold drift,
saved-array damage, downstream claim promotion, figure damage, and missing
script snapshots are rejected.

## Output

```text
outputs/bem_experiments/650_scarep_2d_cpu_bem_panel84_frequency_subset_bridge_audit_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel84_frequency_subset_bridge_audit_validation_sensitivity_rows.csv
data/scarep_2d_cpu_bem_panel84_frequency_subset_bridge_audit_validation_sensitivity_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel84_frequency_subset_bridge_audit_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:                   true
cases tested:                             27
expected pass cases:                      1
expected fail cases:                      26
actual pass cases:                        1
actual fail cases:                        26
unexpected outcomes:                      0
exact source passes:                      true
damaged cases rejected:                   true
bridge damage rejected:                   true
threshold-bracket damage rejected:        true
array damage rejected:                    true
claim-promotion cases rejected:           true
validation sensitivity ready:             true
project FDTD comparison ready:            false
real 3D validation ready:                 false
GPU/HPC ready:                            false
field transfer ready:                     false
field FWI ready:                          false
```

Sensitivity classes:

| Class | Cases | Outcome |
| --- | ---: | --- |
| Exact source | 1 | accepted |
| Source and bridge readiness drift | 2 | rejected |
| Subset and panel-count damage | 4 | rejected |
| Threshold-bracket drift | 9 | rejected |
| Saved-array damage | 3 | rejected |
| Downstream claim promotion | 5 | rejected |
| Figure or script damage | 2 | rejected |
| Row mismatch | 1 | rejected |

## Interpretation

The narrow 84-panel pass is guarded against common artifact damage and claim
drift. The exact run `649` source is accepted, while all damaged states are
rejected.

## Decision

Use run `649` as the validator guard for the 84-panel candidate. A policy
refresh can promote 84 panels as the lower-cost high-frequency candidate, with
the caveat that 84 is a narrow-margin pass and 88 remains the more comfortable
low-cost pass.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel84_frequency_subset_bridge_audit.py
tests/test_scarep_2d_cpu_bem_panel84_frequency_subset_bridge_audit_validator.py
tests/test_scarep_2d_cpu_bem_panel84_frequency_subset_bridge_audit_validation_sensitivity.py

9 passed
```

Figure check:

```text
2842x881, dynamic range=255
```

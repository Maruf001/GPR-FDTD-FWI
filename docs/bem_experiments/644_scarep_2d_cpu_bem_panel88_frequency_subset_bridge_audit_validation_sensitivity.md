# BEM Experiment 644: 88-Panel Frequency-Subset Bridge Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `643` validator for the 88-panel high-frequency bridge
result.

Run `643` validated 88 panels as a guarded lower-cost high-frequency candidate.
This run damages the validator inputs one case at a time to confirm that the
validator rejects bridge readiness drift, threshold-bracket damage, saved-array
damage, downstream claim promotion, figure damage, and missing script
snapshots.

## Output

```text
outputs/bem_experiments/644_scarep_2d_cpu_bem_panel88_frequency_subset_bridge_audit_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel88_frequency_subset_bridge_audit_validation_sensitivity_rows.csv
data/scarep_2d_cpu_bem_panel88_frequency_subset_bridge_audit_validation_sensitivity_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel88_frequency_subset_bridge_audit_validation_sensitivity.png
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

The 88-panel bridge is now guarded against accidental promotion or threshold
drift. The exact run `643` source is accepted, while all damaged states are
rejected.

## Decision

Use run `643` as the guarded validator for the 88-panel lower-cost
high-frequency candidate. Refresh the frequency-cost policy so 88 panels
replace 96 panels as the lower-cost high-frequency candidate, while 128 panels
remain the strict endpoint.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel88_frequency_subset_bridge_audit.py
tests/test_scarep_2d_cpu_bem_panel88_frequency_subset_bridge_audit_validator.py
tests/test_scarep_2d_cpu_bem_panel88_frequency_subset_bridge_audit_validation_sensitivity.py

9 passed
```

Figure check:

```text
2842x881, dynamic range=255
```

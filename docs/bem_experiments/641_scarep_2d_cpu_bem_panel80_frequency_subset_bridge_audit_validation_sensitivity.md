# BEM Experiment 641: 80-Panel Frequency-Subset Bridge Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `640` validator for the 80-panel high-frequency no-go
result.

Run `640` validated that the 80-panel solve is a real no-go for
high-frequency-only use. This run damages the validator inputs one case at a
time to confirm that the validator rejects no-go drift, threshold-bracket
damage, saved-array damage, downstream claim promotion, figure damage, and
missing script snapshots.

## Output

```text
outputs/bem_experiments/641_scarep_2d_cpu_bem_panel80_frequency_subset_bridge_audit_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel80_frequency_subset_bridge_audit_validation_sensitivity_rows.csv
data/scarep_2d_cpu_bem_panel80_frequency_subset_bridge_audit_validation_sensitivity_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel80_frequency_subset_bridge_audit_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:                   true
cases tested:                             26
expected pass cases:                      1
expected fail cases:                      25
actual pass cases:                        1
actual fail cases:                        25
unexpected outcomes:                      0
exact source passes:                      true
damaged cases rejected:                   true
no-go damage rejected:                    true
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
| Source and no-go drift | 6 | rejected |
| Threshold-bracket drift | 7 | rejected |
| Saved-array damage | 3 | rejected |
| Downstream claim promotion | 5 | rejected |
| Figure or script damage | 2 | rejected |
| Other structural damage | 2 | rejected |

## Interpretation

The no-go result is now guarded against accidental promotion. The exact
run `640` source is accepted, while all damaged states are rejected. This
supports the current bracket:

```text
64 panels: high band fails
80 panels: high band fails
96 panels: high band passes
128 panels: strict high-band endpoint
```

## Decision

Keep run `640` as the no-go validator for run `639`. Keep the run `636`
frequency-cost policy unchanged.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel80_frequency_subset_bridge_audit.py
tests/test_scarep_2d_cpu_bem_panel80_frequency_subset_bridge_audit_validator.py
tests/test_scarep_2d_cpu_bem_panel80_frequency_subset_bridge_audit_validation_sensitivity.py

9 passed
```

Figure check:

```text
2788x880, dynamic range=255
```

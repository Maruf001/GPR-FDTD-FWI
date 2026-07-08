# BEM Experiment 632: Frequency-Aware Panel Policy Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `631` validator for the frequency-aware 64/128-panel
policy from run `630`.

The sensitivity audit answers whether the validator only accepts the exact
guarded source policy and rejects damaged states that would weaken the panel
split, erase the high-frequency boundary, or over-promote the result beyond
the scarep analytic-cylinder BEM evidence.

## Output

```text
outputs/bem_experiments/632_scarep_2d_cpu_bem_frequency_aware_panel_policy_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_frequency_aware_panel_policy_validation_sensitivity_rows.csv
data/scarep_2d_cpu_bem_frequency_aware_panel_policy_validation_sensitivity_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_frequency_aware_panel_policy_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:            true
sensitivity cases:                 20
expected pass cases:               1
expected fail cases:               19
actual pass cases:                 1
actual fail cases:                 19
unexpected outcomes:               0
exact source passes:               true
damaged cases rejected:            true
panel policy damage rejected:      true
claim promotion cases rejected:    true
project FDTD comparison ready:     false
real 3D validation ready:          false
GPU/HPC ready:                     false
field transfer ready:              false
field FWI ready:                   false
```

The exact source validator passes. All nineteen damaged states fail as
expected:

| Group | Damaged states | Result |
| --- | ---: | --- |
| Source readiness | 1 | rejected |
| Policy row shape and panel roles | 9 | rejected |
| High-frequency boundary and improvement | 3 | rejected |
| Project FDTD, 3D, GPU/HPC, field-transfer, and field-FWI promotion | 5 | rejected |
| Figure and script artifacts | 2 | rejected |

## Interpretation

Run `632` hardens the frequency-aware panel-policy block. The guarded decision
remains:

```text
64 panels: receiver-line sensitivity and broad/low/mid-band sweeps
128 panels: high-frequency-only 2.08-3.00 GHz endpoint checks
no promotion: project FDTD, field transfer, 3D, GPU/HPC, or field FWI
```

The validator also now fails gracefully when a required policy row is missing:
the missing-row sensitivity case is rejected by failed checks rather than by an
uncaught exception.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_frequency_aware_panel_policy.py
tests/test_scarep_2d_cpu_bem_frequency_aware_panel_policy_validator.py
tests/test_scarep_2d_cpu_bem_frequency_aware_panel_policy_validation_sensitivity.py

9 passed
```

Figure check:

```text
2644x891, dynamic range=255
```

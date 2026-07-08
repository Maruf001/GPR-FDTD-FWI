# BEM Experiment 631: Frequency-Aware Panel Policy Validator

Date: 2026-06-30

## Purpose

Validate run `630`, the frequency-aware 64/128-panel policy for the
two-dimensional scarep CPU BEM analytic-cylinder setup.

## Output

```text
outputs/bem_experiments/631_scarep_2d_cpu_bem_frequency_aware_panel_policy_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_frequency_aware_panel_policy_validator_check_rows.csv
data/scarep_2d_cpu_bem_frequency_aware_panel_policy_validator_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_frequency_aware_panel_policy_validator.png
scripts/
```

## Result

```text
validation checks:                 5
failed checks:                     0
policy rows:                       4
64-panel policy rows:              2
128-panel policy rows:             1
blocked downstream policy rows:    1
64-panel high-band relative L2:    0.001736291511432671
128-panel high-band relative L2:   0.0004276569548253307
high-band improvement factor:      4.060009995960033
project FDTD comparison ready:     false
real 3D validation ready:          false
GPU/HPC ready:                     false
field transfer ready:              false
field FWI ready:                   false
```

All five validation checks pass:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source frequency-aware policy ready | pass |
| 2 | policy rows preserve frequency split | pass |
| 3 | high-frequency endpoint boundary preserved | pass |
| 4 | claim boundary remains analytic BEM only | pass |
| 5 | figure and scripts exist | pass |

## Interpretation

Run `631` guards the run `630` policy. The guarded policy remains:

```text
64 panels: receiver-line sensitivity and broad/low/mid-band sweeps
128 panels: high-frequency-only 2.08-3.00 GHz endpoint checks
no promotion: project FDTD, field transfer, 3D, GPU/HPC, or field FWI
```

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_frequency_aware_panel_policy.py
tests/test_scarep_2d_cpu_bem_frequency_aware_panel_policy_validator.py

6 passed
```

Figure check:

```text
2285x837, dynamic range=255
```

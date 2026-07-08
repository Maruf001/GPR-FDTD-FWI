# BEM Experiment 637: 64/96/128 Frequency-Cost Panel Policy Refresh Validator

Date: 2026-06-30

## Purpose

Validate run `636`, the refreshed scarep two-dimensional CPU BEM panel policy.

## Output

```text
outputs/bem_experiments/637_scarep_2d_cpu_bem_panel64_96_128_frequency_cost_policy_refresh_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel64_96_128_frequency_cost_policy_refresh_validator_check_rows.csv
data/scarep_2d_cpu_bem_panel64_96_128_frequency_cost_policy_refresh_validator_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel64_96_128_frequency_cost_policy_refresh_validator.png
scripts/
```

## Result

```text
validation checks:                 5
failed checks:                     0
policy rows:                       5
64-panel policy rows:              2
96-panel policy rows:              1
128-panel policy rows:             1
blocked downstream policy rows:    1
64-panel high-band relative L2:    0.001736291511432671
96-panel high-band relative L2:    0.0007600368161379071
128-panel high-band relative L2:   0.0004276569548253307
96-panel wall time vs 128-panel:   0.5702697635429481
project FDTD comparison ready:     false
real 3D validation ready:          false
GPU/HPC ready:                     false
field transfer ready:              false
field FWI ready:                   false
```

All five validation checks pass:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source refreshed policy ready | pass |
| 2 | policy rows preserve 64 96 128 split | pass |
| 3 | high-frequency cost and strict endpoint roles preserved | pass |
| 4 | claim boundary remains analytic BEM only | pass |
| 5 | figure and scripts exist | pass |

## Interpretation

Run `637` validates the refreshed policy:

```text
64 panels: receiver-line and broad/low/mid sweeps
96 panels: lower-cost high-frequency candidate
128 panels: strict high-frequency endpoint
```

The policy remains analytic BEM evidence only.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel64_96_128_frequency_cost_policy_refresh.py
tests/test_scarep_2d_cpu_bem_panel64_96_128_frequency_cost_policy_refresh_validator.py

6 passed
```

Figure check:

```text
2285x832, dynamic range=255
```

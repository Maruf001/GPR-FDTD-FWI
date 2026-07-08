# BEM Experiment 655: 64/82/84/88/96/128 Frequency-Cost Policy Refresh Validator

Date: 2026-06-30

## Purpose

Validate run `654`, the refreshed scarep 2D CPU BEM panel policy.

Run `654` promoted 84 panels as the minimum guarded high-frequency candidate
and retained 82 panels as the no-go lower bound. This validator checks source
readiness, policy-row shape, the 82-to-84 threshold role, figure output, script
snapshots, and downstream claim boundaries.

## Output

```text
outputs/bem_experiments/655_scarep_2d_cpu_bem_panel64_82_84_88_96_128_frequency_cost_policy_refresh_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel64_82_84_88_96_128_frequency_cost_policy_refresh_validator_check_rows.csv
data/scarep_2d_cpu_bem_panel64_82_84_88_96_128_frequency_cost_policy_refresh_validator_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel64_82_84_88_96_128_frequency_cost_policy_refresh_validator.png
scripts/
```

## Result

```text
checks:                                  5
checks passed:                          5
checks failed:                          0
policy rows:                            8
82-panel no-go reference rows:          1
84-panel policy rows:                   1
88-panel reference rows:                1
96-panel reference rows:                1
128-panel policy rows:                  1
82-panel high-band relative L2:         0.001045485149014675
84-panel high-band relative L2:         0.000995562585853498
84-panel margin below target:           0.000004437414146501962
policy validation ready:                true
project FDTD comparison ready:          false
real 3D validation ready:               false
GPU/HPC ready:                          false
field transfer ready:                   false
field FWI ready:                        false
```

Validator checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | Source refreshed policy ready | pass |
| 2 | Policy rows preserve 64/82/84/88/96/128 split | pass |
| 3 | 82-to-84 high-frequency threshold preserved | pass |
| 4 | Claim boundary remains analytic BEM only | pass |
| 5 | Figure and scripts exist | pass |

## Interpretation

The refreshed policy is internally valid:

```text
82 panels: nearest tested no-go
84 panels: minimum guarded high-frequency candidate
88 panels: wider-margin low-cost reference
128 panels: strict endpoint
```

The claim remains limited to the scarep analytic-cylinder BEM setting.

## Decision

Use run `654` as the current scarep analytic-cylinder panel policy until a
matched project-FDTD comparison or 3D validation changes the boundary.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel64_82_84_88_96_128_frequency_cost_policy_refresh.py
tests/test_scarep_2d_cpu_bem_panel64_82_84_88_96_128_frequency_cost_policy_refresh_validator.py

6 passed
```

Figure check:

```text
2339x874, dynamic range=255
```

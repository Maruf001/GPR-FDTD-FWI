# BEM Experiment 654: 64/82/84/88/96/128 Frequency-Cost Policy Refresh

Date: 2026-06-30

## Purpose

Refresh the scarep 2D CPU BEM panel policy after the guarded 82/84 threshold
bracket.

Runs `648-650` established 84 panels as a narrow but validated high-frequency
pass. Runs `651-653` established 82 panels as the nearest tested no-go lower
side. This run converts those results into the current analytic-cylinder BEM
panel policy.

## Output

```text
outputs/bem_experiments/654_scarep_2d_cpu_bem_panel64_82_84_88_96_128_frequency_cost_policy_refresh
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel64_82_84_88_96_128_frequency_cost_policy_refresh_rows.csv
data/scarep_2d_cpu_bem_panel64_82_84_88_96_128_frequency_cost_policy_refresh_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel64_82_84_88_96_128_frequency_cost_policy_refresh.png
scripts/
```

## Result

```text
policy rows:                               8
64-panel policy rows:                      2
82-panel no-go reference rows:             1
84-panel policy rows:                      1
88-panel reference rows:                   1
96-panel reference rows:                   1
128-panel policy rows:                     1
blocked downstream rows:                   1
82-panel high-band relative L2:            0.001045485149014675
84-panel high-band relative L2:            0.000995562585853498
88-panel high-band relative L2:            0.0009060002386797175
96-panel high-band relative L2:            0.0007600368161379071
128-panel high-band relative L2:           0.0004276569548253307
84-panel margin below target:              0.000004437414146501962
84-panel wall time relative to 88 panels:  0.9087875317580165
84-panel wall time relative to 128 panels: 0.4387780920351586
policy ready:                              true
project FDTD comparison ready:             false
real 3D validation ready:                  false
GPU/HPC ready:                             false
field transfer ready:                      false
field FWI ready:                           false
```

Policy table:

| Context | Recommendation | Role |
| --- | --- | --- |
| Receiver-line sensitivity | 64 panels | default |
| Broad, low, and mid-band sweeps | 64 panels | default |
| High-frequency 2.08-3.00 GHz lower bound | not recommended: 82 panels fail | validated no-go |
| High-frequency 2.08-3.00 GHz minimum guarded use | 84 panels | minimum guarded candidate |
| High-frequency 2.08-3.00 GHz wider-margin low-cost reference | 88 panels | comfortable reference |
| High-frequency 2.08-3.00 GHz reference | 96 panels | validated but superseded reference |
| High-frequency 2.08-3.00 GHz strict endpoint | 128 panels | strict endpoint |
| Project FDTD, field, and 3D transfer | none | blocked downstream |

## Interpretation

The current analytic-cylinder BEM policy is now:

```text
64 panels: default for receiver-line and broad/low/mid-band sweeps
82 panels: nearest tested high-frequency no-go
84 panels: lowest tested passing high-frequency count, narrow margin
88 panels: wider-margin low-cost reference
96 panels: validated superseded reference
128 panels: strict high-frequency endpoint
```

This is still an analytic-cylinder BEM policy. It does not validate project
FDTD comparison, 3D finite-rebar modeling, GPU/HPC use, field transfer, or
field FWI.

## Decision

Use 84 panels as the minimum guarded high-frequency candidate, with 88 panels
as the wider-margin low-cost reference and 128 panels as the strict endpoint.
Keep all downstream transfer claims blocked until matched project-FDTD or 3D
evidence exists.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel64_82_84_88_96_128_frequency_cost_policy_refresh.py

3 passed
```

Figure check:

```text
2626x862, dynamic range=255
```

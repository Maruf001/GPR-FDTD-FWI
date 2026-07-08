# BEM Experiment 646: 64/88/96/128 Frequency-Cost Policy Refresh Validator

Date: 2026-06-30

## Purpose

Validate run `645`, the refreshed scarep 2D CPU BEM panel policy.

Run `645` changed the high-frequency cost-aware candidate from 96 panels to
88 panels while retaining 96 panels as a validated reference and 128 panels as
the strict endpoint. This validator checks source readiness, policy-row shape,
the 80/88/96/128 threshold roles, figure output, script snapshots, and
downstream claim boundaries.

## Output

```text
outputs/bem_experiments/646_scarep_2d_cpu_bem_panel64_88_96_128_frequency_cost_policy_refresh_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel64_88_96_128_frequency_cost_policy_refresh_validator_check_rows.csv
data/scarep_2d_cpu_bem_panel64_88_96_128_frequency_cost_policy_refresh_validator_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel64_88_96_128_frequency_cost_policy_refresh_validator.png
scripts/
```

## Result

```text
checks:                                   5
checks passed:                           5
checks failed:                           0
policy rows:                             7
64-panel policy rows:                    2
80-panel no-go reference rows:           1
88-panel policy rows:                    1
96-panel reference rows:                 1
128-panel policy rows:                   1
blocked downstream rows:                 1
88-panel high-band relative L2:          0.0009060002386797175
96-panel high-band relative L2:          0.0007600368161379071
128-panel high-band relative L2:         0.0004276569548253307
policy validation ready:                 true
project FDTD comparison ready:           false
real 3D validation ready:                false
GPU/HPC ready:                           false
field transfer ready:                    false
field FWI ready:                         false
```

Validator checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | Source refreshed policy ready | pass |
| 2 | Policy rows preserve 64/80/88/96/128 split | pass |
| 3 | High-frequency candidate, reference, and endpoint roles preserved | pass |
| 4 | Claim boundary remains analytic BEM only | pass |
| 5 | Figure and scripts exist | pass |

## Interpretation

The refreshed panel policy is internally valid and keeps its claim boundary:

```text
64 panels: default receiver and broad/low/mid sweeps
80 panels: no-go lower bound
88 panels: guarded lower-cost high-frequency candidate
96 panels: validated superseded reference
128 panels: strict endpoint
```

## Decision

Use run `645` as the current scarep analytic-cylinder panel policy until a
matched project-FDTD comparison or 3D validation changes the boundary.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel64_88_96_128_frequency_cost_policy_refresh.py
tests/test_scarep_2d_cpu_bem_panel64_88_96_128_frequency_cost_policy_refresh_validator.py

6 passed
```

Figure check:

```text
2303x869, dynamic range=255
```

# BEM Experiment 645: 64/88/96/128 Frequency-Cost Policy Refresh

Date: 2026-06-30

## Purpose

Refresh the scarep 2D CPU BEM panel policy after the guarded 88-panel
high-frequency bridge result.

Runs `639-641` established 80 panels as a validated high-frequency no-go.
Runs `642-644` established 88 panels as a guarded lower-cost high-frequency
candidate. Earlier runs already established 64 panels as the default
receiver/broad-band setting, 96 panels as a valid but more expensive
high-frequency candidate, and 128 panels as the strict endpoint.

## Output

```text
outputs/bem_experiments/645_scarep_2d_cpu_bem_panel64_88_96_128_frequency_cost_policy_refresh
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel64_88_96_128_frequency_cost_policy_refresh_rows.csv
data/scarep_2d_cpu_bem_panel64_88_96_128_frequency_cost_policy_refresh_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel64_88_96_128_frequency_cost_policy_refresh.png
scripts/
```

## Result

```text
policy rows:                               7
64-panel policy rows:                      2
80-panel no-go reference rows:             1
88-panel policy rows:                      1
96-panel validated-reference rows:         1
128-panel policy rows:                     1
blocked downstream rows:                   1
64-panel high-band relative L2:            0.001736291511432671
80-panel high-band relative L2:            0.0010993149385036519
88-panel high-band relative L2:            0.0009060002386797175
96-panel high-band relative L2:            0.0007600368161379071
128-panel high-band relative L2:           0.0004276569548253307
88-panel wall time relative to 96 panels:  0.8466467195355962
88-panel wall time relative to 128 panels: 0.4828170245539772
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
| High-frequency 2.08-3.00 GHz lower bound | not recommended: 80 panels fail | validated no-go |
| High-frequency 2.08-3.00 GHz cost-aware use | 88 panels | cost-aware candidate |
| High-frequency 2.08-3.00 GHz reference | 96 panels | validated but superseded reference |
| High-frequency 2.08-3.00 GHz strict endpoint | 128 panels | strict endpoint |
| Project FDTD, field, and 3D transfer | none | blocked downstream |

## Interpretation

The current analytic-cylinder BEM policy is now sharper than the previous
64/96/128 policy:

```text
64 panels: default for receiver-line and broad/low/mid-band sweeps
80 panels: validated no-go for high-frequency-only work
88 panels: guarded lower-cost high-frequency candidate
96 panels: valid but superseded high-frequency reference
128 panels: strict high-frequency endpoint
```

This is still an analytic-cylinder BEM policy. It does not validate project
FDTD comparison, 3D finite-rebar modeling, GPU/HPC use, field transfer, or
field FWI.

## Decision

Use 64 panels for receiver-line and broad/low/mid sweeps, 88 panels as the
lower-cost high-frequency candidate, and 128 panels as the strict
high-frequency endpoint. Keep 96 panels as a validated reference. Keep all
downstream transfer claims blocked until matched project-FDTD or 3D evidence
exists.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel64_88_96_128_frequency_cost_policy_refresh.py

3 passed
```

Figure check:

```text
2536x862, dynamic range=255
```

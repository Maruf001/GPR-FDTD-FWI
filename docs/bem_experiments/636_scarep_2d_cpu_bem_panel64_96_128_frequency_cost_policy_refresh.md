# BEM Experiment 636: 64/96/128 Frequency-Cost Panel Policy Refresh

Date: 2026-06-30

## Purpose

Refresh the scarep two-dimensional CPU BEM panel policy after the guarded
96-panel bridge result from runs `633-635`.

The earlier policy used 64 panels for default sweeps and 128 panels for
high-frequency endpoint checks. The new evidence shows that 96 panels also
pass the high-frequency target at lower wall time, while 128 panels still give
the smaller high-band error.

## Output

```text
outputs/bem_experiments/636_scarep_2d_cpu_bem_panel64_96_128_frequency_cost_policy_refresh
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel64_96_128_frequency_cost_policy_refresh_rows.csv
data/scarep_2d_cpu_bem_panel64_96_128_frequency_cost_policy_refresh_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel64_96_128_frequency_cost_policy_refresh.png
scripts/
```

## Result

```text
policy rows:                         5
64-panel policy rows:                2
96-panel policy rows:                1
128-panel policy rows:               1
blocked downstream policy rows:      1
64-panel high-band relative L2:      0.001736291511432671
96-panel high-band relative L2:      0.0007600368161379071
128-panel high-band relative L2:     0.0004276569548253307
96-panel wall time vs 128-panel:     0.5702697635429481
96-panel improvement vs 64 panels:   2.2844834283891116x
96-panel gap vs 128 panels:          1.7772114017140943x
project FDTD comparison ready:       false
real 3D validation ready:            false
GPU/HPC ready:                       false
field transfer ready:                false
field FWI ready:                     false
```

Policy:

| Context | Recommended panels | Role |
| --- | ---: | --- |
| receiver-line sensitivity | 64 | default |
| broad/low/mid-band sweeps | 64 | default |
| high-frequency 2.08-3.00 GHz cost-aware work | 96 | cost-aware candidate |
| high-frequency 2.08-3.00 GHz strict endpoint | 128 | strict endpoint |
| project FDTD, field, or 3D transfer | none | blocked downstream |

## Interpretation

The panel policy is now three-tiered:

```text
64 panels:  default receiver-line and broad/low/mid-frequency sweeps
96 panels:  lower-cost high-frequency candidate
128 panels: strict high-frequency endpoint confirmation
```

This policy is only for the scarep analytic-cylinder BEM setup. It does not
validate project FDTD comparison, field transfer, 3D validation, GPU/HPC work,
or field FWI.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel64_96_128_frequency_cost_policy_refresh.py

3 passed
```

Figure check:

```text
2464x834, dynamic range=255
```

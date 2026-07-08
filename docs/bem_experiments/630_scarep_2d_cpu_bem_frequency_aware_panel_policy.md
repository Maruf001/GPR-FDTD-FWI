# BEM Experiment 630: Frequency-Aware 64/128 Panel Policy

Date: 2026-06-30

## Purpose

Convert the recent 64-panel and 128-panel frequency-subset findings into one
frequency-aware operating policy for the two-dimensional scarep CPU BEM
analytic-cylinder setup.

## Output

```text
outputs/bem_experiments/630_scarep_2d_cpu_bem_frequency_aware_panel_policy
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_frequency_aware_panel_policy_rows.csv
data/scarep_2d_cpu_bem_frequency_aware_panel_policy_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_frequency_aware_panel_policy.png
scripts/
```

## Result

```text
policy rows:                         4
64-panel policy rows:                2
128-panel policy rows:               1
blocked downstream policy rows:      1
receiver-line default panels:        64
broad/low/mid-band default panels:   64
high-frequency endpoint panels:      128
64-panel high-band relative L2:      0.001736291511432671
128-panel high-band relative L2:     0.0004276569548253307
high-band improvement factor:        4.060009995960033
project FDTD comparison ready:       false
real 3D validation ready:            false
GPU/HPC ready:                       false
field transfer ready:                false
field FWI ready:                     false
```

Policy table:

| Context | Recommended panels | Basis | 64-panel relative L2 | 128-panel relative L2 |
| --- | ---: | --- | ---: | ---: |
| receiver-line sensitivity | 64 | all receiver and scan-line subsets below `1e-3` | 0.0007704118971318319 | |
| broad/low/mid-band sweeps | 64 | full, low, and mid frequency bands below `1e-3` | 0.0009503011515443673 | |
| high-frequency-only 2.08-3.00 GHz | 128 | 64 panels fail high band and 128 panels close the gap | 0.001736291511432671 | 0.0004276569548253307 |
| project FDTD, field, or 3D transfer | none | not validated by scarep analytic-cylinder BEM alone | | |

## Interpretation

The BEM panel policy is no longer one-size-fits-all:

```text
Use 64 panels for default two-dimensional analytic-cylinder BEM sweeps,
receiver-line sensitivity studies, and broad/low/mid-band checks.

Use 128 panels when a claim depends on the high-frequency-only 2.08-3.00 GHz
band.
```

This remains a two-dimensional analytic-cylinder BEM policy. It does not
validate project FDTD comparisons, field transfer, three-dimensional Maxwell
modeling, GPU/HPC execution, or field FWI.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_frequency_aware_panel_policy.py

3 passed
```

Figure check:

```text
2356x841, dynamic range=255
```

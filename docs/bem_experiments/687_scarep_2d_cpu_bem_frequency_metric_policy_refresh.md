# BEM Experiment 687: Frequency Metric Policy Refresh

Date: 2026-06-30

## Purpose

Convert the dense-frequency and frequency-anatomy findings into the current
BEM transfer metric policy.

Runs `681-683` showed that the denser 49-frequency aggregate result supports
the 116-panel recommendation. Runs `684-686` showed why that result should not
lower the policy to 114 panels: the aggregate high-band metric is
frequency-grid sensitive, while the worst per-frequency error did not improve.

## Output

```text
outputs/bem_experiments/687_scarep_2d_cpu_bem_frequency_metric_policy_refresh
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_frequency_metric_policy_refresh_rows.csv
data/scarep_2d_cpu_bem_frequency_metric_policy_refresh_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_frequency_metric_policy_refresh.png
scripts/
```

## Result

```text
policy rows:                         5
nearest no-go panel:                 113
minimum passing panel:               114
guarded recommended panel:           116
guard margin:                        2.5e-05
minimum passing margin:              1.5199423897917664e-05
guarded recommended margin:          4.9382924375243283e-05
dense frequency count:               49
dense 116-panel minimum margin:      0.0002368575405765187
aggregate metric grid-sensitive:     true
116-panel worst per-frequency L2:    0.002033505195979887
per-frequency diagnostic required:   true
lower panel policy change ready:     false
project FDTD comparison ready:       false
real 3D validation ready:            false
GPU/HPC ready:                       false
field transfer ready:                false
field FWI ready:                     false
```

## Interpretation

The current metric policy is:

```text
Use aggregate high-band relative L2 as the comparable acceptance metric only
on a fixed frequency grid.
Use the configured guard margin before recommending a lower-cost panel endpoint.
Use per-frequency error anatomy when aggregate metrics change across grids.
Keep 116 panels as the guarded analytic transfer endpoint.
Do not lower the policy to 114 panels from dense-grid aggregate results alone.
```

## Decision

Keep 116 panels as the guarded analytic transfer endpoint. Keep project-FDTD,
real 3D, GPU/HPC, field transfer, and field FWI claims blocked.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_frequency_metric_policy_refresh.py
3 passed
```

Figure check:

```text
1924x847, dynamic range=255
```

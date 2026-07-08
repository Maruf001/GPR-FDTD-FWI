# BEM Experiment 678: 113/114/116 Transfer Margin Policy Refresh

Date: 2026-06-30

## Purpose

Convert the closed panel threshold into a usable analytic transfer policy.

Runs `675-677` established that 113 panels are the nearest tested lower-side
no-go and 114 panels are the minimum tested pass. The 114-panel margin is very
tight, so this run separates the minimum passing panel from the guarded
recommended endpoint.

## Output

```text
outputs/bem_experiments/678_scarep_2d_cpu_bem_panel113_114_116_transfer_margin_policy_refresh
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel113_114_116_transfer_margin_policy_refresh_rows.csv
data/scarep_2d_cpu_bem_panel113_114_116_transfer_margin_policy_refresh_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel113_114_116_transfer_margin_policy_refresh.png
scripts/
```

## Result

```text
target relative L2:                    0.001
guard margin:                          0.000025
nearest no-go panel:                   113
nearest no-go max high-band L2:        0.0010026008820656063
minimum passing panel:                 114
minimum passing margin:                0.000015199423897917664
guarded recommended panel:             116
guarded recommended margin:            0.000049382924375243283
panel-113 validation ready:            true
panel-113 sensitivity ready:           true
panel-114 validation ready:            true
panel-114 sensitivity ready:           true
project FDTD comparison ready:         false
real 3D validation ready:              false
GPU/HPC ready:                         false
field transfer ready:                  false
field FWI ready:                       false
```

## Interpretation

The minimum demonstrated pass is 114 panels. Because its margin is smaller
than the configured guard margin, 114 panels should be treated as a threshold
result, not the guarded operating point.

The guarded recommendation is 116 panels for these analytic transfer variants.

## Decision

Use 114 panels as the minimum validated analytic pass. Use 116 panels as the
guarded recommended material/geometry transfer endpoint. Keep project-FDTD,
3D, field, GPU/HPC, and field-FWI claims blocked.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel113_114_116_transfer_margin_policy_refresh.py

3 passed
```

Figure check:

```text
2464x854, dynamic range=255
```

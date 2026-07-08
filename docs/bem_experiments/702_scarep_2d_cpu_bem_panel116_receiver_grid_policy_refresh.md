# BEM Experiment 702: 116-Panel Receiver-Grid Policy Refresh

Date: 2026-06-30

## Purpose

Refresh the guarded analytic BEM receiver-grid policy after the 25-frequency
and 49-frequency receiver-grid audits.

This run reads validated artifacts from runs `696-701` and the frequency-metric
policy from run `687`. It does not run new BEM solves, compare against project
FDTD outputs, run 3D Maxwell BEM, launch GPU/HPC work, or promote field
transfer.

## Output

```text
outputs/bem_experiments/702_scarep_2d_cpu_bem_panel116_receiver_grid_policy_refresh
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel116_receiver_grid_policy_refresh_metric_rows.csv
data/scarep_2d_cpu_bem_panel116_receiver_grid_policy_refresh_policy_rows.csv
data/scarep_2d_cpu_bem_panel116_receiver_grid_policy_refresh_summary.json
figures/scarep_2d_cpu_bem_panel116_receiver_grid_policy_refresh.png
scripts/script_snapshot_manifest.json
```

## Result

```text
metric rows:                               2
policy rows:                               5
guarded receiver-grid panel:               116
frequency grids covered:                   2
scan-count variants covered:               3
target relative L2:                        0.001
guard margin:                              0.000025
worst 116-panel high-band relative L2:     0.0009518291083452528
minimum margin to target:                  0.000048170891654747265
guard margin ready:                        true
receiver-grid policy ready:                true
per-frequency diagnostic required:         true
lower-panel policy change ready:           false
project-FDTD comparison ready:             false
3D validation ready:                       false
field transfer ready:                      false
field FWI ready:                           false
```

Metric table:

| Frequency count | Scan counts | Panel | Max high-band L2 | Margin to 0.001 | Pass count |
| ---: | --- | ---: | ---: | ---: | ---: |
| 25 | 9, 11, 13 | 116 | 0.0009518291083452528 | 0.000048170891654747265 | 3 |
| 49 | 9, 11, 13 | 116 | 0.0007643703508458867 | 0.00023562964915411328 | 3 |

Policy rows:

| Policy item | Value |
| --- | --- |
| guarded receiver-grid endpoint | 116 panels |
| fixed frequency grid required | true |
| guard margin required | 0.000025 |
| per-frequency anatomy required when grid changes | true |
| claim boundary | analytic-cylinder BEM only |

## Interpretation

The 116-panel endpoint remains receiver-grid robust across the tested 9, 11,
and 13 scan-position layouts on both aggregate frequency grids. The controlling
margin is the 25-frequency receiver-grid result, not the dense 49-frequency
result.

The dense-grid aggregate improvement still does not justify lowering the
policy to 114 panels, because run `684` showed that per-frequency worst errors
did not improve when the aggregate error dropped.

## Decision

Keep 116 panels as the receiver-grid guarded analytic BEM endpoint. Preserve
the fixed-frequency-grid comparison rule, the per-frequency diagnostic guard,
and the analytic-only claim boundary.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_receiver_grid_policy_refresh.py
tests/test_scarep_2d_cpu_bem_panel116_receiver_grid_policy_refresh_validator.py
tests/test_scarep_2d_cpu_bem_panel116_receiver_grid_policy_refresh_validation_sensitivity.py
9 passed
```

Figure check:

```text
2464x854, dynamic range=255
```


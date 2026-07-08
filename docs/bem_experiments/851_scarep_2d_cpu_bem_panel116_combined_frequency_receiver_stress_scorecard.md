# BEM Experiment 851: 116-Panel Combined Frequency/Receiver Stress Scorecard

Date: 2026-07-01

## Purpose

Combine the validated 25-frequency and 49-frequency receiver-grid checks into
one scorecard for the current 116-panel analytic 2D BEM endpoint.

This run does not launch new BEM solves, project FDTD, 3D Maxwell BEM,
GPU/HPC work, field transfer, or field FWI. It reads the validated receiver
and frequency-grid artifacts and asks whether the active endpoint remains
stable when those checks are evaluated together.

## Output

```text
outputs/bem_experiments/851_scarep_2d_cpu_bem_panel116_combined_frequency_receiver_stress_scorecard
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel116_combined_frequency_receiver_stress_scorecard_stress_rows.csv
data/scarep_2d_cpu_bem_panel116_combined_frequency_receiver_stress_scorecard_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel116_combined_frequency_receiver_stress_scorecard.png
scripts/
```

## Result

```text
stress rows:                              6
frequency grids:                          2
scan-count variants:                      3
tested panel count:                       116
target high-band relative L2:             0.001
guard margin:                             2.5e-05
maximum high-band relative L2:            0.0009518291083452528
minimum margin to target:                 4.8170891654747265e-05
passing stress rows:                      6
guard-margin passing rows:                6
controlling frequency grid:               25
controlling scan positions:               13
25f/49f worst-grid sensitivity ratio:     1.2452459822544342
lower-panel policy change ready:          false
project-FDTD comparison ready:            false
real 3D validation ready:                 false
field transfer ready:                     false
field FWI ready:                          false
```

## Interpretation

The 116-panel endpoint passes all combined receiver/frequency stress rows. The
controlling row is the 25-frequency, 13-scan layout, with high-band relative L2
of `0.0009518291083452528`. The dense 49-frequency grid is less controlling in
the aggregate scorecard, so the fixed-frequency-grid and per-frequency
diagnostic guards remain necessary.

## Decision

Keep 116 panels as the guarded analytic 2D BEM endpoint. Do not lower the
panel policy, and do not promote project-FDTD comparison, field transfer, or
3D validation from this scorecard.

## Validation

Figure check:

```text
2897x854, dynamic range=255
```

Script snapshots:

```text
2
```

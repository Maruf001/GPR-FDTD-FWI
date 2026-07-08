# BEM Experiment 857: 116-Panel Controlling Receiver Frequency Anatomy Audit

Date: 2026-07-01

## Purpose

Run a per-frequency diagnostic for the controlling row found by run `851`: the
116-panel, 25-frequency, 13-scan receiver layout.

This run performs fresh CPU BEM solves for the 25-frequency and 49-frequency
grids at the 13-scan layout. It compares only against the analytic 2D
dielectric-cylinder reference. It does not run project FDTD, 3D Maxwell BEM,
GPU/HPC work, field transfer, or field FWI.

## Output

```text
outputs/bem_experiments/857_scarep_2d_cpu_bem_panel116_controlling_receiver_frequency_anatomy_audit
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel116_controlling_receiver_frequency_anatomy_audit_grid_rows.csv
data/scarep_2d_cpu_bem_panel116_controlling_receiver_frequency_anatomy_audit_frequency_error_rows.csv
data/scarep_2d_cpu_bem_panel116_controlling_receiver_frequency_anatomy_audit_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel116_controlling_receiver_frequency_anatomy_audit.png
scripts/
```

## Result

```text
scan positions:                         13
panel count:                            116
frequency grids:                        2
grid rows:                              2
frequency-error rows:                   74
high-band frequency-error rows:         27
25-frequency high-band relative L2:     0.0009518291083452528
49-frequency high-band relative L2:     0.0007643703508458867
25-frequency margin to target:          4.8170891654747265e-05
49-frequency margin to target:          0.00023562964915411328
25-frequency max bin relative L2:       0.0020304660813911003
49-frequency max bin relative L2:       0.0020304660813911003
worst high-band frequency:              2.3125 GHz
aggregate metric grid sensitive:        true
aggregate pass but bin exceeds target:  true
lower-panel policy change ready:        false
project-FDTD comparison ready:          false
real 3D validation ready:               false
field transfer ready:                   false
field FWI ready:                        false
```

## Interpretation

The controlling 13-scan receiver layout passes the aggregate high-band metric
on both frequency grids. The individual high-band bin at `2.3125 GHz` is still
above the aggregate target, with relative L2 `0.0020304660813911003`.

This confirms why the 116-panel endpoint should be treated as an aggregate
analytic endpoint rather than a per-frequency guarantee.

## Decision

Keep 116 panels as the guarded aggregate analytic endpoint. Preserve the
per-frequency diagnostic guard. Do not lower the panel policy or promote
project-FDTD, field-transfer, or real-3D claims from this anatomy audit.

## Validation

Figure check:

```text
2608x870, dynamic range=255
```

Script snapshots:

```text
2
```

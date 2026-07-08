# BEM Experiment 684: 114/116 Frequency-Grid Anatomy Audit

Date: 2026-06-30

## Purpose

Explain why run `681` produced lower aggregate high-band errors on the denser
49-frequency grid.

The target case is the larger-radius variant, because that case controlled the
113/114/116 panel decision. This run compares 25-frequency and 49-frequency
sampling for 114 and 116 panels, and records both aggregate high-band relative
L2 and per-frequency relative L2.

## Output

```text
outputs/bem_experiments/684_scarep_2d_cpu_bem_panel114_116_frequency_grid_anatomy_audit
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel114_116_frequency_grid_anatomy_audit_grid_panel_rows.csv
data/scarep_2d_cpu_bem_panel114_116_frequency_grid_anatomy_audit_frequency_error_rows.csv
data/scarep_2d_cpu_bem_panel114_116_frequency_grid_anatomy_audit_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel114_116_frequency_grid_anatomy_audit.png
scripts/
```

## Result

```text
target case:                         radius_75mm_baseline_eps
grid rows:                           4
frequency-error rows:                148
114-panel 25-frequency high-band L2: 0.0009848005761020824
114-panel 49-frequency high-band L2: 0.0007904252030039112
116-panel 25-frequency high-band L2: 0.0009506170756247567
116-panel 49-frequency high-band L2: 0.0007631424594234813
114-panel 25-frequency max bin L2:   0.002107396735185063
114-panel 49-frequency max bin L2:   0.002107396735185063
116-panel 25-frequency max bin L2:   0.002033505195979887
116-panel 49-frequency max bin L2:   0.002033505195979887
aggregate metric grid-sensitive:     true
lower panel policy change ready:     false
project FDTD comparison ready:       false
real 3D validation ready:            false
GPU/HPC ready:                       false
field transfer ready:                false
field FWI ready:                     false
```

## Interpretation

The denser grid lowers the aggregate high-band relative L2 because the
aggregate metric depends on the sampled frequency grid. It does not remove the
worst per-frequency error: the maximum high-band bin error is unchanged for
both 114 and 116 panels.

This explains why run `681` should be treated as support for the guarded
116-panel policy, not as permission to lower the policy to 114 panels.

## Decision

Keep 116 panels as the guarded transfer endpoint. Do not lower the panel policy
from the dense-grid aggregate result alone.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel114_116_frequency_grid_anatomy_audit.py
3 passed
```

Figure check:

```text
2572x870, dynamic range=255
```

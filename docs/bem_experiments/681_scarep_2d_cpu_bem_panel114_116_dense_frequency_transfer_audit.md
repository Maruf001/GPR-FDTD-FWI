# BEM Experiment 681: 114/116 Dense-Frequency Transfer Audit

Date: 2026-06-30

## Purpose

Test whether the margin-aware 114/116-panel analytic transfer policy survives a
denser frequency grid.

Run `678` established that 113 panels are the nearest no-go, 114 panels are
the minimum passing panel with a very tight margin on the original grid, and
116 panels are the guarded recommendation. This run repeats the same four
material/geometry variants on a 49-frequency grid for 114, 116, and 128
panels.

## Output

```text
outputs/bem_experiments/681_scarep_2d_cpu_bem_panel114_116_dense_frequency_transfer_audit
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel114_116_dense_frequency_transfer_audit_solve_rows.csv
data/scarep_2d_cpu_bem_panel114_116_dense_frequency_transfer_audit_case_rows.csv
data/scarep_2d_cpu_bem_panel114_116_dense_frequency_transfer_audit_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel114_116_dense_frequency_transfer_audit.png
scripts/
```

## Result

```text
frequency samples:                    49
variant cases:                        4
solve rows:                           12
114-panel transfer pass count:         4
116-panel transfer pass count:         4
128-panel transfer pass count:         4
114-panel guard pass count:            4
116-panel guard pass count:            4
128-panel guard pass count:            4
114-panel max high-band L2:            0.0007904252030039112
116-panel max high-band L2:            0.0007631424594234813
128-panel max high-band L2:            0.0006260191501451638
114-panel minimum margin:              0.00020957479699608883
116-panel minimum margin:              0.0002368575405765187
minimum dense-frequency passing panel: 114
guarded dense-frequency panel:         114
116-panel guard survives:              true
project FDTD comparison ready:         false
real 3D validation ready:              false
GPU/HPC ready:                         false
field transfer ready:                  false
field FWI ready:                       false
```

## Interpretation

The denser 49-frequency audit does not weaken the panel policy. It strengthens
the analytic evidence: both 114 and 116 panels pass all four transfer variants
with margins comfortably larger than the configured guard margin.

This does not replace the earlier policy by itself, because the original
coarse-grid run `672` still showed 114 panels as a tight-margin pass. The
conservative interpretation is that 116 panels remain the guarded analytic
transfer endpoint, while run `681` adds dense-frequency support for that
choice.

## Decision

Keep 116 panels as the guarded analytic material/geometry transfer endpoint for
these 2D scalar BEM variants. Keep project-FDTD comparison, real 3D validation,
GPU/HPC, field transfer, and field FWI claims blocked.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel114_116_dense_frequency_transfer_audit.py
4 passed
```

Figure check:

```text
2608x884, dynamic range=255
```

# BEM Experiment 863: 116-Panel Frequency-Bin Policy Matrix

Date: 2026-07-01

## Purpose

Convert the validated run `860-862` frequency-bin exceedance result into an
explicit policy matrix.

This run does not run new BEM solves, project FDTD, field transfer, field FWI,
or 3D/HPC work.

## Output

```text
outputs/bem_experiments/863_scarep_2d_cpu_bem_panel116_frequency_bin_policy_matrix
```

## Result

```text
policy rows:                              5
accepted policy rows:                     1
blocked policy rows:                      4
total high-band bins:                     27
total bins above target:                  5
worst frequency:                          2.3125 GHz
worst per-frequency relative L2:          0.0020304660813911003
aggregate endpoint with diagnostic ready: true
hard per-frequency endpoint ready:        false
lower-panel policy change ready:          false
project-FDTD comparison ready:            false
real 3D validation ready:                 false
field transfer ready:                     false
field FWI ready:                          false
```

## Interpretation

The accepted policy is narrow: use 116 panels as an aggregate analytic endpoint
only when the per-frequency diagnostic guard is preserved.

The hard per-frequency endpoint is not accepted, because five high-band bins
remain above the aggregate target. Lower-panel, project-FDTD, field-transfer,
and real-3D claims remain blocked.

## Decision

Use this as the current 116-panel frequency-bin policy matrix.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_frequency_bin_policy_matrix.py
3 passed
```

Figure check:

```text
2537x880, dynamic range=255
```

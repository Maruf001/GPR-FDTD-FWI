# BEM Experiment 860: 116-Panel Frequency-Bin Exceedance Scorecard

Date: 2026-07-01

## Purpose

Score how many high-band frequency bins exceed the aggregate target in the
controlling 116-panel analytic BEM receiver layout.

This run reads the saved run `857` frequency-error rows. It does not run new
BEM solves, project FDTD, field transfer, field FWI, or 3D/HPC work.

## Output

```text
outputs/bem_experiments/860_scarep_2d_cpu_bem_panel116_frequency_bin_exceedance_scorecard
```

## Result

```text
score rows:                              2
frequency grids:                         2
total high-band bins:                    27
total bins above target:                 5
maximum above-target fraction:           0.2222222222222222
worst frequency grid:                    25
worst frequency:                         2.3125 GHz
worst per-frequency relative L2:         0.0020304660813911003
aggregate pass but bin exceeds target:   true
per-frequency diagnostic required:       true
lower-panel policy change ready:         false
project-FDTD comparison ready:           false
field transfer ready:                    false
field FWI ready:                         false
```

## Interpretation

The per-frequency issue is concentrated rather than broad. Five of twenty-seven
high-band bins exceed the aggregate target, with the worst bin at `2.3125 GHz`.

This supports the current claim boundary: 116 panels remains a guarded
aggregate analytic endpoint, but per-frequency diagnostics must remain part of
the policy.

## Decision

Keep 116 panels as an aggregate analytic endpoint. Preserve the per-frequency
diagnostic guard and do not promote project-FDTD, field-transfer, or real-3D
claims from this scorecard.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_frequency_bin_exceedance_scorecard.py
3 passed
```

Figure check:

```text
2465x854, dynamic range=255
```

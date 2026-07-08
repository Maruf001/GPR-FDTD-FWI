# BEM Experiment 651: 82-Panel Frequency-Subset Bridge Audit

Date: 2026-06-30

## Purpose

Test whether the high-frequency panel threshold can move below the narrow
84-panel pass.

Runs `648-650` showed that 84 panels pass all nine frequency subsets, but only
barely. This run tests 82 panels on the same scarep analytic-cylinder scan.

## Output

```text
outputs/bem_experiments/651_scarep_2d_cpu_bem_panel82_frequency_subset_bridge_audit
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel82_frequency_subset_bridge_audit_rows.csv
data/scarep_2d_cpu_bem_panel82_frequency_subset_bridge_audit_summary.json
data/scarep_2d_cpu_bem_panel82_frequency_subset_bridge_audit_arrays.npz
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel82_frequency_subset_bridge_audit.png
scripts/
```

## Result

```text
panels:                                  82
scan positions:                          11
frequencies:                             25
wall seconds:                            33.33186760591343
full-band relative L2:                   0.0004306652790451734
low-band relative L2:                    0.00024383555669988175
mid-band relative L2:                    0.0005804272465836457
high-band relative L2:                   0.001045485149014675
80-panel high-band relative L2:          0.0010993149385036519
84-panel high-band relative L2:          0.000995562585853498
96-panel high-band relative L2:          0.0007600368161379071
128-panel high-band relative L2:         0.0004276569548253307
frequency subsets tested:                9
frequency subsets passing < 1e-3:        8
frequency subsets failing >= 1e-3:       1
82-panel high-frequency bridge ready:    false
project FDTD comparison ready:           false
real 3D validation ready:                false
GPU/HPC ready:                           false
field transfer ready:                    false
field FWI ready:                         false
```

The failing subset is the high-frequency-only 2.08-3.00 GHz band:

| Subset | Relative L2 | Passes `1e-3` |
| --- | ---: | --- |
| full 25-bin band | 0.0004306652790451734 | yes |
| low 0.25-0.94 GHz | 0.00024383555669988175 | yes |
| mid 1.05-1.97 GHz | 0.0005804272465836457 | yes |
| high 2.08-3.00 GHz | 0.001045485149014675 | no |
| even frequency bins | 0.00044694159651236377 | yes |
| odd frequency bins | 0.0004133159468289866 | yes |
| every third bin | 0.0003947784841287573 | yes |
| center band | 0.0005857293016091069 | yes |
| edge low/high band | 0.00015866221543723208 | yes |

## Interpretation

The 82-panel solve improves on 80 panels but does not close the high-frequency
target. The current discrete threshold bracket is now:

```text
80 panels: high band fails
82 panels: high band fails
84 panels: high band passes narrowly
88 panels: high band passes
96 panels: high band passes
128 panels: strict endpoint
```

This supports 84 panels as the current lowest tested passing panel count for
the scarep analytic-cylinder high-frequency subset.

## Decision

Do not promote 82 panels for high-frequency work. Use this as the no-go lower
side of the 82/84 threshold bracket. Keep downstream project-FDTD, 3D, GPU/HPC,
field-transfer, and field-FWI claims blocked.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel82_frequency_subset_bridge_audit.py

3 passed
```

Figure check:

```text
2464x867, dynamic range=255
```

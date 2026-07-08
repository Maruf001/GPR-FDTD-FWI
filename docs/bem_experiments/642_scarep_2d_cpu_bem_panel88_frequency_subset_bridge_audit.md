# BEM Experiment 642: 88-Panel Frequency-Subset Bridge Audit

Date: 2026-06-30

## Purpose

Test whether the high-frequency panel threshold lies above 80 panels but below
96 panels.

Runs `639-641` showed that 80 panels are a validated high-frequency no-go.
Runs `633-638` showed that 96 panels pass all guarded frequency subsets. This
run tests the midpoint, 88 panels, on the same scarep analytic-cylinder scan.

## Output

```text
outputs/bem_experiments/642_scarep_2d_cpu_bem_panel88_frequency_subset_bridge_audit
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel88_frequency_subset_bridge_audit_rows.csv
data/scarep_2d_cpu_bem_panel88_frequency_subset_bridge_audit_summary.json
data/scarep_2d_cpu_bem_panel88_frequency_subset_bridge_audit_arrays.npz
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel88_frequency_subset_bridge_audit.png
scripts/
```

## Result

```text
panels:                                  88
scan positions:                          11
frequencies:                             25
wall seconds:                            38.486762969056144
full-band relative L2:                   0.000374448604515617
low-band relative L2:                    0.00021233901721609338
mid-band relative L2:                    0.0005046977489059122
high-band relative L2:                   0.0009060002386797175
64-panel high-band relative L2:          0.001736291511432671
80-panel high-band relative L2:          0.0010993149385036519
96-panel high-band relative L2:          0.0007600368161379071
128-panel high-band relative L2:         0.0004276569548253307
frequency subsets tested:                9
frequency subsets passing < 1e-3:        9
frequency subsets failing >= 1e-3:       0
88-panel high-frequency bridge ready:    true
project FDTD comparison ready:           false
real 3D validation ready:                false
GPU/HPC ready:                           false
field transfer ready:                    false
field FWI ready:                         false
```

Frequency-subset results:

| Subset | Relative L2 | Passes `1e-3` |
| --- | ---: | --- |
| full 25-bin band | 0.000374448604515617 | yes |
| low 0.25-0.94 GHz | 0.00021233901721609338 | yes |
| mid 1.05-1.97 GHz | 0.0005046977489059122 | yes |
| high 2.08-3.00 GHz | 0.0009060002386797175 | yes |
| even frequency bins | 0.0003886892984412867 | yes |
| odd frequency bins | 0.0003592652819738459 | yes |
| every third bin | 0.0003433444242738302 | yes |
| center band | 0.0005093080334461923 | yes |
| edge low/high band | 0.00013783221569649458 | yes |

## Interpretation

The high-frequency threshold moved downward from the previous 96-panel
candidate. The current bracket is:

```text
64 panels: high band fails
80 panels: high band fails
88 panels: high band passes
96 panels: high band passes
128 panels: strict endpoint
```

The 88-panel solve is about `1.21x` better than the 80-panel high-band error,
about `1.19x` worse than the 96-panel high-band error, about `0.85x` of the
96-panel wall time, and about `0.48x` of the 128-panel wall time.

## Decision

Treat 88 panels as the new lower-cost high-frequency candidate after validator
hardening. Keep 128 panels as the strict endpoint. Do not promote this
analytic-cylinder result to project FDTD comparison, 3D validation, GPU/HPC,
field transfer, or field FWI.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel88_frequency_subset_bridge_audit.py

3 passed
```

Figure check:

```text
2464x867, dynamic range=255
```

# BEM Experiment 639: 80-Panel Frequency-Subset Bridge Audit

Date: 2026-06-30

## Purpose

Test whether the lower-cost high-frequency panel threshold can move below the
guarded 96-panel candidate.

Runs `633-638` showed that 96 panels pass the high-frequency target and support
a refreshed 64/96/128 policy. This run tests an 80-panel candidate on the same
scarep analytic-cylinder scan.

## Output

```text
outputs/bem_experiments/639_scarep_2d_cpu_bem_panel80_frequency_subset_bridge_audit
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel80_frequency_subset_bridge_audit_rows.csv
data/scarep_2d_cpu_bem_panel80_frequency_subset_bridge_audit_summary.json
data/scarep_2d_cpu_bem_panel80_frequency_subset_bridge_audit_arrays.npz
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel80_frequency_subset_bridge_audit.png
scripts/
```

## Result

```text
panels:                                  80
scan positions:                          11
frequencies:                             25
wall seconds:                            31.86359849991277
full-band relative L2:                   0.0004522868417816943
low-band relative L2:                    0.0002559306105787817
mid-band relative L2:                    0.0006095503034557899
high-band relative L2:                   0.0010993149385036519
64-panel high-band relative L2:          0.001736291511432671
96-panel high-band relative L2:          0.0007600368161379071
128-panel high-band relative L2:         0.0004276569548253307
frequency subsets tested:                9
frequency subsets passing < 1e-3:        8
frequency subsets failing >= 1e-3:       1
80-panel high-frequency bridge ready:    false
project FDTD comparison ready:           false
real 3D validation ready:                false
GPU/HPC ready:                           false
field transfer ready:                    false
field FWI ready:                         false
```

The failing subset is the high-frequency-only 2.08-3.00 GHz band:

| Subset | Relative L2 | Passes `1e-3` |
| --- | ---: | --- |
| full 25-bin band | 0.0004522868417816943 | yes |
| low 0.25-0.94 GHz | 0.0002559306105787817 | yes |
| mid 1.05-1.97 GHz | 0.0006095503034557899 | yes |
| high 2.08-3.00 GHz | 0.0010993149385036519 | no |
| even frequency bins | 0.00046933816168262527 | yes |
| odd frequency bins | 0.0004341132042896681 | yes |
| every third bin | 0.0004145565870522167 | yes |
| center band | 0.0006151185066461021 | yes |
| edge low/high band | 0.00016668598541480249 | yes |

## Interpretation

The 80-panel solve improves on 64 panels but does not close the high-frequency
target. The useful bracket is now:

```text
64 panels: high band fails
80 panels: high band fails
96 panels: high band passes
128 panels: stricter high-band endpoint
```

This supports keeping 96 panels as the lower-cost high-frequency candidate for
now, rather than reducing the policy to 80 panels.

## Decision

Do not promote 80 panels for high-frequency work. Keep the guarded run `636`
policy unchanged: 64 panels for default sweeps, 96 panels as the lower-cost
high-frequency candidate, and 128 panels as the strict endpoint.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel80_frequency_subset_bridge_audit.py

3 passed
```

Figure check:

```text
2446x867, dynamic range=255
```

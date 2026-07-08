# BEM Experiment 648: 84-Panel Frequency-Subset Bridge Audit

Date: 2026-06-30

## Purpose

Test whether the high-frequency panel threshold can move below the guarded
88-panel candidate.

Runs `639-641` showed that 80 panels fail the high-frequency-only target.
Runs `642-647` showed that 88 panels pass and support the current
64/88/96/128 panel policy. This run tests the midpoint, 84 panels, on the same
scarep analytic-cylinder scan.

## Output

```text
outputs/bem_experiments/648_scarep_2d_cpu_bem_panel84_frequency_subset_bridge_audit
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel84_frequency_subset_bridge_audit_rows.csv
data/scarep_2d_cpu_bem_panel84_frequency_subset_bridge_audit_summary.json
data/scarep_2d_cpu_bem_panel84_frequency_subset_bridge_audit_arrays.npz
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel84_frequency_subset_bridge_audit.png
scripts/
```

## Result

```text
panels:                                  84
scan positions:                          11
frequencies:                             25
wall seconds:                            34.97629032400437
full-band relative L2:                   0.0004105770871630673
low-band relative L2:                    0.00023258901593887563
mid-band relative L2:                    0.0005533678757565655
high-band relative L2:                   0.000995562585853498
80-panel high-band relative L2:          0.0010993149385036519
88-panel high-band relative L2:          0.0009060002386797175
96-panel high-band relative L2:          0.0007600368161379071
128-panel high-band relative L2:         0.0004276569548253307
frequency subsets tested:                9
frequency subsets passing < 1e-3:        9
frequency subsets failing >= 1e-3:       0
84-panel high-frequency bridge ready:    true
project FDTD comparison ready:           false
real 3D validation ready:                false
GPU/HPC ready:                           false
field transfer ready:                    false
field FWI ready:                         false
```

Frequency-subset results:

| Subset | Relative L2 | Passes `1e-3` |
| --- | ---: | --- |
| full 25-bin band | 0.0004105770871630673 | yes |
| low 0.25-0.94 GHz | 0.00023258901593887563 | yes |
| mid 1.05-1.97 GHz | 0.0005533678757565655 | yes |
| high 2.08-3.00 GHz | 0.000995562585853498 | yes |
| even frequency bins | 0.00042612942193406367 | yes |
| odd frequency bins | 0.0003939979638312933 | yes |
| every third bin | 0.0003764010606302727 | yes |
| center band | 0.0005584227018450823 | yes |
| edge low/high band | 0.0001512135964370518 | yes |

## Interpretation

The high-frequency threshold moved downward again, but only narrowly. The
84-panel high-band error is just below the `1e-3` target:

```text
target minus 84-panel high-band error = 0.000004437414146502028
```

The current bracket is:

```text
64 panels: high band fails
80 panels: high band fails
84 panels: high band passes narrowly
88 panels: high band passes
96 panels: high band passes
128 panels: strict endpoint
```

## Decision

Treat 84 panels as a narrow-margin candidate pending validator hardening. Do
not update the active policy from run `645` until the 84-panel result is
validated and sensitivity-hardened. Keep downstream project-FDTD, 3D, GPU/HPC,
field-transfer, and field-FWI claims blocked.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel84_frequency_subset_bridge_audit.py

3 passed
```

Figure check:

```text
2464x867, dynamic range=255
```

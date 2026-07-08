# BEM Experiment 633: 96-Panel Frequency-Subset Bridge Audit

Date: 2026-06-30

## Purpose

Test whether a 96-panel scarep CPU BEM solve can close the high-frequency-only
failure seen at 64 panels, without paying the full 128-panel endpoint cost.

Run `624` showed that 64 panels pass broad, low, and mid-frequency subsets but
fail the 2.08-3.00 GHz high-frequency-only subset. Run `627` showed that
128 panels close that high-frequency boundary. This run tests the intermediate
96-panel candidate.

## Output

```text
outputs/bem_experiments/633_scarep_2d_cpu_bem_panel96_frequency_subset_bridge_audit
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel96_frequency_subset_bridge_audit_rows.csv
data/scarep_2d_cpu_bem_panel96_frequency_subset_bridge_audit_summary.json
data/scarep_2d_cpu_bem_panel96_frequency_subset_bridge_audit_arrays.npz
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel96_frequency_subset_bridge_audit.png
scripts/
```

## Result

```text
panels:                                  96
scan positions:                          11
frequencies:                             25
wall seconds:                            45.45787762594409
full-band relative L2:                   0.0003153081842055151
low-band relative L2:                    0.00017912306537916088
mid-band relative L2:                    0.00042501637547310596
high-band relative L2:                   0.0007600368161379071
64-panel high-band relative L2:          0.001736291511432671
128-panel high-band relative L2:         0.0004276569548253307
high-band improvement vs 64 panels:      2.2844834283891116x
high-band gap vs 128 panels:             1.7772114017140943x
wall seconds relative to 128 panels:     0.5702697635429481
frequency subsets tested:                9
frequency subsets passing < 1e-3:        9
frequency subsets failing >= 1e-3:       0
96-panel high-frequency bridge ready:    true
project FDTD comparison ready:           false
real 3D validation ready:                false
GPU/HPC ready:                           false
field transfer ready:                    false
field FWI ready:                         false
```

All nine frequency subsets pass below the `1e-3` target:

| Subset | Relative L2 |
| --- | ---: |
| full 25-bin band | 0.0003153081842055151 |
| low 0.25-0.94 GHz | 0.00017912306537916088 |
| mid 1.05-1.97 GHz | 0.00042501637547310596 |
| high 2.08-3.00 GHz | 0.0007600368161379071 |
| even frequency bins | 0.0003273752438314411 |
| odd frequency bins | 0.00030243911655651124 |
| every third bin | 0.00028921762652489173 |
| center band | 0.00042889919631998224 |
| edge low/high band | 0.00011596928440368181 |

## Interpretation

The 96-panel solve is a useful intermediate point. It closes the 64-panel
high-frequency failure while taking about `57%` of the 128-panel wall time in
this run. Its high-band error is still about `1.78x` larger than the 128-panel
endpoint, so 128 panels remain the stricter accuracy endpoint, but 96 panels
are now a credible lower-cost high-frequency candidate.

## Decision

Use 96 panels as the current lower-cost high-frequency candidate, pending
validator and sensitivity hardening. Keep project FDTD comparison, 3D
validation, field transfer, field FWI, and GPU/HPC claims blocked from this
analytic-cylinder BEM result.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel96_frequency_subset_bridge_audit.py

3 passed
```

Figure check:

```text
2446x867, dynamic range=255
```

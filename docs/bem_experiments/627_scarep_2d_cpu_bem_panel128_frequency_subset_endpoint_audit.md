# BEM Experiment 627: 128-Panel Frequency-Subset Endpoint Audit

Date: 2026-06-30

## Purpose

Test whether the 128-panel two-dimensional CPU BEM endpoint closes the
high-frequency-only accuracy gap found at 64 panels in run `624`.

Run `624` showed that 64 panels pass the full, low, and mid frequency bands but
fail the high-frequency-only 2.08-3.00 GHz band under the `1e-3` relative-error
target. This run performs one fresh 128-panel CPU BEM solve on the same
analytic-cylinder validation problem, saves the response arrays, and reruns the
same nine frequency-subset checks.

## Output

```text
outputs/bem_experiments/627_scarep_2d_cpu_bem_panel128_frequency_subset_endpoint_audit
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel128_frequency_subset_endpoint_audit_rows.csv
data/scarep_2d_cpu_bem_panel128_frequency_subset_endpoint_audit_summary.json
data/scarep_2d_cpu_bem_panel128_frequency_subset_endpoint_audit_arrays.npz
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel128_frequency_subset_endpoint_audit.png
scripts/
```

The saved array package contains:

```text
frequencies_hz
source_points
receiver_points
time_s
bem_frequency_response
analytic_frequency_response
bem_time_bscan
analytic_time_bscan
```

## Result

```text
panels:                                      128
scan positions:                              11
frequencies:                                 25
wall seconds:                                79.71293680998497
complex relative L2:                         0.00017926490798156493
time-B-scan relative L2:                     0.00013202484159666165
frequency subsets:                           9
frequency subsets below 1e-3:                9
frequency subsets above/equal 1e-3:          0
full-band relative L2:                       0.00017926490798156504
low-band relative L2:                        0.00010235059260755993
mid-band relative L2:                        0.0002416728121920427
high-band relative L2:                       0.0004276569548253307
64-panel high-band relative L2:              0.001736291511432671
high-band improvement factor versus 64:      4.060009995960033
128 panels close 64-panel high-band gap:     true
project FDTD comparison ready:               false
real 3D validation ready:                    false
GPU/HPC ready:                               false
field transfer ready:                        false
field FWI ready:                             false
```

All nine frequency subsets pass under the `1e-3` target:

| Subset | Frequency range | Relative L2 |
| --- | ---: | ---: |
| full band | 0.25-3.00 GHz | 0.00017926490798156504 |
| low band | 0.25-0.94 GHz | 0.00010235059260755993 |
| mid band | 1.05-1.97 GHz | 0.0002416728121920427 |
| high band | 2.08-3.00 GHz | 0.0004276569548253307 |
| even bins | 0.25-3.00 GHz | 0.0001862069950255101 |
| odd bins | 0.36-2.89 GHz | 0.00017185787254369328 |
| every third bin | 0.25-3.00 GHz | 0.00016462230194876188 |
| center band | 1.05-2.20 GHz | 0.00024388270358840236 |
| edge low/high | 0.25-3.00 GHz | 0.00006587468001738573 |

## Interpretation

The high-frequency-only failure at 64 panels is a panel-resolution endpoint
issue in this two-dimensional analytic-cylinder BEM setup. Moving to 128 panels
reduces the high-band relative error from `0.001736291511432671` to
`0.0004276569548253307`, a `4.06x` improvement, and brings all nine frequency
subsets below the `1e-3` target.

This sharpens the BEM operating policy:

```text
Use 64 panels for cheaper broad-band, low-band, mid-band, receiver-line, and
screening sweeps.
Use 128 panels as the high-frequency endpoint when a claim depends on the
2.08-3.00 GHz band or on tighter accuracy.
```

The result remains limited to the two-dimensional scarep analytic-cylinder BEM
validation problem. It is not a project FDTD comparison, not a field-data result,
not a three-dimensional Maxwell validation, and not a GPU/HPC readiness result.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel128_frequency_subset_endpoint_audit.py

3 passed
```

Figure check:

```text
2428x867, dynamic range=255
```

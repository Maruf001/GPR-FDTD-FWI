# BEM Experiment 624: scarep 2D CPU BEM 64-Panel Frequency-Subset Stability Audit

Date: 2026-06-30

## Purpose

Test whether the validated 64-panel scarep CPU BEM default remains below the
`1e-3` analytic-cylinder error target across frequency-band subsets.

Runs `621-623` showed that 64 panels are stable under receiver/scan-line
cropping and thinning. This run tests the other axis: low, mid, high, and
decimated frequency subsets using the saved run `621` arrays.

This run does not rerun BEM solves, compare against project FDTD outputs, run
3D validation, launch GPU/HPC work, transfer to field work, run field FWI, or
train neural networks.

## Output

```text
outputs/bem_experiments/624_scarep_2d_cpu_bem_panel64_frequency_subset_stability_audit
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel64_frequency_subset_stability_audit_rows.csv
data/scarep_2d_cpu_bem_panel64_frequency_subset_stability_audit_summary.json
figures/scarep_2d_cpu_bem_panel64_frequency_subset_stability_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
target relative L2:                  0.001
frequency subsets:                   9
full-band relative L2:               0.0007053747139208217
low-band relative L2:                0.00039681403122296773
mid-band relative L2:                0.0009503011515443673
high-band relative L2:               0.001736291511432671
maximum subset relative L2:          0.001736291511432671
passing subsets:                     8
failing subsets:                     1
all subsets below 1e-3:              false
high band exceeds 1e-3:              true
high-frequency-only needs endpoint:  true
compared to project FDTD:            false
real 3D validation ready:            false
GPU/HPC ready:                       false
field transfer ready:                false
field FWI ready:                     false
audit ready:                         true
```

Frequency-subset outcomes:

| Subset | Frequency count | Frequency range | Relative L2 | Pass |
| --- | ---: | --- | ---: | --- |
| full_25 | 25 | 0.25-3.00 GHz | 0.0007053747139208217 | yes |
| low_0p25_0p94ghz | 7 | 0.25-0.94 GHz | 0.00039681403122296773 | yes |
| mid_1p05_1p97ghz | 9 | 1.05-1.97 GHz | 0.0009503011515443673 | yes |
| high_2p08_3p00ghz | 9 | 2.08-3.00 GHz | 0.001736291511432671 | no |
| even_bins_13 | 13 | 0.25-3.00 GHz | 0.0007311714318995723 | yes |
| odd_bins_12 | 12 | 0.36-2.89 GHz | 0.0006779127897557529 | yes |
| every_third_9 | 9 | 0.25-3.00 GHz | 0.0006459244280464918 | yes |
| center_11 | 11 | 1.05-2.20 GHz | 0.0009589893438666324 | yes |
| edge_low_high_10 | 10 | 0.25-3.00 GHz | 0.00026110236870969026 | yes |

## Interpretation

The 64-panel default is adequate for broad-band, low-band, mid-band, and
decimated-frequency diagnostics in this analytic-cylinder setup. It is not
adequate for a claim that depends only on the 2-3 GHz high-frequency band under
the same `1e-3` threshold.

## Decision

Use 64 panels for broad/low/mid-band receiver-line sweeps. Use the 128-panel
endpoint, or a dedicated high-frequency confirmation, when the claim depends
on 2-3 GHz behavior alone.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel64_frequency_subset_stability_audit.py

3 passed
```

Figure validation:

```text
2356x905, dynamic range=255
```

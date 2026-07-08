# BEM Experiment 866: Panel-116 Frequency-Bin Amplitude/Phase Decomposition

Date: 2026-07-01

## Purpose

Decompose the remaining above-target high-band frequency-bin errors from the
116-panel analytic BEM endpoint into amplitude, phase, mixed, and scalar-gain
components.

This run re-solves the controlling 13-scan, 116-panel analytic case for the
25- and 49-frequency grids. It does not run project FDTD, field processing,
3D/HPC work, or GPU kernels.

## Output

```text
outputs/bem_experiments/866_scarep_2d_cpu_bem_panel116_frequency_bin_amplitude_phase_decomposition_audit
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel116_frequency_bin_amplitude_phase_decomposition_audit_grid_rows.csv
data/scarep_2d_cpu_bem_panel116_frequency_bin_amplitude_phase_decomposition_audit_frequency_decomposition_rows.csv
data/scarep_2d_cpu_bem_panel116_frequency_bin_amplitude_phase_decomposition_audit_summary.json
figures/scarep_2d_cpu_bem_panel116_frequency_bin_amplitude_phase_decomposition_audit.png
```

## Result

```text
source anatomy ready:                       true
source policy ready:                        true
panel count:                                116
frequency grids:                            2
frequency decomposition rows:               74
high-band decomposition rows:               27
above-target high-band rows:                5
above-target amplitude-dominant rows:       0
above-target phase-dominant rows:           1
above-target mixed rows:                    4
dominant above-target mode:                 mixed
25-frequency high-band relative L2:         0.000951829108345244
49-frequency high-band relative L2:         0.0007643703508458815
worst bin frequency:                        2.3125 GHz
worst bin complex relative L2:              0.0020304660813910734
worst bin amplitude relative L2:            0.0012972280086559237
worst bin phase-only relative L2:           0.0015623055247504384
worst bin phase RMSE:                       0.0015623057200655063 rad
worst bin scalar-gain-corrected L2:         0.0019054837810734088
worst bin scalar-gain reduction fraction:   0.061553503140539645
scalar-gain correction promoted:            false
project FDTD comparison ready:              false
field transfer ready:                       false
3D/HPC ready:                               false
```

## Interpretation

The remaining per-frequency exceedance is not an amplitude-only calibration
problem. Four of the five above-target high-band bins are mixed amplitude/phase
errors, and one is phase-dominant. The worst bin at `2.3125 GHz` remains above
target after a best scalar complex gain correction, with only about 6.2%
relative reduction.

This points to a frequency-local shape or operator error rather than a simple
global amplitude or phase offset.

## Decision

Keep the 116-panel result as an aggregate analytic endpoint with
per-frequency diagnostics. Do not promote scalar-gain correction, hard
per-frequency acceptance, project-FDTD comparison, field transfer, or 3D/HPC
claims from this audit.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_frequency_bin_amplitude_phase_decomposition_audit.py
3 passed
```

Figure check:

```text
2969x870, dynamic range=255
```

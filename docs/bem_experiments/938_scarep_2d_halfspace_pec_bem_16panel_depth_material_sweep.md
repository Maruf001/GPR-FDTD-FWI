# BEM Experiment 938: Half-Space PEC 16-Panel Depth and Material Sweep

Date: 2026-07-02

## Purpose

Extend the guarded 16-panel BEM depth-sensitivity block from runs `935-937`
to a small depth/material grid.

This run evaluates three PEC rebar center depths and three lower-half-space
relative-permittivity values:

```text
depths:     0.25, 0.35, 0.45 m
lower epsr: 4, 6, 8
```

The baseline case is `0.35` m depth with lower-half-space relative permittivity
`6`. This is a CPU-only BEM sensitivity run. It does not run FDTD, use field
data, match project-core FDTD, transfer to field evidence, or start 3D/HPC
work.

## Output

```text
outputs/bem_experiments/938_scarep_2d_halfspace_pec_bem_16panel_depth_material_sweep
```

## Result

```text
cases:                                      9
depth values:                              0.25;0.35;0.45 m
lower-half-space relative permittivity:    4;6;8
baseline depth:                            0.35 m
baseline relative permittivity:            6
preliminary BEM panels:                    16
scan positions:                            9
frequency samples:                         41
time samples:                              2048
total BEM solve wall seconds:              102.17866309802048
peak span across depth at epsr 6:          0.018574056369368822 dB
peak span across epsr at 0.35 m depth:     0.08605468696404216 dB
time span across depth at epsr 6:          0.0 ns
time span across epsr at 0.35 m depth:     0.0 ns
max relative L2 across depth at epsr 6:    0.039940245470760076
max relative L2 across epsr at 0.35 m:     0.05706521432942532
max relative L2 across full grid:          0.0649192423436475
project-core FDTD matched:                 false
field transfer ready:                      false
3D validation ready:                       false
gpu priority:                              none
```

Case rows:

| Depth (m) | Lower epsr | Peak abs | Peak dB vs baseline | Relative L2 vs baseline |
| ---: | ---: | ---: | ---: | ---: |
| 0.25 | 4 | 1150.195751599022 | -0.030477749847757606 | 0.0649192423436475 |
| 0.35 | 4 | 1147.5554482582143 | -0.050439348409308124 | 0.05706521432942532 |
| 0.45 | 4 | 1147.443799502074 | -0.051284463087035076 | 0.05268596697898034 |
| 0.25 | 6 | 1156.6685927193373 | 0.0182659322877885 | 0.039940245470760076 |
| 0.35 | 6 | 1154.2387402189202 | 0.0 | 0.0 |
| 0.45 | 6 | 1154.1977953694586 | -0.00030812408158032074 | 0.024061575691943917 |
| 0.25 | 8 | 1158.6377780559733 | 0.0330407636889153 | 0.04723724957594182 |
| 0.35 | 8 | 1158.9812594912412 | 0.03561533855473403 | 0.04156085009534679 |
| 0.45 | 8 | 1158.977734125343 | 0.035588917950046206 | 0.03877058620829347 |

## Interpretation

In this simplified half-space PEC setup, peak amplitude remains a weak
discriminator. Across the three tested depths at lower-half-space relative
permittivity `6`, the peak span is only about `0.019` dB. Across relative
permittivity values `4-8` at the center depth, the peak span is still small,
about `0.086` dB.

Waveform/scan shape is more useful than peak amplitude. The maximum relative
L2 difference across depth at relative permittivity `6` is about `4.0%`, while
the maximum relative L2 difference across relative permittivity at the center
depth is about `5.7%`. The full grid reaches about `6.5%` relative L2 from the
baseline.

## Decision

Use this run as a preliminary BEM-only depth/material sensitivity result. For
follow-on BEM screening, use waveform-shape metrics before peak-amplitude
metrics. Keep project-core FDTD matching, field transfer, GPU escalation, and
3D validation blocked until matched FDTD or measured data are available.

## Validation

Focused tests:

```text
tests/test_scarep_2d_halfspace_pec_bem_16panel_depth_material_sweep.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_depth_sweep.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_depth_sweep_validator.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_depth_sweep_validation_sensitivity.py
13 passed
```

Python compile check:

```text
run_scarep_2d_halfspace_pec_bem_16panel_depth_material_sweep.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_depth_material_sweep.py
pass
```

Figure check:

```text
2815x1511, dynamic range=255
```

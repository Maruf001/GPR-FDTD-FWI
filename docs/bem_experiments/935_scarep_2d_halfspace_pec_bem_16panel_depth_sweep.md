# BEM Experiment 935: Half-Space PEC 16-Panel Depth Sweep

Date: 2026-07-01

## Purpose

Use the 16-panel preliminary policy from runs `932-934` for a small BEM-only
depth sweep in the air/concrete half-space.

This run evaluates three PEC rebar center depths with the same half-space
material, scan line, source spectrum, and 16-panel BEM setting:

```text
0.25 m
0.35 m
0.45 m
```

This is a CPU-only BEM sensitivity run. It does not run FDTD, use field data,
match project-core FDTD, transfer to field evidence, or start 3D/HPC work.

## Output

```text
outputs/bem_experiments/935_scarep_2d_halfspace_pec_bem_16panel_depth_sweep
```

## Result

```text
depth cases:                            3
depth values:                           0.25;0.35;0.45 m
preliminary BEM panels:                 16
scan positions:                         9
frequency samples:                      41
time samples:                           2048
total BEM solve wall seconds:           33.86896941997111
shallow peak absolute field:            1156.6685927193373
deep peak absolute field:               1154.1977953694586
deep peak change vs shallow:            -0.018574056369367674 dB
peak monotone nonincreasing with depth: true
max relative L2 vs 0.35 m depth:        0.039940245470760076
project-core FDTD matched:              false
field transfer ready:                   false
3D validation ready:                    false
gpu priority:                           none
```

Depth rows:

| Center z (m) | Cover below interface (m) | Peak abs | L2 norm | Relative L2 vs 0.35 m | Peak dB vs 0.25 m |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0.25 | 0.15 | 1156.6685927193373 | 27732.133203555502 | 0.039940245470760076 | 0.0 |
| 0.35 | 0.25 | 1154.2387402189202 | 27724.86415868418 | 0.0 | -0.018265932287788007 |
| 0.45 | 0.35 | 1154.1977953694586 | 27724.65295664775 | 0.024061575691943917 | -0.018574056369367674 |

## Interpretation

For this 16-panel half-space BEM setup, peak amplitude alone is a weak depth
indicator across the tested depth range. The peak drops by only about `0.019`
dB from the shallow case to the deep case.

The waveform/scan shape changes more than the peak amplitude: the largest
relative L2 difference from the 0.35 m baseline is about `4.0%`. This suggests
that preliminary depth screening should use waveform-shape metrics, not only
peak amplitude.

## Decision

Use this as a preliminary BEM depth-sensitivity result. Keep project-core FDTD,
field transfer, and 3D validation blocked until matched FDTD or measured data
are available.

## Validation

Focused tests:

```text
tests/test_scarep_2d_halfspace_pec_bem_16panel_depth_sweep.py
3 passed
```

Figure check:

```text
3112x845, dynamic range=255
```

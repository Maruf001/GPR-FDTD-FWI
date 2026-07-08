# BEM Experiment 936: Half-Space PEC 16-Panel Depth Sweep Validator

Date: 2026-07-02

## Purpose

Validate the run `935` 16-panel half-space PEC BEM depth sweep from saved
artifacts.

This run checks that the depth sweep keeps the intended BEM-only scope,
preserves the three-depth 16-panel setup, keeps peak amplitude as a weak depth
signal, preserves waveform/scan-shape depth sensitivity, and does not promote
project-core FDTD, field transfer, GPU work, or 3D validation.

This is a CPU-only validation run. It does not run FDTD, use field data, match
project-core FDTD, transfer to field evidence, or start 3D/HPC work.

## Output

```text
outputs/bem_experiments/936_scarep_2d_halfspace_pec_bem_16panel_depth_sweep_validator
```

## Result

```text
validation checks:                     6
passed checks:                         6
failed checks:                         0
depth cases:                           3
depth values:                          0.25;0.35;0.45 m
preliminary BEM panels:                16
deep peak change vs shallow:           -0.018574056369367674 dB
peak monotone nonincreasing with depth:true
max relative L2 vs 0.35 m depth:       0.039940245470760076
project-core FDTD matched:             false
field transfer ready:                  false
3D validation ready:                   false
gpu priority:                          none
validation ready:                      true
```

Validation checks:

| Check order | Validation check | Passed |
| ---: | --- | --- |
| 1 | sweep identity and readiness | true |
| 2 | sweep shape and panel policy | true |
| 3 | peak amplitude depth signal is weak | true |
| 4 | waveform shape depth signal present | true |
| 5 | scope and downstream blocked | true |
| 6 | figure and scripts valid | true |

## Interpretation

The run `935` depth sweep validates as a preliminary BEM-only sensitivity
result. In this setup, peak amplitude changes by less than `0.02` dB across
the tested depths, so peak amplitude alone is not a useful depth indicator.
The waveform/scan-shape metric changes by about `4.0%`, which is the more
useful signal for preliminary depth screening.

## Decision

Use runs `935-936` as the guarded preliminary 16-panel BEM depth-sensitivity
block. Continue BEM depth and material-contrast sweeps with waveform-shape
metrics, and keep 32-panel checks for selected final comparison checkpoints.
Project-core FDTD matching, field transfer, GPU escalation, and 3D validation
remain blocked.

## Validation

Focused tests:

```text
tests/test_scarep_2d_halfspace_pec_bem_16panel_depth_sweep.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_depth_sweep_validator.py
7 passed
```

Python compile check:

```text
run_scarep_2d_halfspace_pec_bem_16panel_depth_sweep.py
run_scarep_2d_halfspace_pec_bem_16panel_depth_sweep_validator.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_depth_sweep.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_depth_sweep_validator.py
pass
```

Figure check:

```text
2573x856, dynamic range=255
```

# BEM Experiment 939: Half-Space PEC 16-Panel Depth and Material Sweep Validator

Date: 2026-07-02

## Purpose

Validate the run `938` 16-panel half-space PEC BEM depth/material sweep from
saved artifacts.

This run checks that the saved sweep preserves the 3-by-3 depth/material grid,
the 16-panel preliminary policy, the baseline metrics, the depth-vs-material
sensitivity boundary, and the blocked downstream scope.

This is a CPU-only validation run. It does not run FDTD, use field data, match
project-core FDTD, transfer to field evidence, or start 3D/HPC work.

## Output

```text
outputs/bem_experiments/939_scarep_2d_halfspace_pec_bem_16panel_depth_material_sweep_validator
```

## Result

```text
validation checks:                         6
passed checks:                             6
failed checks:                             0
cases:                                     9
depth values:                              0.25;0.35;0.45 m
lower-half-space relative permittivity:    4;6;8
preliminary BEM panels:                    16
peak span across depth at epsr 6:          0.018574056369368822 dB
peak span across epsr at 0.35 m depth:     0.08605468696404216 dB
max relative L2 across depth at epsr 6:    0.039940245470760076
max relative L2 across epsr at 0.35 m:     0.05706521432942532
max relative L2 across full grid:          0.0649192423436475
project-core FDTD matched:                 false
field transfer ready:                      false
3D validation ready:                       false
gpu priority:                              none
validation ready:                          true
```

Validation checks:

| Check order | Validation check | Passed |
| ---: | --- | --- |
| 1 | sweep identity and readiness | true |
| 2 | grid shape and panel policy | true |
| 3 | baseline and metric consistency | true |
| 4 | depth material signal boundary | true |
| 5 | scope and downstream blocked | true |
| 6 | figure and scripts valid | true |

## Interpretation

The run `938` depth/material sweep validates as a preliminary BEM-only
sensitivity result. For this 3-by-3 grid, relative-permittivity variation at
the center depth produces a larger waveform/scan-shape change than depth
variation at relative permittivity `6`.

## Decision

Use runs `938-939` as the guarded preliminary 16-panel BEM depth/material
sensitivity block. Follow-on BEM screening should use waveform-shape metrics
before peak-amplitude metrics. Project-core FDTD matching, field transfer, GPU
escalation, and 3D validation remain blocked.

## Validation

Focused tests:

```text
tests/test_scarep_2d_halfspace_pec_bem_16panel_depth_material_sweep.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_depth_material_sweep_validator.py
7 passed
```

Python compile check:

```text
run_scarep_2d_halfspace_pec_bem_16panel_depth_material_sweep.py
run_scarep_2d_halfspace_pec_bem_16panel_depth_material_sweep_validator.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_depth_material_sweep.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_depth_material_sweep_validator.py
pass
```

Figure check:

```text
2681x859, dynamic range=255
```

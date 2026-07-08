# BEM Experiment 942: Half-Space PEC 16-Panel Source/Receiver Geometry Sweep Validator

Date: 2026-07-02

## Purpose

Validate the run `941` 16-panel half-space PEC BEM source/receiver geometry
sweep from saved artifacts.

This run checks that the saved sweep preserves the 3-by-3 Tx/Rx offset and
antenna-z grid, the 16-panel preliminary policy, the baseline metrics, the
geometry sensitivity boundary, and the blocked downstream scope.

This is a CPU-only validation run. It does not run FDTD, use field data, match
project-core FDTD, transfer to field evidence, or start 3D/HPC work.

## Output

```text
outputs/bem_experiments/942_scarep_2d_halfspace_pec_bem_16panel_source_receiver_geometry_sweep_validator
```

## Result

```text
validation checks:                         6
passed checks:                             6
failed checks:                             0
cases:                                     9
Tx/Rx offset values:                       0.04;0.06;0.08 m
antenna z values:                          -0.02;0;0.04 m
preliminary BEM panels:                    16
peak span across Tx/Rx offset at z=0:      2.6214537950832346 dB
peak span across antenna z at offset=0.06: 0.10842371175746399 dB
time span across Tx/Rx offset at z=0:      0.13190034196385092 ns
time span across antenna z at offset=0.06: 0.0 ns
max relative L2 across offset at z=0:      0.7099232724148534
max relative L2 across antenna z:          0.4171376953084501
max relative L2 across full grid:          0.9115427115447009
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
| 4 | geometry signal boundary | true |
| 5 | scope and downstream blocked | true |
| 6 | figure and scripts valid | true |

## Interpretation

The run `941` source/receiver geometry sweep validates as a preliminary
BEM-only sensitivity result. Tx/Rx spacing is the dominant tested geometry
effect, producing much larger peak-amplitude and waveform-shape changes than
antenna z-position in this small grid.

## Decision

Use runs `941-942` as the guarded preliminary 16-panel BEM acquisition-geometry
sensitivity block. Future matched BEM/FDTD comparisons should lock Tx/Rx
spacing and antenna z-position before interpreting residual disagreement as
depth or material error. Project-core FDTD matching, field transfer, GPU
escalation, and 3D validation remain blocked.

## Validation

Focused tests:

```text
tests/test_scarep_2d_halfspace_pec_bem_16panel_source_receiver_geometry_sweep.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_source_receiver_geometry_sweep_validator.py
7 passed
```

Python compile check:

```text
run_scarep_2d_halfspace_pec_bem_16panel_source_receiver_geometry_sweep.py
run_scarep_2d_halfspace_pec_bem_16panel_source_receiver_geometry_sweep_validator.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_source_receiver_geometry_sweep.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_source_receiver_geometry_sweep_validator.py
pass
```

Figure check:

```text
2681x859, dynamic range=255
```

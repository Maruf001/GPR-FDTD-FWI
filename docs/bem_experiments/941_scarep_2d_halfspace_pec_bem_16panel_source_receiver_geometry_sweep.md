# BEM Experiment 941: Half-Space PEC 16-Panel Source/Receiver Geometry Sweep

Date: 2026-07-02

## Purpose

Use the guarded 16-panel BEM setting to isolate acquisition-geometry
sensitivity at the baseline half-space PEC case.

This run keeps target depth and lower-half-space relative permittivity fixed:

```text
target depth: 0.35 m
lower epsr:   6
```

It varies Tx/Rx spacing and antenna z-position:

```text
Tx/Rx offsets: 0.04, 0.06, 0.08 m
antenna z:     -0.02, 0.00, 0.04 m
```

The baseline case is `0.06` m Tx/Rx spacing and antenna z-position `0.00` m.
This is a CPU-only BEM sensitivity run. It does not run FDTD, use field data,
match project-core FDTD, transfer to field evidence, or start 3D/HPC work.

## Output

```text
outputs/bem_experiments/941_scarep_2d_halfspace_pec_bem_16panel_source_receiver_geometry_sweep
```

## Result

```text
cases:                                      9
Tx/Rx offset values:                       0.04;0.06;0.08 m
antenna z values:                          -0.02;0;0.04 m
baseline Tx/Rx offset:                     0.06 m
baseline antenna z:                        0.0 m
target depth:                              0.35 m
lower-half-space relative permittivity:    6
preliminary BEM panels:                    16
scan positions:                            9
frequency samples:                         41
time samples:                              2048
total BEM solve wall seconds:              103.06960728461854
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
```

Case rows:

| Tx/Rx offset (m) | Antenna z (m) | Peak abs | Peak dB vs baseline | Relative L2 vs baseline |
| ---: | ---: | ---: | ---: | ---: |
| 0.04 | -0.02 | 1374.904050721686 | 1.5195348969118296 | 0.7475448709847718 |
| 0.06 | -0.02 | 1152.6511967457723 | -0.011954822255911426 | 0.2403154412097976 |
| 0.08 | -0.02 | 1011.0094562102903 | -1.1508085792748375 | 0.6338702841478464 |
| 0.04 | 0.00 | 1374.9506415743176 | 1.5198292273761083 | 0.7099232724148534 |
| 0.06 | 0.00 | 1154.2387402189202 | 0.0 | 0.0 |
| 0.08 | 0.00 | 1016.7505552530179 | -1.1016245677071266 | 0.5847617203178206 |
| 0.04 | 0.04 | 1368.2181283780774 | 1.4771938746670352 | 0.9115427115447009 |
| 0.06 | 0.04 | 1139.920229885785 | -0.10842371175746399 | 0.4171376953084501 |
| 0.08 | 0.04 | 987.8330790981927 | -1.3522416310018062 | 0.6028654953291047 |

## Interpretation

Acquisition geometry is much more influential than the small depth/material
variations tested in runs `935-940`. At antenna z-position `0.00` m, changing
Tx/Rx spacing from `0.04` m to `0.08` m spans about `2.62` dB in peak
amplitude and reaches about `0.71` relative L2 from the baseline. Changing
antenna z-position at the baseline spacing reaches about `0.42` relative L2.

This means that future BEM/FDTD matching should prioritize source/receiver
geometry before treating residual disagreement as target-depth or material
error.

## Decision

Use this run as a preliminary BEM-only acquisition-geometry sensitivity result.
Future matched BEM/FDTD comparisons should lock Tx/Rx spacing and antenna
z-position carefully. Project-core FDTD matching, field transfer, GPU
escalation, and 3D validation remain blocked until matched FDTD or measured
data are available.

## Validation

Focused tests:

```text
tests/test_scarep_2d_halfspace_pec_bem_16panel_source_receiver_geometry_sweep.py
3 passed
```

Python compile check:

```text
run_scarep_2d_halfspace_pec_bem_16panel_source_receiver_geometry_sweep.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_source_receiver_geometry_sweep.py
pass
```

Figure check:

```text
2817x1511, dynamic range=255
```

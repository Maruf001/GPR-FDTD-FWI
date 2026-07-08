# BEM Experiment 943: Half-Space PEC 16-Panel Source/Receiver Geometry Sweep Validation Sensitivity

Date: 2026-07-02

## Purpose

Stress-test the run `942` 16-panel half-space PEC BEM source/receiver geometry
sweep validator.

This run checks that the validator accepts only the exact saved
source/receiver geometry state and rejects damaged grid rows, offset values,
antenna-z values, baseline settings, panel policy, scan/frequency/time counts,
baseline metrics, geometry sensitivity metrics, downstream promotion, figure
damage, and script-snapshot damage.

## Output

```text
outputs/bem_experiments/943_scarep_2d_halfspace_pec_bem_16panel_source_receiver_geometry_sweep_validation_sensitivity
```

## Result

```text
source validator ready:                true
scenarios:                             25
expected pass scenarios:               1
expected fail scenarios:               24
observed pass scenarios:               1
observed fail scenarios:               24
unexpected outcomes:                   0
damaged scenarios:                     24
damaged scenarios rejected:            24
cases:                                 9
Tx/Rx offset values:                   0.04;0.06;0.08 m
antenna z values:                      -0.02;0;0.04 m
preliminary BEM panels:                16
peak span across offset at z=0:        2.6214537950832346 dB
peak span across antenna z:            0.10842371175746399 dB
time span across offset at z=0:        0.13190034196385092 ns
time span across antenna z:            0.0 ns
max relative L2 across offset at z=0:  0.7099232724148534
max relative L2 across antenna z:      0.4171376953084501
max relative L2 across full grid:      0.9115427115447009
project-core FDTD matched:             false
field transfer ready:                  false
3D validation ready:                   false
gpu priority:                          none
```

Rejected damaged states include:

```text
sweep-not-ready state
row removal
offset-value damage
antenna-z value damage
baseline-offset damage
baseline-antenna-z damage
panel-policy damage
scan-count damage
frequency-count damage
time-sample damage
baseline relative-L2 damage
peak-offset span damage
peak-antenna-z span damage
time-offset signal damage
time-antenna-z signal damage
relative-L2 offset-signal damage
relative-L2 antenna-z signal damage
full-grid relative-L2 damage
project-core FDTD promotion
field-transfer promotion
3D promotion
GPU-priority promotion
figure damage
script-snapshot damage
```

## Interpretation

The run `942` validator is fail-closed for the preliminary
source/receiver-geometry sensitivity result. It accepts the exact saved
3-by-3 BEM-only geometry grid and rejects damaged metrics or premature
downstream promotion.

## Decision

Use runs `941-943` as the guarded preliminary 16-panel BEM
acquisition-geometry sensitivity block. Source/receiver geometry should be
locked before interpreting BEM/FDTD residuals as depth or material error. This
does not support project-core FDTD matching, field transfer, GPU escalation, or
3D validation.

## Validation

Focused tests:

```text
tests/test_scarep_2d_halfspace_pec_bem_16panel_source_receiver_geometry_sweep.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_source_receiver_geometry_sweep_validator.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_source_receiver_geometry_sweep_validation_sensitivity.py
10 passed
```

Python compile check:

```text
run_scarep_2d_halfspace_pec_bem_16panel_source_receiver_geometry_sweep.py
run_scarep_2d_halfspace_pec_bem_16panel_source_receiver_geometry_sweep_validator.py
run_scarep_2d_halfspace_pec_bem_16panel_source_receiver_geometry_sweep_validation_sensitivity.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_source_receiver_geometry_sweep.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_source_receiver_geometry_sweep_validator.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_source_receiver_geometry_sweep_validation_sensitivity.py
pass
```

Figure check:

```text
3617x879, dynamic range=255
```

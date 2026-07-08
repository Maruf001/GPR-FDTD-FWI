# BEM Experiment 940: Half-Space PEC 16-Panel Depth and Material Sweep Validation Sensitivity

Date: 2026-07-02

## Purpose

Stress-test the run `939` 16-panel half-space PEC BEM depth/material sweep
validator.

This run checks that the validator accepts only the exact saved depth/material
sweep state and rejects damaged grid rows, depth values, material values,
panel policy, scan/frequency/time counts, baseline metrics, depth/material
sensitivity metrics, downstream promotion, figure damage, and script-snapshot
damage.

## Output

```text
outputs/bem_experiments/940_scarep_2d_halfspace_pec_bem_16panel_depth_material_sweep_validation_sensitivity
```

## Result

```text
source validator ready:                true
scenarios:                             21
expected pass scenarios:               1
expected fail scenarios:               20
observed pass scenarios:               1
observed fail scenarios:               20
unexpected outcomes:                   0
damaged scenarios:                     20
damaged scenarios rejected:            20
cases:                                 9
depth values:                          0.25;0.35;0.45 m
lower epsr values:                     4;6;8
preliminary BEM panels:                16
peak span across depth at epsr 6:      0.018574056369368822 dB
peak span across epsr at 0.35 m:       0.08605468696404216 dB
max relative L2 across depth at epsr 6:0.039940245470760076
max relative L2 across epsr at 0.35 m: 0.05706521432942532
max relative L2 across full grid:      0.0649192423436475
project-core FDTD matched:             false
field transfer ready:                  false
3D validation ready:                   false
gpu priority:                          none
```

Rejected damaged states include:

```text
sweep-not-ready state
row removal
depth-value damage
relative-permittivity value damage
panel-policy damage
scan-count damage
frequency-count damage
time-sample damage
baseline relative-L2 damage
peak-depth span damage
peak-material span damage
relative-L2 depth-signal damage
relative-L2 material-signal damage
full-grid relative-L2 damage
project-core FDTD promotion
field-transfer promotion
3D promotion
GPU-priority promotion
figure damage
script-snapshot damage
```

## Interpretation

The run `939` validator is fail-closed for the preliminary depth/material
sensitivity result. It accepts the exact saved 3-by-3 BEM-only grid and rejects
damaged metrics or premature downstream promotion.

## Decision

Use runs `938-940` as the guarded preliminary 16-panel BEM depth/material
sensitivity block. The current result supports waveform-shape-based screening
for follow-on BEM studies. It does not support project-core FDTD matching,
field transfer, GPU escalation, or 3D validation.

## Validation

Focused tests:

```text
tests/test_scarep_2d_halfspace_pec_bem_16panel_depth_material_sweep.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_depth_material_sweep_validator.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_depth_material_sweep_validation_sensitivity.py
10 passed
```

Python compile check:

```text
run_scarep_2d_halfspace_pec_bem_16panel_depth_material_sweep.py
run_scarep_2d_halfspace_pec_bem_16panel_depth_material_sweep_validator.py
run_scarep_2d_halfspace_pec_bem_16panel_depth_material_sweep_validation_sensitivity.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_depth_material_sweep.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_depth_material_sweep_validator.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_depth_material_sweep_validation_sensitivity.py
pass
```

Figure check:

```text
3365x883, dynamic range=255
```

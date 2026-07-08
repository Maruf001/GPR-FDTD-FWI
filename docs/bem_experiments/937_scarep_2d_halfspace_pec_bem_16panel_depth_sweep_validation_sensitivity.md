# BEM Experiment 937: Half-Space PEC 16-Panel Depth Sweep Validation Sensitivity

Date: 2026-07-02

## Purpose

Stress-test the run `936` 16-panel half-space PEC BEM depth-sweep validator.

This run checks that the validator accepts only the exact saved depth-sweep
state and rejects damaged depth rows, depth values, panel policy, scan/frequency
counts, time samples, peak-depth metrics, waveform-shape metrics, figure
metadata, script snapshots, and premature project-core FDTD, field-transfer,
GPU, or 3D promotion.

## Output

```text
outputs/bem_experiments/937_scarep_2d_halfspace_pec_bem_16panel_depth_sweep_validation_sensitivity
```

## Result

```text
source validator ready:                true
scenarios:                             19
expected pass scenarios:               1
expected fail scenarios:               18
observed pass scenarios:               1
observed fail scenarios:               18
unexpected outcomes:                   0
damaged scenarios:                     18
damaged scenarios rejected:            18
depth cases:                           3
depth values:                          0.25;0.35;0.45 m
preliminary BEM panels:                16
deep peak change vs shallow:           -0.018574056369367674 dB
max relative L2 vs 0.35 m depth:       0.039940245470760076
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
panel-policy damage
scan-count damage
frequency-count damage
time-sample damage
peak-monotonicity damage
peak-dB damage
absent waveform-shape signal
overstated waveform-shape signal
baseline relative-L2 damage
project-core FDTD promotion
field-transfer promotion
3D promotion
GPU-priority promotion
figure damage
script-snapshot damage
```

## Interpretation

The run `936` validator is fail-closed for the preliminary depth-sensitivity
claim. It accepts the exact saved BEM-only depth sweep and rejects damaged
metrics or premature downstream promotion.

## Decision

Use runs `935-937` as the guarded preliminary 16-panel BEM depth-sensitivity
block. The current result supports waveform-shape-based preliminary depth
screening in this simplified half-space PEC setup. It does not support
project-core FDTD matching, field transfer, GPU escalation, or 3D validation.

## Validation

Focused tests:

```text
tests/test_scarep_2d_halfspace_pec_bem_16panel_depth_sweep.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_depth_sweep_validator.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_depth_sweep_validation_sensitivity.py
10 passed
```

Python compile check:

```text
run_scarep_2d_halfspace_pec_bem_16panel_depth_sweep.py
run_scarep_2d_halfspace_pec_bem_16panel_depth_sweep_validator.py
run_scarep_2d_halfspace_pec_bem_16panel_depth_sweep_validation_sensitivity.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_depth_sweep.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_depth_sweep_validator.py
tests/test_scarep_2d_halfspace_pec_bem_16panel_depth_sweep_validation_sensitivity.py
pass
```

Figure check:

```text
3293x884, dynamic range=255
```

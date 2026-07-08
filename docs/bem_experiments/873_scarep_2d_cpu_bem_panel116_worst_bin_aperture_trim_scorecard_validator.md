# BEM Experiment 873: Panel-116 Worst-Bin Aperture Trim Scorecard Validator

Date: 2026-07-01

## Purpose

Validate the saved run `872` aperture-trim scorecard from artifacts.

This validator does not rerun BEM, FDTD, field processing, 3D/HPC work, or GPU
kernels.

## Output

```text
outputs/bem_experiments/873_scarep_2d_cpu_bem_panel116_worst_bin_aperture_trim_scorecard_validator
```

## Result

```text
validation checks:                      6
passed checks:                          6
failed checks:                          0
score rows:                             6
frequency:                              2.3125 GHz
target relative L2:                     0.001
full aperture relative L2:              0.002030466081391074
strict-center relative L2:              0.001938978012629881
edge-quarters relative L2:              0.0021015204146441102
best subset:                            strict_center_non_edge
best subset relative L2:                0.001938978012629881
any aperture subset passes target:      false
edge trim repairs worst bin:            false
worst-bin mismatch survives interior:   true
project FDTD comparison ready:          false
field transfer ready:                   false
3D validation ready:                    false
```

## Interpretation

The aperture-trim scorecard validates as a no-repair result. Removing edge
receivers reduces the error slightly, but not enough to meet the target.

## Decision

Use run `872` as the current aperture-trim diagnostic for the worst remaining
116-panel high-band frequency bin.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_aperture_trim_scorecard_validator.py
3 passed
```

Figure check:

```text
2429x864, dynamic range=255
```

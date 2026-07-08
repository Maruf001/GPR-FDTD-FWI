# BEM Experiment 022: Distance-Aware Direct-Wave Calibration Probe

Date: 2026-06-24

## Purpose

Use the long-offset direct-wave data from run `021` to test whether a
distance-aware source scale can repair the project-core FDTD-to-Green-function
mismatch.

This run does not launch a new FDTD solve. It reads the run `021` arrays,
fits per-offset complex source scales, and compares:

- a measured per-offset calibration table;
- leave-one-offset-out interpolation of that table.

## Output

```text
outputs/bem_experiments/022_project_core_distance_aware_direct_wave_calibration_probe
```

Key artifacts:

```text
data/distance_aware_direct_wave_calibration_summary.json
data/distance_aware_direct_wave_offset_metrics.csv
data/distance_aware_direct_wave_frequency_metrics.csv
data/distance_aware_direct_wave_calibration_arrays.npz
figures/distance_aware_direct_wave_offset_probe.png
figures/distance_aware_direct_wave_scale_surface.png
docs/DISTANCE_AWARE_DIRECT_WAVE_CALIBRATION_PROBE.md
```

## Result

```text
source run:                         outputs/bem_experiments/021_project_core_long_offset_direct_wave_green_transfer_audit
offset count:                       9
frequency count:                    17
measured table symmetric L2:        0.30880226614764117
leave-one-offset symmetric L2:      0.9672799928720243
max measured-table offset L2:       0.4026620237905695
max leave-one-offset offset L2:     1.7224404811442773
distance-aware interpolation ready: false
```

Offset diagnostics:

| Offset (m) | Measured table symmetric L2 | Leave-one-offset symmetric L2 |
| ---: | ---: | ---: |
| 0.02 | 0.23002377570364504 | 1.444538219822308 |
| 0.04 | 0.2975234272113172 | 0.3204769160704787 |
| 0.06 | 0.320118596727833 | 0.34131405068722337 |
| 0.08 | 0.31257799970565214 | 0.33621797789320135 |
| 0.10 | 0.3012543124007648 | 0.7268636249360102 |
| 0.14 | 0.3063219828139095 | 0.7674431986652575 |
| 0.18 | 0.35272581188672847 | 0.7026045803265706 |
| 0.22 | 0.40181837702309436 | 0.7121226435991872 |
| 0.26 | 0.4026620237905695 | 1.7224404811442773 |

## Interpretation

A measured per-offset source scale table improves direct-wave agreement, but
sparse interpolation is not reliable enough. The source scale has
distance-dependent amplitude and phase structure that sparse linear
interpolation cannot safely capture.

This rules out a simple quick fix for applying run `020` or run `021` direct
calibration to the run `019` scattered target response.

## Decision

Do not use sparse interpolated distance-aware calibration for target
scattering yet. The next repair should either:

1. sample a denser direct-wave calibration grid; or
2. change the project source formulation so it better matches the 2D
   line-source Green reference.

## Validation

```text
python -m py_compile run_project_core_distance_aware_direct_wave_calibration_probe.py
conda run -n gpr-fdtd-fwi python run_project_core_distance_aware_direct_wave_calibration_probe.py
```

Figure check:

```text
2 PNG figures, nonblank dynamic range, dimensions from 1187x731 to 1808x740
```

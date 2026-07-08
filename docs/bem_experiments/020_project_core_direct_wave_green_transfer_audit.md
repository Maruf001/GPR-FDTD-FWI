# BEM Experiment 020: Project-Core Direct-Wave Green Transfer Audit

Date: 2026-06-24

## Purpose

Remove the target entirely and test the most basic calibration assumption:

```text
Can one frequency-dependent source factor map the homogeneous 2D Green
function to the project-core FDTD direct wave across multiple Tx/Rx distances?
```

This directly explains whether direct-wave calibration at one Tx/Rx distance
can be expected to normalize scattered paths with different effective path
lengths.

## Output

```text
outputs/bem_experiments/020_project_core_direct_wave_green_transfer_audit
```

Key artifacts:

```text
data/project_core_direct_wave_green_transfer_summary.json
data/project_core_direct_wave_frequency_metrics.csv
data/project_core_direct_wave_offset_metrics.csv
data/project_core_direct_wave_green_transfer_arrays.npz
figures/project_core_direct_wave_geometry.png
figures/project_core_direct_wave_offset_metrics.png
figures/project_core_direct_wave_frequency_metrics.png
docs/PROJECT_CORE_DIRECT_WAVE_GREEN_TRANSFER_AUDIT.md
```

## Result

```text
source count:                            7
Tx/Rx offsets:                           0.02, 0.04, 0.06, 0.08, 0.10 m
pair count:                              35
selected frequency bins:                 17
all-pair direct symmetric L2:            1.3817060385586055
reference-offset transfer symmetric L2:  1.1999907091021738
max offset transfer symmetric L2:        1.7860352411892388
max per-offset symmetric L2:             0.360543033595403
direct-wave transfer ready:              false
```

Offset diagnostics:

| Tx/Rx offset (m) | Reference-offset transfer symmetric L2 | Per-offset symmetric L2 |
| ---: | ---: | ---: |
| 0.02 | 0.21084785831983285 | 0.21084785831983285 |
| 0.04 | 1.4273865897462932 | 0.28810247194064764 |
| 0.06 | 1.7860352411892388 | 0.32996626063031226 |
| 0.08 | 1.4662217883751718 | 0.34735924460824336 |
| 0.10 | 1.3890997647782 | 0.360543033595403 |

## Interpretation

The project-core soft source cannot currently be represented by one simple
per-frequency line-source scale across propagation distance. Calibrating at
the 20 mm Tx/Rx offset does not transfer to longer offsets. However,
per-offset calibration is much better, which points to a distance-dependent
source/receiver/finite-domain transfer mismatch rather than random numerical
failure.

This explains why runs `017` and `019` failed on scattered fields: scattered
paths involve different effective propagation distances than the direct
calibration path.

## Decision

Pause target-complexity escalation. The next useful branch is a
distance-aware project-source/Green calibration, or a project-core source
formulation that is directly comparable to the 2D line-source Green function.

Do not compare BEM against the older `outputs/experiments` archive until this
direct-wave transfer gate is resolved.

## Validation

```text
python -m py_compile run_project_core_direct_wave_green_transfer_audit.py
conda run -n gpr-fdtd-fwi python run_project_core_direct_wave_green_transfer_audit.py
```

Figure check:

```text
3 PNG figures, nonblank dynamic range, dimensions from 1187x731 to 1816x701
```

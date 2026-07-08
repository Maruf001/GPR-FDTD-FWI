# BEM Experiment 021: Project-Core Long-Offset Direct-Wave Green Transfer Audit

Date: 2026-06-24

## Purpose

Extend run `020` to longer direct-wave propagation distances. The goal is to
check whether the direct-wave source/Green mismatch is only a short-offset
artifact or persists across distances comparable to the two-leg
source-target-receiver paths in target-scattering runs.

This run still has no target.

## Output

```text
outputs/bem_experiments/021_project_core_long_offset_direct_wave_green_transfer_audit
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
Tx/Rx offsets:                           0.02, 0.04, 0.06, 0.08, 0.10, 0.14, 0.18, 0.22, 0.26 m
pair count:                              63
selected frequency bins:                 17
all-pair direct symmetric L2:            1.4992638840597787
reference-offset transfer symmetric L2:  1.2581670693015625
max offset transfer symmetric L2:        1.7827303182485217
max per-offset symmetric L2:             0.4026620237905695
direct-wave transfer ready:              false
```

Selected offset diagnostics:

| Tx/Rx offset (m) | Reference-offset transfer symmetric L2 | Per-offset symmetric L2 |
| ---: | ---: | ---: |
| 0.02 | 0.23002377570364504 | 0.23002377570364504 |
| 0.06 | 1.7827303182485217 | 0.320118596727833 |
| 0.10 | 1.3813651772229674 | 0.3012543124007648 |
| 0.18 | 1.5671042201274463 | 0.35272581188672847 |
| 0.26 | 1.4971549641546338 | 0.4026620237905695 |

## Interpretation

The source/Green mismatch persists across long direct-wave offsets. A simple
source factor calibrated at 20 mm does not transfer to longer direct paths.
Per-offset calibration remains much better, but it degrades mildly at the
longest offsets.

This strengthens the conclusion from run `020`: the project-core bridge needs
a distance-aware source/receiver transfer model or a better matched project
source formulation before target-scattering BEM comparisons are meaningful.

## Decision

Do not continue to homogeneous PEC or half-space PEC bridge gates yet. The next
useful work is to fit and validate a distance-aware direct-wave calibration
surface, then test whether it can improve the homogeneous dielectric scattered
case from run `019`.

## Validation

```text
conda run -n gpr-fdtd-fwi python run_project_core_direct_wave_green_transfer_audit.py \
  --outdir outputs/bem_experiments/021_project_core_long_offset_direct_wave_green_transfer_audit \
  --source-count 7 \
  --source-start-m 0.08 \
  --source-end-m 0.20 \
  --tx-rx-offsets-m 0.02,0.04,0.06,0.08,0.10,0.14,0.18,0.22,0.26 \
  --reference-offset-m 0.02
```

Figure check:

```text
3 PNG figures, nonblank dynamic range, dimensions from 1187x731 to 1816x701
```

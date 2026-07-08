# BEM Project-Core Bridge Source-Calibration Checkpoint

Date: 2026-06-24

## Scope

This checkpoint records the BEM-track project-core bridge work after the
homogeneous dielectric and dense direct-wave calibration branch.

No field data, field FWI, heavy GPU queue, 3D/HPC run, or neural-network
training was launched.

## Runs Added

```text
019_project_core_homogeneous_dielectric_bridge_adapter
020_project_core_direct_wave_green_transfer_audit
021_project_core_long_offset_direct_wave_green_transfer_audit
022_project_core_distance_aware_direct_wave_calibration_probe
023_project_core_dense_direct_wave_green_transfer_audit
024_project_core_dense_distance_interpolation_validation
025_project_core_homogeneous_dielectric_distance_calibrated_replay
026_project_core_arrival_window_direct_wave_audit
```

Tracked notes:

```text
docs/bem_experiments/019_project_core_homogeneous_dielectric_bridge_adapter.md
docs/bem_experiments/020_project_core_direct_wave_green_transfer_audit.md
docs/bem_experiments/021_project_core_long_offset_direct_wave_green_transfer_audit.md
docs/bem_experiments/022_project_core_distance_aware_direct_wave_calibration_probe.md
docs/bem_experiments/023_project_core_dense_direct_wave_green_transfer_audit.md
docs/bem_experiments/024_project_core_dense_distance_interpolation_validation.md
docs/bem_experiments/025_project_core_homogeneous_dielectric_distance_calibrated_replay.md
docs/bem_experiments/026_project_core_arrival_window_direct_wave_audit.md
```

## Main Findings

Run `019` removed half-space and PEC complexity. The homogeneous dielectric
target bridge still failed:

```text
direct/background relative L2:       0.2109902555403409
total time symmetric L2:             0.3506392905143433
scattered time symmetric L2:         1.5121594456531522
bridge ready:                        false
```

Runs `020` and `021` removed the target entirely. One direct-wave source factor
does not transfer across Tx/Rx offset:

```text
run 020 reference-offset transfer L2: 1.1999907091021738
run 021 reference-offset transfer L2: 1.2581670693015625
run 021 max per-offset L2:            0.4026620237905695
```

Run `022` showed that sparse distance-aware interpolation is not reliable:

```text
measured table symmetric L2:          0.30880226614764117
leave-one-offset symmetric L2:        0.9672799928720243
```

Runs `023` and `024` showed that a dense direct-wave table can interpolate
inside the sampled offset range:

```text
run 023 max per-offset L2:            0.4418908733177504
run 024 measured table L2:            0.3347857456839477
run 024 even/odd validation L2:       0.34190295352453876
run 024 dense interpolation ready:    true
```

Run `025` applied that dense distance calibration to the homogeneous
dielectric target. It did not repair the scattered-field bridge:

```text
direct-offset scattered L2:           1.520128574804845
broken-path scattered L2:             1.4544669770583798
broken-path total L2:                 0.43040354025518324
target replay ready:                  false
```

Run `026` tested whether simple direct-arrival windowing fixes the direct-wave
transfer gate. It does not:

```text
full all-pair symmetric L2:           1.6206668574552758
best all-pair symmetric L2:           1.6206668574552758
best reference-transfer L2:           1.3229455481578225
arrival window improves gate:         false
```

## Decision

The project-core bridge blocker is now narrower:

```text
Not primarily PEC rasterization.
Not primarily half-space layering.
Not fixed by direct-wave path-length calibration.
Not fixed by simple arrival-window cleanup.
```

The next useful work is source/receiver formulation or a true scattered-field
calibration against controlled simple targets. Do not compare BEM to the older
`outputs/experiments` archive yet.

## Current Presentation Position

BEM-owned validation through run `016` remains the strongest result.

Project-core bridge work through run `026` should be presented as disciplined
negative evidence: it prevents overclaiming and identifies the next technical
blocker before 3D, field, or inversion escalation.

## Validation

```text
python -m py_compile \
  run_project_core_homogeneous_dielectric_bridge_adapter.py \
  run_project_core_direct_wave_green_transfer_audit.py \
  run_project_core_distance_aware_direct_wave_calibration_probe.py \
  run_project_core_dense_distance_interpolation_validation.py \
  run_project_core_homogeneous_dielectric_distance_calibrated_replay.py \
  run_project_core_arrival_window_direct_wave_audit.py

git diff --check
```

Figures from runs `019` through `026` were checked for nonblank dynamic range.

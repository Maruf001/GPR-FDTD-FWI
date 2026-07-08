# BEM Experiment 030: Homogeneous Dielectric Empirical Green Replay

Date: 2026-06-25

## Purpose

Replay the earlier homogeneous dielectric target bridge from run `019` using
the empirical direct-wave Green surface from run `029`.

This is a reuse/replay audit. It does not run new FDTD simulations, use field
data, launch GPU work, or touch the historical `outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/030_project_core_homogeneous_dielectric_empirical_green_replay
```

## Result

```text
target source run:                  outputs/bem_experiments/019_project_core_homogeneous_dielectric_bridge_adapter
empirical Green run:                outputs/bem_experiments/029_project_core_empirical_green_surface_audit
target source range:                0.17 to 0.31 m
empirical Green source range:       0.06 to 0.18 m
target sources in Green range:      1 / 7
target offsets in Green range:      7 / 7
empirical Green coverage ready:     false
direct/background empirical L2:     0.3364968873804547
scattered empirical time L2:        1.493782336554112
legacy scattered time L2:           1.5121594456531522
empirical target replay ready:      false
```

## Interpretation

This run is primarily a coverage warning. The target scan from run `019` is
mostly outside the empirical source range sampled in run `029`, so this is not
a clean target-scattering verdict.

## Decision

Do not use this replay as the final target-scattering result. Run an in-range
homogeneous target case before judging the empirical baseline.

## Validation

```text
python -m py_compile run_project_core_homogeneous_dielectric_empirical_green_replay.py
python run_project_core_homogeneous_dielectric_empirical_green_replay.py
```


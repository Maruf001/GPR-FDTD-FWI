# BEM Experiment 032: In-Range Homogeneous Dielectric Empirical Green Replay

Date: 2026-06-25

## Purpose

Replay the in-range homogeneous dielectric target run `031` using the empirical
finite-domain direct-wave Green surface from run `029`.

This is the clean replay that run `030` could not provide because run `019`
was mostly outside the empirical source range.

## Output

```text
outputs/bem_experiments/032_project_core_homogeneous_dielectric_inrange_empirical_green_replay
```

## Result

```text
target source run:                  outputs/bem_experiments/031_project_core_homogeneous_dielectric_inrange_bridge_adapter
empirical Green run:                outputs/bem_experiments/029_project_core_empirical_green_surface_audit
target sources in Green range:      7 / 7
target offsets in Green range:      7 / 7
empirical Green coverage ready:     true
legacy direct/background L2:        0.2464180384607423
empirical direct/background L2:     0.01662205712366382
legacy total time L2:               0.42038566376997455
empirical total time L2:            0.35174147593288074
legacy scattered time L2:           1.5431553591086644
empirical scattered time L2:        1.552057143941903
empirical target replay ready:      false
```

## Interpretation

The empirical direct-wave baseline nearly closes the direct/background
mismatch and improves the total-field comparison, but it does not repair target
scattering. The blocker has moved away from direct-wave normalization and
toward target-scattering transfer or discrete target representation.

## Decision

Stop spending effort on direct-wave-only calibration for this bridge. Run a
controlled target-strength ladder next.

## Validation

```text
python run_project_core_homogeneous_dielectric_empirical_green_replay.py \
  --target-run outputs/bem_experiments/031_project_core_homogeneous_dielectric_inrange_bridge_adapter \
  --outdir outputs/bem_experiments/032_project_core_homogeneous_dielectric_inrange_empirical_green_replay
```


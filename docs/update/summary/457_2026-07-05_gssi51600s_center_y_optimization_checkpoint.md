# 457 - GSSI 51600S Center-Y Optimization Checkpoint

## What changed

Continued the real field-data predictor branch on the trusted GSSI 51600S scans. The finite-length 3D Fast-GPR optimizer now supports an optimized main-event crossline center parameter (`--optimize-center-z` internally; product-facing meaning: crossline y center). This adds a bounded y/crossline coordinate to the existing optimized x, cover depth, finite length, diameter, material permittivity, conductivity, and source-time shift parameters.

Generated matched real-data GSSI runs:

- `535_gssi51600s_finite_length_3d_profiles0_2_centerz_opt_smoke_iter2`: two-iteration smoke, finite loss and finite y-center gradients.
- `536_gssi51600s_finite_length_3d_profiles0_2_centerz_opt_mid_windows_iter6`: six-iteration profiles 0-2 y-center run.
- `537_gssi51600s_finite_length_3d_profiles1_3_centerz_opt_mid_windows_iter6`: six-iteration profiles 1-3 y-center run.
- `538_gssi51600s_finite_length_3d_profiles1_3_centerz_opt_mid_windows_iter24`: matched 24-iteration profiles 1-3 y-center run.
- `539_gssi51600s_finite_length_3d_profiles0_2_centerz_opt_mid_windows_iter24`: matched 24-iteration profiles 0-2 y-center run.

Built the product-facing comparison card and refreshed the current bundle:

- `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/197_gssi51600s_center_z_optimization_card_current`
- `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/198_gssi51600s_current_prediction_bundle_with_center_z_diagnostic`

## Key numbers

Matched 24-iteration comparison against fixed crossline center:

- Optimized y-center mean objective delta vs fixed: `-0.0032694637775421143`.
- Optimized y-center mean field L1 delta vs fixed: `+0.0005715787410736084`.
- Optimized y-center length-gap delta vs fixed: `+0.0059023648500442505` m.
- Optimized y-center fitted range: `0.3182916045188904` to `0.41151750087738037` m.
- Optimized y-center subset gap: `0.09322589635848999` m.
- Optimized length range: `0.1347428262233734` to `0.16977189481258392` m.
- Optimized diameter range: `13.127650134265423` to `13.568403199315071` mm.

Profiles 0-2 improved materially with y-center freedom:

- Fixed-center objective: `0.9367484450340271`.
- Optimized-center objective: `0.9301010370254517`.
- Optimized y-center: `0.41151750087738037` m.

Profiles 1-3 remained effectively tied but slightly worse:

- Fixed-center objective: `0.9654792547225952`.
- Optimized-center objective: `0.9655877351760864`.
- Optimized y-center: `0.3182916045188904` m.

## Current decision

`optimized_crossline_center_diagnostic_not_default`

The optimized y/crossline center is a real differentiable parameter and improves the mean objective, mostly through the profiles 0-2 subset. It does not improve mean waveform L1 and increases subset length disagreement, so it is not promoted as the current product default. The current bundle reports the optimized y-center range as diagnostic evidence while keeping the fixed/nonuniform crossline geometry as the default product reference.

## What remains blocked

Measured crossline profile coordinates are still the main release blocker for a single y location and finite length. The optimizer can now estimate a y-center range, but the two overlapping profile subsets prefer different y centers, so this should be treated as a diagnostic range until measured profile positions, a stronger profile-position optimizer, or a y-dependent/multi-event target model resolves the split.

## Validation and resource checks

- Focused compile passed for the modified optimizer, center-y card, current bundle, and current query scripts.
- Focused tests: `18 passed`.
- Broader GSSI/card regression suite: `166 passed`.
- Figure checks passed for:
  - center-y optimization card: `(2297, 818)` RGBA, nonblank.
  - refreshed bundle copy of the center-y figure: `(2297, 818)` RGBA, nonblank.
- Current query now reports the center-y diagnostic fields in the product-facing pretty output.

## Next defensible task

Continue the real GSSI product path by testing whether a bounded profile-position optimizer or measured-geometry intake can reduce the y-center split while preserving waveform fit. If the split remains, move to a y-dependent finite target or source/time alignment branch before making a stronger 3D rebar geometry claim.

## Marathon status

The local 20-hour marathon request is still active. This checkpoint is a progress artifact, not a stopping point.

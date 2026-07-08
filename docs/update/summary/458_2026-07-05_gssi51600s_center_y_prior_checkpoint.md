# 458 - GSSI 51600S Center-Y Prior Checkpoint

## What changed

Added an optional normalized trust-region prior for the optimized main-event crossline center in the 3D Fast-GPR field optimizer. This lets the real GSSI fit test an optimized y/crossline center while softly anchoring it near the current fixed geometry when needed.

Ran matched 24-iteration GSSI runs with the center-y prior:

- `540_gssi51600s_finite_length_3d_profiles0_2_centerz_prior_mid_windows_iter24`
- `541_gssi51600s_finite_length_3d_profiles1_3_centerz_prior_mid_windows_iter24`

Updated the center-y optimization card to compare three matched variants:

- fixed crossline center,
- unconstrained optimized crossline center,
- prior-constrained optimized crossline center.

Refreshed the current bundle:

- `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/199_gssi51600s_center_z_optimization_card_with_prior_current`
- `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/200_gssi51600s_current_prediction_bundle_with_center_z_prior_diagnostic`

## Key numbers

Prior-constrained y-center compared with fixed center:

- Mean objective delta vs fixed: `+3.096461296081543e-05`.
- Mean field L1 delta vs fixed: `+4.965066909790039e-05`.
- Fitted y-center range: `0.34635496139526367` to `0.35147595405578613` m.
- Fitted y-center gap: `0.005120992660522461` m.

Unconstrained y-center comparison retained from checkpoint 457:

- Mean objective delta vs fixed: `-0.0032694637775421143`.
- Mean field L1 delta vs fixed: `+0.0005715787410736084`.
- Fitted y-center range: `0.3182916045188904` to `0.41151750087738037` m.
- Fitted y-center gap: `0.09322589635848999` m.

## Current decision

`optimized_crossline_center_diagnostic_not_default`

The prior-constrained run shows the trust region works as a guardrail: it keeps the two profile-subset y estimates within about 5 mm of each other, but it also collapses the result back to the fixed-center geometry and provides essentially no fit gain. The unconstrained run remains useful diagnostic evidence that y-center motion can improve one subset's objective, but it is not stable enough to promote as a release y coordinate.

## What remains blocked

The predictor still needs measured crossline profile positions or a stronger profile-position/y-dependent target model before releasing a single y location and finite length. The current output correctly reports y as conditioned/diagnostic rather than measured.

## Validation and resource checks

- Focused compile passed for the modified optimizer, center-y card, current bundle, and current query scripts.
- Focused tests: `18 passed`.
- Broader GSSI/card regression suite: `166 passed`.
- `git diff --check` passed for touched tracked paths.
- Current query reports both unconstrained and prior-constrained center-y diagnostics.

## Next defensible task

Move from target-center y optimization to profile-position/source-time evidence: either test a bounded profile-position search around the current nonuniform coordinate seed, or improve source/time alignment so the y-dependent depth split can be interpreted with less ambiguity.

## Marathon status

The local 20-hour marathon request is still active. This checkpoint is a progress artifact, not a stopping point.

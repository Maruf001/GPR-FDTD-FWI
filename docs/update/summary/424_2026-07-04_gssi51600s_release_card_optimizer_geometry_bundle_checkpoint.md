# GSSI 51600S Release Card Optimizer Geometry Bundle Checkpoint

## Scope

- Added optimizer-estimated crossline geometry fields to the GSSI release-style prediction card.
- Updated the current GSSI prediction bundle default to use the newer release card.
- Regenerated the bundle after the release-card update.

## Updated Release Card

- Artifact:
  `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/125_gssi51600s_release_style_prediction_card_with_optimizer_geometry_context`
- Decision:
  `gssi51600s_prediction_card_confirmation_needed`
- Added fields:
  - `optimizer_estimated_profile_spacing_status`
  - `optimizer_estimated_profile_spacing_m`
  - `optimizer_estimated_profile_y_positions_m_if_profile0_zero`
  - `optimizer_estimated_subset_center_y_m_if_profile0_zero`
  - joint profile-spacing context

## Updated Bundle

- Artifact:
  `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/126_gssi51600s_current_prediction_bundle_with_release_card_optimizer_geometry_context`
- The bundle now points to release card `125`.
- The bundle current prediction carries the optimizer-estimated spacing branch:
  - status: `estimated_not_measured_metadata`
  - spacing: `0.22 m`
  - profile y positions if profile 0 is zero: `[0.0, 0.22, 0.44, 0.66] m`

## Validation

- Focused GSSI suite:
  `82 passed in 4.47s`
- Diff hygiene:
  `git diff --check` passed for touched query, release-card, bundle, planner, test, and daily-update files.

## Product Interpretation

The release-style card and packaged bundle now match the live query: they report a usable optimizer-estimated profile-spacing branch while preserving the boundary that the crossline profile coordinates are not measured metadata.

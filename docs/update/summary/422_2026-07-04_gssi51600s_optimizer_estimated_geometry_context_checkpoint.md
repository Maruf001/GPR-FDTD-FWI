# GSSI 51600S Optimizer-Estimated Geometry Context Checkpoint

## Scope

- Clarified the live GSSI prediction output so the old assumed y value is no longer presented as a measured coordinate.
- Added optimizer-estimated profile geometry fields derived from the dense joint spacing card.
- Regenerated the current GSSI prediction bundle after the live-query update.

## Current Live Query Change

The pretty output now prints:

- `x/y_assumed/z_m`
- `optimizer_estimated_profile_spacing_status`
- `optimizer_estimated_profile_spacing_m`
- `optimizer_estimated_profile_y_positions_m_if_profile0_zero`
- `optimizer_estimated_subset_center_y_m_if_profile0_zero`

Current values:

- optimizer-estimated spacing status: `estimated_not_measured_metadata`
- optimizer-estimated spacing: `0.22 m`
- profile y positions if profile 0 is set to zero: `[0.0, 0.22, 0.44, 0.66] m`
- subset centers under that spacing: profiles 0-2 at `0.22 m`, profiles 1-3 at `0.44 m`

## Generated Artifact

- `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/124_gssi51600s_current_prediction_bundle_with_optimizer_estimated_geometry_context`

## Validation

- Focused GSSI suite:
  `82 passed in 4.44s`
- Diff hygiene:
  `git diff --check` passed for the touched query, bundle, planner, test, and daily-update files.

## Product Interpretation

The predictor now returns a practical optimizer-estimated crossline spacing and relative profile coordinate set while still preserving the claim boundary that these are not measured survey coordinates. This keeps the 3D prediction usable without overstating y position or finite-length certainty.

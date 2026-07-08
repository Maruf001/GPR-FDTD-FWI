# GSSI51600S Residual-Mode Sensitivity Checkpoint

## What Changed

- Tested whether the `0-2` versus `1-3` length split is caused by the current `profile_mean` residual definition.
- Ran receiver-mean residual versions of the same five-window AdamW optimizer on:
  - profiles `0-2`.
  - profiles `1-3`.
- Synthesized profile-mean versus receiver-mean results into one residual-mode sensitivity artifact.

## Key Numbers

- Receiver-mean `0-2` run: `outputs/validation_exp_on_field_data/3d_geometry_inventory/430_gssi51600s_finite_length_3d_profiles0_2_receiver_mean_residual_y016_adamw_windows50_54_58_62_66_iter6/`.
  - best length `0.183968693 m`.
  - best diameter `17.316544 mm`.
  - best objective loss `0.958662629`.
  - best field L1 loss `0.936113536`.
- Receiver-mean `1-3` run: `outputs/validation_exp_on_field_data/3d_geometry_inventory/431_gssi51600s_finite_length_3d_profiles1_3_receiver_mean_residual_y016_adamw_windows50_54_58_62_66_iter6/`.
  - best length `0.186922133 m`.
  - best diameter `17.301014 mm`.
  - best objective loss `1.031250358`.
  - best field L1 loss `1.011739135`.
- Residual-mode synthesis: `outputs/validation_exp_on_field_data/3d_geometry_inventory/432_gssi51600s_finite_length_3d_residual_mode_sensitivity_profiles0_2_1_3_adamw_y016/`.
  - decision `finite_length_joint_xz_material_stability_supports_length_and_diameter`.
  - best label `rmean_profiles0_2`.
  - near-best labels `rmean_profiles0_2` only.
  - near-best length `0.183968693 m`.
  - all-run diameter range `17.295390-17.316544 mm`.

## Current Decision

The longer `1-3` branch is sensitive to residual definition. Under receiver-mean residualization, the `1-3` run collapses near the short-length branch, but its fit becomes much worse than receiver-mean `0-2`. This suggests the long `1-3` branch is linked to profile-to-profile content emphasized by `profile_mean` residualization.

The product default remains unchanged because switching residual modes would stabilize length by suppressing profile-to-profile content that may be physically meaningful. The next useful step is to test intermediate profile weighting or source/time alignment, not to silently replace the objective.

## Validation

- Both receiver-mean optimizer runs completed with finite losses and gradients.
- The residual-mode synthesis figure was visually inspected and matches the numeric rows.

## Next Defensible Task

Test a controlled profile-amplitude weighting or source/time alignment variant that can keep useful profile-to-profile information while reducing the `1-3` long-branch ambiguity.

The local marathon request remains active.

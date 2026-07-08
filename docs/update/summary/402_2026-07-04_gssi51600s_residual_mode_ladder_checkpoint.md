# GSSI51600S Residual-Mode Ladder Checkpoint

## What Changed

- Extended the residual-mode sensitivity from two modes to three modes:
  - `profile_mean`.
  - `receiver_mean`.
  - `global_mean`.
- Ran global-mean residual versions of the five-window AdamW optimizer on GSSI profiles `0-2` and `1-3`.
- Synthesized all six residual-mode/profile-subset runs into one ladder.

## Key Numbers

- Global-mean `0-2` run: `outputs/validation_exp_on_field_data/3d_geometry_inventory/433_gssi51600s_finite_length_3d_profiles0_2_global_mean_residual_y016_adamw_windows50_54_58_62_66_iter6/`.
  - best length `0.183952466 m`.
  - best diameter `17.295703 mm`.
  - best objective loss `0.981906235`.
  - best field L1 loss `0.958779454`.
- Global-mean `1-3` run: `outputs/validation_exp_on_field_data/3d_geometry_inventory/434_gssi51600s_finite_length_3d_profiles1_3_global_mean_residual_y016_adamw_windows50_54_58_62_66_iter6/`.
  - decision `finite_length_scattered_optimizer_no_material_loss_decrease`.
  - best length stayed at seed `0.199999988 m`.
  - best diameter stayed at seed `18.586002 mm`.
  - best objective loss `1.017814755`.
  - best field L1 loss `0.995747209`.
- Residual-mode ladder synthesis: `outputs/validation_exp_on_field_data/3d_geometry_inventory/435_gssi51600s_finite_length_3d_residual_mode_ladder_profiles0_2_1_3_adamw_y016/`.
  - best label `rmean_profiles0_2`.
  - near-best labels `rmean_profiles0_2` only.
  - near-best length `0.183968693 m`.
  - all-run diameter range `17.295390-18.586002 mm`.

## Current Decision

Receiver-mean residualization gives the lowest objective for the `0-2` stack and a stable short length, but it makes the `1-3` stack substantially worse. Global-mean residualization does not provide a better compromise because `1-3` does not materially optimize from the seed.

The current product default should not switch residual modes automatically. The useful conclusion is narrower: the longer `1-3` branch is tied to profile-to-profile content emphasized by `profile_mean`, so the next method improvement should be controlled profile weighting or source/time alignment, not a silent objective change.

## Validation

- Both global-mean optimizer runs completed.
- The six-row residual-mode ladder figure was visually inspected.
- Latest focused validation before this branch passed.

## Next Defensible Task

Prototype a controlled profile-weighted objective or source/time alignment variant and compare it against the profile-mean and receiver-mean ladders before changing any product default.

The local marathon request remains active.

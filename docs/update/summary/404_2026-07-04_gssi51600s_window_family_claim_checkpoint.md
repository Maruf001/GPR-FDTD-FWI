# 2026-07-04 GSSI 51600S Window-Family Claim Checkpoint

## What changed

- Tested whether the GSSI `profiles1_3` long-length branch was caused by the event-window family.
- Added two early-window profile-mean optimizer runs using sample starts `42,46,50,54,58`:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/439_gssi51600s_finite_length_3d_profiles1_3_profile_mean_early_windows_y016_adamw_windows42_46_50_54_58_iter6`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/440_gssi51600s_finite_length_3d_profiles0_2_profile_mean_early_windows_y016_adamw_windows42_46_50_54_58_iter6`
- Synthesized early, wide, mid, and single-window profile-mean runs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/441_gssi51600s_finite_length_3d_profile_mean_window_family_profiles0_2_1_3_adamw_y016`
- Added a GSSI-specific window-family product claim card:
  - `run_gssi51600s_window_family_claim_card.py`
  - `tests/test_gssi51600s_window_family_claim_card.py`
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/103_gssi51600s_window_family_claim_card_current`

## Key numbers

- `profiles0_2` early windows:
  - best length: `0.183582276 m`
  - best diameter: `17.296415 mm`
  - best field L1: `0.936874568`
  - best objective loss: `0.959273517`
- `profiles1_3` early windows:
  - best length: `0.217392877 m`
  - best diameter: `17.321652 mm`
  - best field L1: `0.966311872`
  - best objective loss: `0.982521355`
- Across the profile-mean window family:
  - `profiles0_2` length range: `0.183165550-0.183582276 m`
  - `profiles1_3` length range: `0.209991097-0.217392877 m`
  - subset length gap: `0.026408821 m`
  - `profiles0_2` length width: `0.000416726 m`
  - `profiles1_3` length width: `0.007401779 m`

## Current decision

The strict GSSI window-family claim-card decision is:

`do_not_collapse_profile_window_range_window_family_preserves_subset_split`

The tested early/mid/wide/single window families preserve the short `profiles0_2` branch and the longer `profiles1_3` branch. Therefore the current conservative GSSI product range should not be tightened by blaming the split on event-window selection.

## What remains blocked

- Crossline spacing/profile coordinates are still not metadata-confirmed.
- The length split is now less likely to be caused by time-shift prior, simple profile ordering, or tested event-window choice.
- The main remaining explanation is profile-content weighting interacting with acquisition geometry, especially because the profile with the strongest/latest local event participates in the longer branch.

## Next defensible task

Move from fixed profile coordinates to explicit profile-position sensitivity for the `profiles1_3` branch, or build a bounded geometry-parameterized run that treats crossline profile offsets as variables. This targets the current blocker directly: whether the 0.183-0.217 m length range is a real finite-length ambiguity or an artifact of assumed crossline geometry.

## Validation/resource checks

- `python run_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py ... profiles1_3 early windows ...` completed.
- `python run_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py ... profiles0_2 early windows ...` completed after rerunning a corrected CLI command.
- `python run_field_3d_0701_finite_length_optimizer_seed_stability.py ...` generated artifact `441`.
- `python run_gssi51600s_window_family_claim_card.py ...` generated artifact `103`.
- `python -m py_compile run_gssi51600s_window_family_claim_card.py` passed.
- `python -m pytest tests/test_gssi51600s_window_family_claim_card.py -q` passed: `2 passed`.
- Figure `103/.../figures/gssi51600s_window_family_claim_card.png` was visually inspected.
- Marathon request remains active; continue to the crossline-geometry sensitivity branch.

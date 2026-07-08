# Field 0704 Four-Window Raw-Amplitude Confirmation Checkpoint

## What changed
- Added a fourth nearby 0704 window to test whether the raw-amplitude objective generalizes beyond the original three-window family.
- Ran a high-amplitude time/polarity ladder for 0704 `sample68_72`.
- Ran the finite-length Fast-GPR optimizer on `sample68_72` with:
  - source frequency `20 MHz`
  - source amplitude `1e8`
  - polarity `-1`
  - shift seed `1.6 ns`
  - shift bounds `0.8-2.4 ns`
  - raw-amplitude loss weight `0.01`
  - AdamW optimizer
  - finite length, diameter, x/z geometry, epsr, and conductivity enabled
- Rebuilt the 0704 synthesis with four nearby windows.
- Refreshed product defaults to the four-window evidence:
  - transfer leaderboard `166`
  - product pointer `167`
  - predictor card `168`
  - release checklist `169`
  - release card `170`
  - range policy `171`
  - range card `172`
  - workflow command pack `173`
  - product default audit `174`
- Updated the daily note with the four-window 0704 values.

## Key numbers
- 0704 `sample68_72` ladder:
  - best shift `+16` samples, equal to `+1.6 ns`
  - best polarity `-1`
  - best ladder loss `0.787922`
  - improvement vs positive zero-shift baseline `0.033439`
- 0704 `sample68_72` optimizer:
  - decision `finite_length_scattered_optimizer_decreased_loss`
  - initial objective `0.944850`
  - best objective `0.936057`
  - objective improvement `0.008793`
  - best field L1 `0.928403`
  - best raw-amplitude L1 `0.762733`
  - best diameter `12.351951 mm`
  - best length `0.111031 m`
  - best depth `2.407379 m`
  - best epsr `3.385505`
  - best conductivity `0.00381756 S/m`
  - best shift `1.482921 ns`
- Four-window 0704 synthesis:
  - decision `finite_length_seed_stability_inconclusive`
  - run count `4`
  - max improvement `0.008793`
  - field-L1 best label `0704_sample68_72_source20_amp1e8_shift16_rawamp001`
  - field-L1 best loss `0.928403`
  - near-best diameter range `11.924520-12.475790 mm`
  - near-best length range `0.097163-0.115700 m`
  - near-best depth range `2.406148-2.458851 m`
  - near-best epsr range `3.265053-3.403231`
  - near-best conductivity range `0.003341-0.003964 S/m`

## Current decision
0704 is a stronger transfer candidate than before: four nearby windows now show meaningful optimizer response under the shift/raw-amplitude workflow. It still remains `transfer_optimizer_decreased_loss_needs_stability_confirmation`, not a shipped claim, because the length, depth, and material ranges are still wider than the 0806 release-promoted result.

0806 remains the current release-promoted real-field 3D prediction. 07011 remains a source/window repair target.

## What remains blocked
- 0704 needs either tighter four-window stability or a clearly defined range-release policy before it can be promoted.
- The next 0704 branch should be an optimizer-family check with the same four windows, or a material/range policy audit that determines whether the current ranges are acceptable as a product output.

## Validation/resource checks
- `python -m py_compile` on changed optimizer/product scripts: passed.
- Product and optimizer focused tests in conda: `35 passed, 4 skipped`.
- Optimizer tests in base Python with torch available: `10 passed`.
- Current query smoke:
  - default 0806 query returns `release_promoted_candidate`.
  - 0704 current-card query returns `transfer_needs_confirmation`.
- `git diff --check`: passed.
- Product default audit `174`: `product_defaults_ready`.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/370_field_3d_0704_fastgpr_time_polarity_ladder_transfer_seed_mid_profile4_sample68_source20_amp1e8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/371_field_3d_0704_fastgpr_transfer_seed_sample68_72_profile_mean_source20_amp1e8_adamw_conductivity_diam12_polarity_neg_shift16_ampraw001_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/372_field_3d_0704_source_amplitude_shift_rawamp001_repair_four_window_synthesis`
- `outputs/validation_exp_on_field_data/product_leaderboard/166_field_prediction_transfer_leaderboard_with_0806_three_window_and_0704_four_window_rawamp_status`
- `outputs/validation_exp_on_field_data/product_leaderboard/168_field_prediction_current_predictor_card_0806_three_window_and_0704_four_window_rawamp_status_readable`
- `outputs/validation_exp_on_field_data/product_leaderboard/170_field_prediction_release_promotion_card_0806_three_window_with_0704_four_window_rawamp_status_ready`
- `outputs/validation_exp_on_field_data/product_leaderboard/174_field_prediction_product_default_audit_0806_three_window_with_0704_four_window_rawamp_status_default`
- `docs/update/daily_update/2026-06-29_to_2026-07-05_daily_update.md`

## Next defensible task
Run a bounded optimizer-family confirmation for 0704 using the same four-window source/shift/raw-amplitude setup. If optimizer family changes do not materially alter the ranges, write a release-policy audit for whether 0704 can be shipped as a ranged transfer prediction; otherwise keep it as a confirmation target and move to another field stack.

## Marathon status
The requested local marathon remains active. Continue with real-field prediction improvement focused on shippable 3D rebar geometry/material outputs.

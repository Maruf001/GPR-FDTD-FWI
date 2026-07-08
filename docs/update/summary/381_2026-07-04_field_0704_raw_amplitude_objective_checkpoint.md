# Field 0704 Raw-Amplitude Objective Checkpoint

## What changed
- Added an optional raw-amplitude shifted L1 term to the Fast-GPR finite-length optimizer.
- Kept the existing normalized waveform L1 as the default behavior; the new term is enabled only with `--amplitude-loss-weight`.
- Added focused tests for raw shifted L1 and summary propagation of the amplitude-loss fields.
- Tested 0704 `sample64_68`, the previously unstable third window, with:
  - `+2.0 ns` shift seed
  - `1.0-3.0 ns` shift bounds
  - source amplitude `1e8`
  - raw-amplitude loss weights `0.05` and `0.01`
- Rebuilt the 0704 three-window synthesis using the useful `0.01` raw-amplitude result.
- Refreshed the current product chain to expose the improved 0704 confirmation result:
  - transfer leaderboard `157`
  - product pointer `158`
  - predictor card `159`
  - release checklist `160`
  - release card `161`
  - range policy `162`
  - range card `163`
  - workflow command pack `164`
  - product default audit `165`

## Key numbers
- 0704 `sample64_68`, raw-amplitude weight `0.05`:
  - decision `finite_length_scattered_optimizer_no_material_loss_decrease`
  - objective improvement `0.000517`
  - normalized field L1 improved from `0.939579` to `0.936211`
  - raw-amplitude L1 worsened from `0.691468` to `0.748434`
  - conclusion: the weight was too strong for promotion.
- 0704 `sample64_68`, raw-amplitude weight `0.01`:
  - decision `finite_length_scattered_optimizer_decreased_loss`
  - objective improvement `0.008120`
  - normalized field L1 improved from `0.939579` to `0.930708`
  - raw-amplitude L1 best `0.766292`
  - best diameter `11.924520 mm`
  - best length `0.097163 m`
  - best depth `2.458851 m`
  - best epsr `3.265053`
  - best conductivity `0.00396398 S/m`
  - best time shift `1.960021 ns`
- Updated 0704 three-window synthesis:
  - decision `finite_length_seed_stability_inconclusive`
  - max improvement `0.008120`
  - field-L1 best label `0704_sample64_68_source20_amp1e8_shift2_rawamp001`
  - field-L1 best loss `0.930708`
  - near-best diameter range `11.924520-12.475790 mm`
  - near-best length range `0.097163-0.115700 m`
  - near-best depth range `2.406148-2.458851 m`
  - near-best epsr range `3.265053-3.403231`
  - near-best conductivity range `0.003341-0.003964 S/m`

## Current decision
0704 is no longer just a seed-fit transfer diagnostic: all three nearby windows now have meaningful optimizer response after the shift and raw-amplitude repair. It still remains `transfer_optimizer_decreased_loss_needs_stability_confirmation`, not a shipped claim, because length/depth/material ranges are still wider than the release-promotion standard.

0806 remains the release-promoted real-field 3D prediction. 07011 remains a source/window repair target.

## What remains blocked
- 0704 needs either a tighter stability family or a release policy explicitly allowing its wider length/depth/material range.
- The next useful 0704 branch is an optimizer-family check or a fourth nearby-window repeat using the `0.01` raw-amplitude setting.
- The raw-amplitude term should remain opt-in until more field windows show that it improves stability rather than overfitting one window.

## Validation/resource checks
- `python -m py_compile` on changed optimizer/product scripts: passed.
- Product and optimizer focused tests in conda: `35 passed, 4 skipped`.
- Optimizer tests in base Python with torch available: `10 passed`.
- Current query smoke:
  - default 0806 query returns `release_promoted_candidate`.
  - 0704 current-card query returns `transfer_needs_confirmation`.
- `git diff --check`: passed.
- Product default audit `165`: `product_defaults_ready`.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/367_field_3d_0704_fastgpr_transfer_seed_sample64_68_profile_mean_source20_amp1e8_adamw_conductivity_diam12_polarity_neg_shift2_ampraw005_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/368_field_3d_0704_fastgpr_transfer_seed_sample64_68_profile_mean_source20_amp1e8_adamw_conductivity_diam12_polarity_neg_shift2_ampraw001_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/369_field_3d_0704_source_amplitude_shift2_rawamp001_repair_three_window_synthesis`
- `outputs/validation_exp_on_field_data/product_leaderboard/157_field_prediction_transfer_leaderboard_with_0806_three_window_and_0704_rawamp_repair_status`
- `outputs/validation_exp_on_field_data/product_leaderboard/159_field_prediction_current_predictor_card_0806_three_window_and_0704_rawamp_repair_status_readable`
- `outputs/validation_exp_on_field_data/product_leaderboard/161_field_prediction_release_promotion_card_0806_three_window_with_0704_rawamp_repair_status_ready`
- `outputs/validation_exp_on_field_data/product_leaderboard/165_field_prediction_product_default_audit_0806_three_window_with_0704_rawamp_repair_status_default`
- `docs/update/daily_update/2026-06-29_to_2026-07-05_daily_update.md`

## Next defensible task
Run a small 0704 confirmation pass with the same `0.01` raw-amplitude objective on either a fourth nearby window or an optimizer-family variant. If stability tightens, move 0704 into release-promotion checks; if it stays wide, keep it as a confirmation target and switch effort to another real field stack.

## Marathon status
The requested local marathon remains active. Continue with real-field prediction improvement focused on shippable 3D rebar geometry/material outputs.

# Field 0704 Shift-2 Confirmation Checkpoint

## What changed
- Tested whether the unstable 0704 third window was failing because the optimizer shift range was too narrow.
- Reran the high-amplitude local time/polarity ladder for 0704 `sample64_68`.
- Reran the 0704 `sample64_68` optimizer with a `+2.0 ns` shift seed and `1.0-3.0 ns` shift bounds.
- Rebuilt the 0704 three-window synthesis with the corrected third-window shift seed.
- Refreshed the product chain so the current defaults point to the shift-corrected 0704 synthesis:
  - transfer leaderboard `148`
  - product pointer `149`
  - predictor card `150`
  - strict release checklist `151`
  - release promotion card `152`
  - range policy `153`
  - range card `154`
  - workflow command pack `155`
  - product default audit `156`

## Key numbers
- 0704 `sample64_68` high-amplitude ladder:
  - best shift `+20` samples, equal to `+2.0 ns`
  - best polarity `-1`
  - best ladder loss `0.816310`
  - improvement vs positive zero-shift baseline `0.029119`
  - prediction standard deviation `0.150779`
  - observed standard deviation `0.271988`
- 0704 `sample64_68` shift-corrected optimizer:
  - decision `finite_length_scattered_optimizer_no_material_loss_decrease`
  - initial/best loss `0.939579`
  - best time shift `2.0 ns`
  - diameter remained `12.000000 mm`
  - length remained `0.100000 m`
- Shift-corrected 0704 three-window synthesis:
  - decision `finite_length_seed_stability_inconclusive`
  - max improvement `0.007773`
  - meaningful improvement threshold `0.001`
  - field-L1 best remains `0704_sample60_64_source20_amp1e8`
  - field-L1 best loss `0.937156`
  - near-best diameter range `12.000000-12.475790 mm`
  - near-best length range `0.100000-0.115700 m`
  - near-best depth range `2.406148-2.449669 m`
  - near-best epsr range `3.300000-3.403231`
  - near-best conductivity range `0.003341-0.003800 S/m`

## Current decision
The +2 ns diagnostic improved the third window's aligned seed loss compared with the previous +0.2 ns setup, but it did not create optimizer descent in that window. 0704 therefore stays product-visible as `transfer_optimizer_decreased_loss_needs_stability_confirmation`; it is not a shipped geometry/material claim.

0806 remains the current release-promoted field-data 3D prediction. 07011 remains a source/window repair target.

## What remains blocked
- 0704 needs another stability repair before release-promotion checks.
- The next useful 0704 branch is not another product refresh; it should test whether the third-window issue is caused by source amplitude, source waveform/windowing, or local acquisition geometry.

## Validation/resource checks
- Product scripts compiled with `python -m py_compile`: passed.
- Product-focused tests: `29 passed`.
- Current query smoke:
  - default 0806 query returns `release_promoted_candidate`.
  - 0704 query from card `150` returns `transfer_needs_confirmation`.
- `git diff --check`: passed.
- Product default audit `156`: `product_defaults_ready`.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/363_field_3d_0704_fastgpr_time_polarity_ladder_transfer_seed_mid_profile4_sample64_source20_amp1e8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/364_field_3d_0704_fastgpr_transfer_seed_sample64_68_profile_mean_source20_amp1e8_adamw_conductivity_diam12_polarity_neg_shift2_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/365_field_3d_0704_source_amplitude_shift2_repair_three_window_synthesis`
- `outputs/validation_exp_on_field_data/product_leaderboard/148_field_prediction_transfer_leaderboard_with_0806_three_window_and_0704_shift2_repair_status`
- `outputs/validation_exp_on_field_data/product_leaderboard/150_field_prediction_current_predictor_card_0806_three_window_and_0704_shift2_repair_status_readable`
- `outputs/validation_exp_on_field_data/product_leaderboard/152_field_prediction_release_promotion_card_0806_three_window_with_0704_shift2_repair_status_ready`
- `outputs/validation_exp_on_field_data/product_leaderboard/156_field_prediction_product_default_audit_0806_three_window_with_0704_shift2_repair_status_default`

## Next defensible task
Run a narrow 0704 source-amplitude or waveform/windowing diagnostic on `sample64_68`, then rerun only the third-window optimizer if the diagnostic identifies a better source setting. If that produces descent, rebuild the three-window synthesis; otherwise keep 0704 as confirmation-needed and move to the next real field stack.

## Marathon status
The requested local marathon remains active. Continue with real-field prediction improvement focused on shippable 3D rebar geometry/material outputs.

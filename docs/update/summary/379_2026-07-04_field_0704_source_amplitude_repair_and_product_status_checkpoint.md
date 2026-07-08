# Field 0704 Source-Amplitude Repair And Product Status Checkpoint

## What changed
- Added source-amplitude control to the Fast-GPR finite-length scattered optimizer so the local real-field objective can use the same amplitude setting found by the source/time ladder.
- Reran the 0704 transfer optimizer on three nearby field windows with negative polarity, 20 MHz source frequency, source amplitude `1e8`, AdamW, finite length, diameter, x/z geometry, relative permittivity, conductivity, and time shift enabled.
- Promoted the 0704 result into the product leaderboard as a confirmation-needed transfer row instead of hiding it or shipping it as a release claim.
- Refreshed the current product artifact chain with the new status:
  - transfer leaderboard `138`
  - product pointer `139`
  - predictor card `140`
  - strict release checklist `141`
  - release promotion card `142`
  - range policy `143`
  - range card `144`
  - workflow command pack `145`
  - product default audit `147`
- Updated the Saturday, July 4 daily update after completing this block.

## Key numbers
- 0704 window `sample56_60`:
  - initial loss `0.943397`
  - best loss `0.938859`
  - improvement `0.004538`
  - diameter `12.475790 mm`
  - length `0.115700 m`
  - depth `2.406148 m`
  - epsr `3.397293`
  - conductivity `0.003341 S/m`
- 0704 window `sample60_64`:
  - initial loss `0.944930`
  - best loss `0.937156`
  - improvement `0.007773`
  - diameter `12.329575 mm`
  - length `0.107735 m`
  - depth `2.418234 m`
  - epsr `3.403231`
  - conductivity `0.003629 S/m`
- 0704 window `sample64_68`:
  - initial/best loss `0.943599`
  - no optimizer decrease from the seed
  - seed diameter `12.000000 mm`
  - seed length `0.100000 m`
  - depth `2.449669 m`
  - epsr `3.300000`
  - conductivity `0.003800 S/m`
- Three-window 0704 synthesis:
  - decision `finite_length_seed_stability_inconclusive`
  - max improvement `0.007773`
  - meaningful improvement threshold `0.001`
  - near-best diameter range `12.000000-12.475790 mm`
  - near-best length range `0.100000-0.115700 m`
  - near-best depth range `2.406148-2.449669 m`
  - near-best epsr range `3.300000-3.403231`
  - near-best conductivity range `0.003341-0.003800 S/m`
  - runtime range `13.50-13.71 s`

## Current decision
0806 remains the current release-promoted 3D real-field prediction. Its default query returns x/y/z `2.4576 / 0.35 / 1.80861 m`, length `0.129125-0.129270 m`, diameter `13.8939-13.9032 mm`, epsr `3.07435`, conductivity `0.00223608 S/m`, and field L1 `0.787964`.

0704 is now product-visible as `transfer_optimizer_decreased_loss_needs_stability_confirmation`. The optimizer can decrease the real-field objective after source-amplitude repair, but one nearby window still fails to decrease, so no 0704 geometry/material claim is shipped yet.

07011 remains `transfer_seed_fit_optimizer_blocked`; its next useful work is source/window repair, not geometry promotion.

## What remains blocked
- 0704 needs a repeat stability pass before it can become a release candidate.
- 07011 needs source/window objective repair before geometry/material claims are meaningful.
- The next deliverable-oriented branch should improve source-amplitude/timing robustness on 0704, then repeat the three-window optimizer.

## Validation/resource checks
- `python -m py_compile` on changed predictor/product/Fast-GPR scripts: passed.
- Product-focused tests: `29 passed`.
- Optimizer/bridge-focused tests: `27 passed, 2 skipped`.
- `git diff --check`: passed.
- Product default audit `147`: `product_defaults_ready`.
- Current query smoke:
  - default 0806 query returns `release_promoted_candidate`.
  - 0704 current-card query returns `transfer_needs_confirmation`.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/358_field_3d_0704_fastgpr_transfer_seed_sample56_60_profile_mean_source20_amp1e8_adamw_conductivity_diam12_polarity_neg_shift02_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/359_field_3d_0704_fastgpr_transfer_seed_sample60_64_profile_mean_source20_amp1e8_adamw_conductivity_diam12_polarity_neg_shift02_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/361_field_3d_0704_fastgpr_transfer_seed_sample64_68_profile_mean_source20_amp1e8_adamw_conductivity_diam12_polarity_neg_shift02_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/362_field_3d_0704_source_amplitude_repair_three_window_synthesis`
- `outputs/validation_exp_on_field_data/product_leaderboard/138_field_prediction_transfer_leaderboard_with_0806_three_window_and_0704_amp_repair_status`
- `outputs/validation_exp_on_field_data/product_leaderboard/140_field_prediction_current_predictor_card_0806_three_window_and_0704_amp_repair_status_readable`
- `outputs/validation_exp_on_field_data/product_leaderboard/142_field_prediction_release_promotion_card_0806_three_window_with_0704_amp_repair_status_ready`
- `outputs/validation_exp_on_field_data/product_leaderboard/147_field_prediction_product_default_audit_0806_three_window_with_0704_amp_repair_status_default_row_candidates`
- `docs/update/daily_update/2026-06-29_to_2026-07-05_daily_update.md`

## Next defensible task
Rerun the 0704 confirmation branch with tighter source-amplitude/timing handling and a fourth nearby window or alternate source amplitude. If stability improves, move 0704 into release-promotion checks; if not, isolate whether the remaining mismatch comes from source windowing, acquisition geometry, or the finite-length 3D parameterization.

## Marathon status
The requested local marathon remains active. Continue with real-field prediction improvement focused on shippable 3D rebar geometry/material outputs.

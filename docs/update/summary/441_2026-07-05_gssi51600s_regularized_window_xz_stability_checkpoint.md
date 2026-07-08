# 441 2026-07-05 GSSI51600S Regularized Window X/Z Stability Checkpoint

## What changed

- Ran a matched regularized 3D GSSI event-window sensitivity pair on the uniform 0.22 m crossline geometry.
- Compared the current mid-window family (`50,54,58,62,66`) against an earlier family (`46,50,54,58,62`) for both overlapping profile subsets.
- Added a regularized event-window x/z stability card and wired it into the current GSSI prediction bundle and query output.
- Updated the daily update for July 5 with the current field-prediction status and next plan.

## Key numbers

- Mid-window mean field L1 loss: `0.932645171880722`.
- Earlier-window mean field L1 loss: `0.9425268769264221`.
- Mean field L1 delta, earlier minus mid: `0.009881705045700073`.
- Mean objective delta, earlier minus mid: `0.013721853494644165`.
- Mid-window cover-depth range: `0.096347875893116-0.138297438621521 m`.
- Earlier-window cover-depth range: `0.09917984902858734-0.10122688114643097 m`.
- Cover-depth subset gap reduction, earlier minus mid: `-0.03990253061056137 m`.
- All-window diameter range: `17.217664048075676-17.518799751996994 mm`.
- All-window length range: `0.18371789157390594-0.18713372945785522 m`.
- All-window relative permittivity range: `2.0178639888763428-2.1142635345458984`.

## Current decision

Decision: `regularized_window_timing_changes_xz_but_mid_window_fits_better`.

The earlier event window makes the x/cover-depth estimates more consistent across overlapping profile subsets, but it worsens waveform fit. The product-facing claim should therefore keep x and cover depth event-window conditioned until source/time-window alignment is confirmed.

The current latest GSSI bundle remains confirmation-needed and GSSI-only. The separate 2025 public archive is retained as a mixed-source validation archive, not as trusted evidence for the current GSSI rebar prediction unless its rebar branch is explicitly targeted.

## What remains blocked

- Crossline profile coordinates are not measured in the available GSSI sidecar metadata.
- Event-window/source-time alignment is still a meaningful uncertainty for x and cover depth.
- The release predictor should not collapse y position, finite length, x, cover depth, material, or diameter to one unconditioned 3D claim yet.

## Validation and resource checks

- `python -m py_compile run_gssi51600s_current_prediction_bundle.py run_field_prediction_current_query.py run_gssi51600s_regularized_window_xz_stability_card.py`
- `python -m pytest tests/test_gssi51600s_regularized_window_xz_stability_card.py tests/test_gssi51600s_current_prediction_bundle.py tests/test_field_prediction_current_query.py -q`
- Result: `14 passed`.
- Query smoke: `python run_field_prediction_current_query.py --dataset gssi51600s --format pretty`.
- Figure sanity checked for the card and bundled copy: both PNGs are nonblank RGBA images with size `1889 x 1379`.

## Artifact paths

- Earlier-window profiles 0/2 run: `outputs/validation_exp_on_field_data/3d_geometry_inventory/502_gssi51600s_finite_length_3d_profiles0_2_uniform_y022_domainz070_adamw_prior_stability_windows46_50_54_58_62_iter24`
- Earlier-window profiles 1/3 run: `outputs/validation_exp_on_field_data/3d_geometry_inventory/504_gssi51600s_finite_length_3d_profiles1_3_uniform_y022_domainz070_adamw_prior_stability_windows46_50_54_58_62_iter24`
- Window stability card: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/163_gssi51600s_regularized_window_xz_stability_card_current`
- Latest bundle: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/164_gssi51600s_current_prediction_bundle_with_regularized_window_xz_stability`
- Latest pointer: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`
- Daily update: `docs/update/daily_update/2026-06-29_to_2026-07-05_daily_update.md`

## Next defensible task

Run a source/time-window alignment branch that optimizes event timing more directly before broadening geometry claims. The goal is to determine whether the better x/cover-depth consistency from the earlier window can be recovered without sacrificing waveform fit.

## Marathon status

The marathon request remains active. Continue after this checkpoint with the next bounded GSSI-only product-improvement branch.

# GSSI 51600S Surface B-Scan Amplitude/Shape Diagnostic Checkpoint

## What changed

- Added `run_gssi51600s_surface_bscan_amplitude_shape_diagnostic.py`.
- Reran Fast-GPR predictions for optimized rank-3 candidate models and compared:
  - existing normalized L1,
  - raw L1,
  - scale-only amplitude-calibrated L1,
  - affine amplitude-calibrated L1.
- Tested the diagnostic helpers in `tests/test_gssi51600s_surface_bscan_amplitude_shape_diagnostic.py`.

## Key numbers

- Diagnostic artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/050_gssi51600s_surface_bscan_amplitude_shape_diagnostic`
- normalized best: continuous-shift rank 3, diameter `18.586 mm`
- scale-only best: continuous-shift rank 3, diameter `18.586 mm`
- affine best: fixed-shift rank 3, diameter `17.993 mm`
- pre-event `0.7 ns` small-diameter variant:
  - diameter `8.109 mm`
  - normalized L1 `0.849534`
  - scale-only L1 `0.060311`
  - affine L1 `0.027257`
- continuous-shift large-diameter variant:
  - diameter `18.586 mm`
  - normalized L1 `0.848794`
  - scale-only L1 `0.055589`
  - affine L1 `0.024858`

## Current decision

Amplitude-calibrated diagnostics do not overturn the large-diameter rank-3 family. They slightly prefer the fixed-shift large-diameter model under affine scaling, while normalized and scale-only losses prefer the continuous-shift large-diameter model.

This supports keeping the current product report centered on rank 3 with a large-diameter top fit, while still reporting a broad near-best diameter range because the windowed normalized objective remains sensitive.

## Claim boundary

This is diagnostic, not a new optimizer objective. It shows amplitude scaling does not rescue the smaller `8 mm` pre-event variant, but a real amplitude-aware optimizer would need to optimize source scale jointly rather than only post-fit the predicted waveform.

## Validation/resource checks

- Amplitude diagnostic tests -> `3 passed`
- Expanded GSSI predictor suite -> `42 passed`
- Diagnostic figure is nonblank, `1855 x 801`, RGB, channel range `0-255`.
- `git diff --check` on updated surface diagnostic/product/optimizer files was clean.
- Script snapshots were frozen under artifact `050`.

## Artifact paths

- Diagnostic summary: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/050_gssi51600s_surface_bscan_amplitude_shape_diagnostic/data/gssi51600s_surface_bscan_amplitude_shape_diagnostic_summary.json`
- Diagnostic rows: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/050_gssi51600s_surface_bscan_amplitude_shape_diagnostic/data/gssi51600s_surface_bscan_amplitude_shape_diagnostic_rows.csv`
- Diagnostic figure: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/050_gssi51600s_surface_bscan_amplitude_shape_diagnostic/figures/gssi51600s_surface_bscan_amplitude_shape_diagnostic.png`

## Next defensible task

Promote this into an optional optimizer objective or run a second field dataset/window with the same corrected surface pipeline. The immediate product value is higher from cross-window/cross-dataset stability than from another single-window tuning pass.

## Marathon status

The requested 20-hour local marathon is still active. Continue with cross-window or cross-dataset stability rather than stopping at this checkpoint.

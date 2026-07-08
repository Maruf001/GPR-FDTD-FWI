# GSSI 51600S Surface B-Scan Continuous Time-Shift Checkpoint

## What changed

- Added optional continuous time-shift optimization to `run_gssi51600s_surface_bscan_geometry_optimizer.py`.
- Ran detector-rank-3 corrected surface B-scan optimization with:
  - AdamW
  - `5 mm` receiver offset
  - `2 mm` diameter lower bound
  - candidate-specific window
  - shift optimized in `[70, 100]` samples
- Updated `run_gssi51600s_surface_bscan_product_report.py` to include the continuous-shift artifact.
- Regenerated the surface product report.

## Key numbers

- Continuous-shift artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/048_gssi51600s_surface_bscan_geometry_optimizer_rank3_xshift_offset005_lower_bound_2mm`
- Continuous-shift product report: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/049_gssi51600s_surface_bscan_product_report`
- fixed-shift rank 3 loss: `0.848678`
- continuous-shift rank 3 loss: `0.848337`
- optimized shift: `94.9003 samples`, `1.8980 ns`
- product x: `0.413941 m`
- product z/depth: `0.128718 m`
- product diameter proxy: `18.586 mm`
- near-best diameter range: `8.109-18.738 mm`
- product epsr: `2.044879`
- product background conductivity: `0.002187 S/m`
- status: `provisional_window_sensitive_geometry`

## Current decision

Continuous shift gives a small but real improvement and keeps the rank-3 large-diameter solution as the top fit. It does not remove the window sensitivity, because the `pre_event=0.7 ns` run remains near enough to keep the diameter range broad.

Current product prediction:

- detector rank: `3`
- x: `0.413941 m`
- z/depth: `0.128718 m`
- diameter proxy: `18.586 mm`
- near-best diameter range: `8.109-18.738 mm`
- epsr: `2.044879`
- background conductivity: `0.002187 S/m`
- y/length: not estimated from current GSSI profiles

## Claim boundary

The source-time degree of freedom is now in the optimizer, not fixed by a ladder. The claim boundary remains: diameter is not settled because modest window changes create near-best alternatives with substantially different diameter/depth.

## Validation/resource checks

- Geometry time-shift config tests -> `5 passed`
- Surface product/geometry tests -> `8 passed`
- Expanded GSSI predictor suite -> `39 passed`
- Continuous-shift figure is nonblank, `2314 x 750`, RGB, channel range `0-255`.
- Product figure is nonblank, `1957 x 750`, RGB, channel range `0-255`.
- `git diff --check` on updated surface optimizer/product files was clean.
- Script snapshots were frozen under artifacts `048` and `049`.

## Artifact paths

- Continuous-shift summary: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/048_gssi51600s_surface_bscan_geometry_optimizer_rank3_xshift_offset005_lower_bound_2mm/data/gssi51600s_surface_bscan_geometry_optimizer_summary.json`
- Continuous-shift rows: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/048_gssi51600s_surface_bscan_geometry_optimizer_rank3_xshift_offset005_lower_bound_2mm/data/gssi51600s_surface_bscan_geometry_optimizer_rows.csv`
- Product JSON: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/049_gssi51600s_surface_bscan_product_report/data/gssi51600s_surface_bscan_product_prediction.json`
- Product CSV: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/049_gssi51600s_surface_bscan_product_report/data/gssi51600s_surface_bscan_product_prediction.csv`

## Next defensible task

Add a source-amplitude or amplitude-shape objective diagnostic. The current normalized objective still lets windowing alter diameter; the next check should determine whether amplitude calibration can stabilize diameter or whether diameter remains a shape-only ambiguity.

## Marathon status

The requested 20-hour local marathon is still active. Continue with amplitude/source calibration diagnostics rather than stopping at this checkpoint.

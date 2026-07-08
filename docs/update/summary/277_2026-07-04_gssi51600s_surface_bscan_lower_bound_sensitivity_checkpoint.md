# GSSI 51600S Surface B-Scan Lower-Bound Sensitivity Checkpoint

## What changed

- Added configurable radius bounds to `run_gssi51600s_surface_bscan_geometry_optimizer.py`.
- Ran the corrected surface B-scan optimizer with a `2 mm` diameter lower bound instead of the earlier `6 mm` lower bound.
- Updated `run_gssi51600s_surface_bscan_product_report.py` so the product report includes the lower-bound sensitivity run and reports a near-best diameter range instead of a single overconfident diameter.
- Regenerated the corrected-surface GSSI product report.

## Key numbers

- Lower-bound sensitivity artifact: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/023_gssi51600s_surface_bscan_geometry_optimizer_lower_bound_2mm`
- Updated corrected-surface product report: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/024_gssi51600s_surface_bscan_product_report`
- Previous AdamW with `6 mm` diameter lower bound:
  - loss `0.884291`
  - x `0.093258 m`
  - z `0.084884 m`
  - diameter `6.727 mm`
  - epsr `2.741512`
- AdamW with `2 mm` diameter lower bound:
  - loss `0.884288`
  - x `0.093608 m`
  - z `0.081884 m`
  - diameter `4.340 mm`
  - epsr `2.741540`
- loss delta, `2 mm` lower bound minus `6 mm` lower bound: `-0.000002742`
- current product diameter status: `provisional_lower_bound_sensitive_small_diameter`
- current product near-best diameter range: `4.340-6.727 mm`
- current product background conductivity: `0.014005 S/m`
- current product source shift/polarity: `1.9 ns / -1`

## Current decision

The corrected surface B-scan adapter is still the right path for GSSI diameter work, but the diameter estimate is lower-bound sensitive. The product should report the best current fit and the near-best range, not a final diameter claim.

Current corrected-surface product prediction:

- x: `0.093608 m`
- z/depth: `0.081884 m`
- diameter proxy: `4.340 mm`
- near-best diameter range: `4.340-6.727 mm`
- epsr: `2.741540`
- background conductivity: `0.014005 S/m`
- y/length: not estimated from current GSSI profiles

## Claim boundary

The lower-bound run proves that the previous `6.7 mm` diameter was at least partly a bound artifact. This does not invalidate the x/z/material fit, but it means the diameter should be described as provisional and small-diameter-favored until source amplitude, antenna offset, and adjacent-window stability are tested.

## Validation/resource checks

- `python -m py_compile run_gssi51600s_surface_bscan_geometry_optimizer.py tests/test_gssi51600s_surface_bscan_geometry_optimizer.py`
- Bound-config tests -> `3 passed`
- Surface product/report tests -> `10 passed`
- Expanded GSSI predictor suite -> `36 passed`
- Lower-bound optimizer figure is nonblank, `2314 x 750`, RGB, channel range `0-255`.
- Updated product figure is nonblank, `1957 x 750`, RGB, channel range `0-255`.
- `git diff --check` on the updated surface optimizer/product files was clean.
- Script snapshots were frozen under artifacts `023` and `024`.

## Artifact paths

- Lower-bound summary: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/023_gssi51600s_surface_bscan_geometry_optimizer_lower_bound_2mm/data/gssi51600s_surface_bscan_geometry_optimizer_summary.json`
- Lower-bound rows: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/023_gssi51600s_surface_bscan_geometry_optimizer_lower_bound_2mm/data/gssi51600s_surface_bscan_geometry_optimizer_rows.csv`
- Updated product JSON: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/024_gssi51600s_surface_bscan_product_report/data/gssi51600s_surface_bscan_product_prediction.json`
- Updated product CSV: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/024_gssi51600s_surface_bscan_product_report/data/gssi51600s_surface_bscan_product_prediction.csv`
- Updated comparison CSV: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/024_gssi51600s_surface_bscan_product_report/data/gssi51600s_surface_bscan_optimizer_comparison.csv`

## Next defensible task

Run source/amplitude calibration or antenna-offset sensitivity for the corrected surface B-scan adapter. The diameter objective is likely using radius to compensate for source/antenna amplitude mismatch, so the next improvement should expose source scale or antenna offset before trusting diameter.

## Marathon status

The requested 20-hour local marathon is still active. Continue with source/amplitude or antenna-offset sensitivity rather than stopping at this checkpoint.

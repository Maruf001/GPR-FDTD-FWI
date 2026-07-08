# Field 3D 0701 Y/Length Optimizer Stability Checkpoint

Date: 2026-07-04

## What Changed

- Extended `run_field_3d_0701_fastgpr_y_length_window_optimizer_scan.py` to accept:
  - `--optimizer {adam,adamw,adamax}`
  - `--optimizer-weight-decay`
- Ran the same real-field 0701 y/length candidate scan with AdamW and Adamax, matching the existing Adam candidate grid.
- Added `run_field_3d_0701_fastgpr_y_length_optimizer_comparison.py`.
- Refreshed the 0701 product report so it carries y/length optimizer-stability evidence.
- Refreshed the top-level product leaderboard to point at the updated 0701 product report.

## Key Numbers

- Existing Adam y/length scan:
  - artifact `051_field_3d_0701_fastgpr_y_length_window_optimizer_scan`
  - best window profiles `1-3`
  - y center `0.200 m`
  - center-span length proxy `0.200 m`
  - best loss `0.707178115845`
- New AdamW y/length scan:
  - artifact `056_field_3d_0701_fastgpr_y_length_window_optimizer_scan_adamw`
  - best window profiles `1-3`
  - y center `0.200 m`
  - center-span length proxy `0.200 m`
  - best loss `0.707172691822`
  - best gap versus Adam `5.424e-06`
- New Adamax y/length scan:
  - artifact `057_field_3d_0701_fastgpr_y_length_window_optimizer_scan_adamax`
  - best window profiles `1-3`
  - y center `0.200 m`
  - center-span length proxy `0.200 m`
  - best loss `0.707178771496`
- Comparison artifact:
  - `058_field_3d_0701_fastgpr_y_length_optimizer_comparison`
  - decision `field_3d_0701_y_length_estimate_stable_across_optimizer_variants`
  - window stability `stable_same_best_window`
  - best-loss optimizer `adamw`
  - recommended optimizer `adam` because the AdamW loss gap is below `1e-5`
- Refreshed product report:
  - `059_field_3d_0701_predictor_product_report`
  - x `9.819386 m`
  - y center `0.200000 m`
  - z `1.507637 m`
  - length proxy `0.200000 m`
  - diameter supported range `8-30 mm`
  - epsr `4.803974`
  - fit loss `0.707159`
  - y/length optimizer stability `stable_same_best_window`
- Refreshed product leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/002_field_prediction_product_leaderboard`
  - current best product for `external_2025_pipe_0701` now points at report `059`.

## What Remains Blocked

- The 0701 diameter remains a supported range, not a unique radius estimate.
- The 0701 y/length value is still a profile-window support proxy; it is not yet a full finite-length 3D steel-cylinder FDTD inversion.
- The failed `055_field_3d_0701_fastgpr_y_length_window_optimizer_scan_adamw` attempt was caused by running in `gpr-fdtd-fwi`, which lacks `torch`; it is superseded by the successful base-Python/CUDA run `056`.

## Current Decision

The 0701 y/length estimate is stable across Adam, AdamW, and Adamax on the current real-field Fast-GPR candidate grid. This strengthens the 3D proxy product claim for y support/length, but does not solve diameter uniqueness.

## Next Defensible Task

Attack the remaining shipping blocker: radius/diameter degeneracy. The next bounded branch should run a radius-aware 0701 candidate family or profile-window/radius joint scan that reports a top radius candidate and a near-best radius range under the same real-field objective.

## Validation And Resources

- `python -m py_compile run_field_3d_0701_fastgpr_y_length_optimizer_comparison.py run_field_3d_0701_fastgpr_y_length_window_optimizer_scan.py`
- `python -m py_compile run_field_3d_0701_predictor_product_report.py`
- `python -m py_compile run_field_prediction_product_leaderboard.py`
- `python -m pytest tests/test_field_3d_0701_fastgpr_y_length_window_optimizer_scan.py tests/test_field_3d_0701_fastgpr_y_length_optimizer_comparison.py tests/test_field_3d_0701_predictor_product_report.py tests/test_field_prediction_product_leaderboard.py -q`
  - `13 passed`
- Touched-file whitespace check passed with `git diff --check -- ...`.
- Figures inspected:
  - `058.../figures/field_3d_0701_fastgpr_y_length_optimizer_comparison.png`
  - `059.../figures/field_3d_0701_predictor_product_report.png`
  - `002.../figures/field_prediction_product_leaderboard.png`

## Artifact Paths

- AdamW y/length scan:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/056_field_3d_0701_fastgpr_y_length_window_optimizer_scan_adamw`
- Adamax y/length scan:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/057_field_3d_0701_fastgpr_y_length_window_optimizer_scan_adamax`
- Optimizer comparison:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/058_field_3d_0701_fastgpr_y_length_optimizer_comparison`
- Updated product report:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/059_field_3d_0701_predictor_product_report`
- Updated top-level leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/002_field_prediction_product_leaderboard`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.

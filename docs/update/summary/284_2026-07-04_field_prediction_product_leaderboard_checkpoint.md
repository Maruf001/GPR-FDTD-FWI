# Field Prediction Product Leaderboard Checkpoint

Date: 2026-07-04

## What Changed

- Added `run_field_prediction_product_leaderboard.py`.
- Added focused tests in `tests/test_field_prediction_product_leaderboard.py`.
- Built the first product-facing leaderboard artifact at:
  - `outputs/validation_exp_on_field_data/product_leaderboard/001_field_prediction_product_leaderboard`
- The leaderboard normalizes current real-field prediction products into one CSV/JSON/figure and explicitly prevents cross-method ranking by raw loss.

## Key Numbers

- Current best products by dataset:
  - `external_2025_pipe_0701`: `fastgpr_3d_stack_y_length_proxy`
    - x `9.819386 m`
    - y center proxy `0.200000 m`
    - z `1.507637 m`
    - diameter supported range `8.0-30.0 mm`
    - epsr `4.803974`
    - fit loss `0.707159`
  - `gssi51600s`: `fastgpr_corrected_surface_bscan`
    - x `0.413941 m`
    - z `0.128718 m`
    - diameter top fit `18.586354 mm`
    - near-best diameter range `8.108958-18.738288 mm`
    - epsr `2.044879`
    - source shift `1.898005 ns`
    - receiver offset `0.005 m`
    - fit loss `0.848337`
- The GSSI legacy local-objective artifact remains indexed as diagnostic only:
  - fit loss `0.646795`
  - diameter status `not_identified_flat_loss_across_scanned_diameters`
  - not selected as current product because its objective is not comparable to the corrected surface adapter.

## What Remains Blocked

- GSSI has no measured crossline geometry in the current DZT-derived product, so y and length are not estimated there.
- GSSI corrected-surface diameter remains window/rank sensitive.
- The 0701 y/length result is still a Fast-GPR stack proxy, not a full finite-length 3D steel-cylinder FDTD inversion.

## Current Decision

Use `001_field_prediction_product_leaderboard` as the current shipping-state index for real-field prediction deliverables. It keeps 3D proxy, corrected 2D surface, and legacy diagnostic products separate so the next optimization work improves the predictor without mixing incompatible objectives.

## Next Defensible Task

Move from reporting/indexing back into predictor improvement: extend the corrected-surface/Fast-GPR product path toward a stronger 3D-style geometry estimate by adding a y/length-aware candidate family on the available field stacks and benchmarking optimizer variants under the same field-window objective.

## Validation And Resources

- `conda run -n gpr-fdtd-fwi python -m py_compile run_field_prediction_product_leaderboard.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_product_leaderboard.py -q`
- Figure inspected:
  - `figures/field_prediction_product_leaderboard.png`
  - size `2093 x 835`
  - nonblank RGB extrema.
- GPU check: NVIDIA GB10 visible and lightly loaded.

## Artifact Paths

- Summary:
  - `outputs/validation_exp_on_field_data/product_leaderboard/001_field_prediction_product_leaderboard/data/field_prediction_product_leaderboard_summary.json`
- Leaderboard CSV:
  - `outputs/validation_exp_on_field_data/product_leaderboard/001_field_prediction_product_leaderboard/data/field_prediction_product_leaderboard.csv`
- Best-by-dataset CSV:
  - `outputs/validation_exp_on_field_data/product_leaderboard/001_field_prediction_product_leaderboard/data/field_prediction_product_best_by_dataset.csv`
- Figure:
  - `outputs/validation_exp_on_field_data/product_leaderboard/001_field_prediction_product_leaderboard/figures/field_prediction_product_leaderboard.png`
- Frozen script:
  - `outputs/validation_exp_on_field_data/product_leaderboard/001_field_prediction_product_leaderboard/scripts/run_field_prediction_product_leaderboard.py`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.

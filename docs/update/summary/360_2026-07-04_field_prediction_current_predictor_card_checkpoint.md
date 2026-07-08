# Field Prediction Current Predictor Card Checkpoint

## What changed
- Added `run_field_prediction_current_predictor_card.py`, a compact product-facing export built from the active product pointer and transfer leaderboard.
- Added tests:
  - `tests/test_field_prediction_current_predictor_card.py`
- Generated predictor-card artifacts:
  - `087_field_prediction_current_predictor_card_0806_sample_window_diameter_family`
  - `088_field_prediction_current_predictor_card_0806_sample_window_diameter_family_readable`
- The readable card keeps JSON/CSV precision but rounds the Markdown table for review.

## Key numbers
- Predictor card `088`:
  - decision `current_predictor_card_ready`
  - row count `5`
  - tier counts:
    - `ships_now`: `1`
    - `next_transfer_candidate`: `1`
    - `blocked_transfer`: `2`
    - `limited_or_context`: `1`
- Shipped row:
  - `external_2025_pipe_0701`
  - x/y/z `9.81939 m / 1.5 m / 1.49399 m`
  - length `0.0968815-0.096882 m`
  - diameter `8.00039-11.9996 mm`
  - epsr `3.32975`
  - background conductivity `0.00377633 S/m`
  - fit L1 `0.600213`
- Next transfer candidate:
  - `external_2025_pipe_0806`
  - x/y/z `2.4576 m / 0.35 m / 1.80544 m`
  - length `0.0809751-0.0935682 m`
  - diameter `8.00037-13.9201 mm`
  - epsr `3.54531`
  - background conductivity `0.00620269 S/m`
  - fit L1 `0.790956`

## Current decision
The current field predictor deliverable now has a single compact card: `0701` is the current shipped 3D release row, and `0806` is the next transfer candidate with fitted geometry/material values but no release promotion.

## What remains blocked
- `0806` diameter is still a range, not a unique estimate.
- `0704` and `07011` are still blocked transfer rows.
- The predictor card is an export, not a standalone CLI/API predictor yet.

## Validation/resource checks
- `python -m py_compile run_field_prediction_current_predictor_card.py`: passed.
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_current_predictor_card.py tests/test_field_prediction_current_product_pointer.py tests/test_field_prediction_transfer_leaderboard.py -q`: `9 passed`.
- `git diff --check` on touched scripts/tests/checkpoints: passed.

## Artifact paths
- `outputs/validation_exp_on_field_data/product_leaderboard/088_field_prediction_current_predictor_card_0806_sample_window_diameter_family_readable`
- `outputs/validation_exp_on_field_data/product_leaderboard/088_field_prediction_current_predictor_card_0806_sample_window_diameter_family_readable/README.md`
- `outputs/validation_exp_on_field_data/product_leaderboard/088_field_prediction_current_predictor_card_0806_sample_window_diameter_family_readable/data/field_prediction_current_predictor_card_summary.json`
- `outputs/validation_exp_on_field_data/product_leaderboard/088_field_prediction_current_predictor_card_0806_sample_window_diameter_family_readable/data/field_prediction_current_predictor_card_rows.csv`

## Next defensible task
Build a small deterministic CLI wrapper around the current card/pointer so the deliverable can answer “what is the current prediction for dataset X?” without manually opening JSON files.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.

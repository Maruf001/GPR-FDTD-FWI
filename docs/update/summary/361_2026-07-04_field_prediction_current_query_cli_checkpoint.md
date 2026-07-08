# Field Prediction Current Query CLI Checkpoint

## What changed
- Added `run_field_prediction_current_query.py`, a deterministic CLI that reads the current predictor card and returns the current prediction for a requested dataset.
- Added tests:
  - `tests/test_field_prediction_current_query.py`
- The CLI supports:
  - `--format pretty` for readable output
  - `--format json` for machine-readable output

## Key numbers
- Validation:
  - `python -m py_compile run_field_prediction_current_query.py`: passed.
  - `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_current_query.py tests/test_field_prediction_current_predictor_card.py -q`: `7 passed`.
  - `git diff --check` on query/card branch files: passed.
- Example current transfer candidate query:
  - command: `python run_field_prediction_current_query.py --dataset external_2025_pipe_0806 --format pretty`
  - output summary:
    - tier `next_transfer_candidate`
    - action `continue_release_promotion_checks`
    - x/y/z `2.4576 / 0.35 / 1.80544 m`
    - length `0.0809751-0.0935682 m`
    - diameter `8.00037-13.9201 mm`
    - epsr `3.54531`
    - conductivity `0.00620269 S/m`
    - fit L1 `0.790956`
- Example current shipped query:
  - command: `python run_field_prediction_current_query.py --dataset external_2025_pipe_0701 --format pretty`
  - output summary:
    - tier `ships_now`
    - action `ship_as_current_release`
    - x/y/z `9.81939 / 1.5 / 1.49399 m`
    - length `0.0968815-0.096882 m`
    - diameter `8.00039-11.9996 mm`
    - epsr `3.32975`
    - conductivity `0.00377633 S/m`
    - fit L1 `0.600213`

## Current decision
The field predictor deliverable now has a small query interface on top of the current pointer/card. This is not yet a full end-user app, but it is enough to retrieve the current shipped prediction or transfer-candidate prediction deterministically from the command line.

## What remains blocked
- The CLI is read-only; it does not run fitting from raw B-scan data yet.
- `0806` is still a transfer candidate, not a shipped row.
- Diameter remains a product-safe range rather than a unique estimate.

## Artifact paths
- `run_field_prediction_current_query.py`
- `tests/test_field_prediction_current_query.py`
- `outputs/validation_exp_on_field_data/product_leaderboard/088_field_prediction_current_predictor_card_0806_sample_window_diameter_family_readable`

## Next defensible task
Start converting the fitting pipeline into a reusable predictor entry point: given a known dataset key and a configured seed/window, run the bounded Fast-GPR optimizer and update a card-like prediction artifact.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.

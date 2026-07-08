# Field Prediction Release Promotion Checklist Checkpoint

## What changed
- Added `run_field_prediction_release_promotion_checklist.py`, which evaluates whether the current `0806` transfer candidate can be promoted to a shipped row.
- Added tests:
  - `tests/test_field_prediction_release_promotion_checklist.py`
- Generated:
  - `091_field_prediction_release_promotion_checklist_0806_current`

## Key numbers
- Checklist `091`:
  - decision `release_promotion_blocked`
  - passed checks `7`
  - failed required checks `2`
- Passing release ingredients:
  - transfer candidate row exists
  - optimizer descent available
  - x/y/z available
  - finite-length range available
  - epsr available
  - conductivity optimized
  - sample-window confirmation available
- Blocking checks:
  - `diameter_unique_enough_for_release`
  - `synthesis_decision_release_ready`
- Blocking evidence:
  - diameter status `diameter_gradient_available`
  - diameter range `8.00037-13.92007 mm`
  - synthesis decision `finite_length_seed_stability_inconclusive`

## Current decision
`0806` has most of the product-shaped prediction evidence needed for release, but it cannot be promoted while diameter remains seed-sensitive and the combined synthesis remains inconclusive.

## What remains blocked
- Need reduce diameter uncertainty or explicitly change release policy to allow a broad diameter range.
- Need a synthesis decision that is not inconclusive under the selected release criteria.

## Validation/resource checks
- `python -m py_compile run_field_prediction_release_promotion_checklist.py`: passed.
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_release_promotion_checklist.py tests/test_field_prediction_product_default_audit.py -q`: `4 passed`.
- `git diff --check` on release-checklist/default-audit branch files: passed.

## Artifact paths
- `outputs/validation_exp_on_field_data/product_leaderboard/091_field_prediction_release_promotion_checklist_0806_current`
- `outputs/validation_exp_on_field_data/product_leaderboard/091_field_prediction_release_promotion_checklist_0806_current/data/field_prediction_release_promotion_checklist_summary.json`
- `run_field_prediction_release_promotion_checklist.py`

## Next defensible task
Target the remaining blocker directly: run or design a diameter-uncertainty reducer, such as a radius regularization/prior test or an objective term that penalizes seed-sensitive diameter without changing x/z/material fit.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.

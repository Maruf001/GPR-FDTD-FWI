# Field Prediction Range Release Candidate Card Checkpoint

## What changed
- Added `run_field_prediction_range_release_candidate_card.py`, which converts the release-policy result into a product-facing candidate card.
- Added tests:
  - `tests/test_field_prediction_range_release_candidate_card.py`
- Generated:
  - `093_field_prediction_range_release_candidate_card_0806`

## Key numbers
- Range card artifact `093`:
  - decision `range_release_candidate_card_ready`
  - policy decision `range_release_policy_candidate`
  - policy dataset `external_2025_pipe_0806`
  - tier `policy_conditional_range_release_candidate`
  - action `ship_only_if_diameter_range_policy_is_accepted`
  - x/y/z `2.4576 / 0.35 / 1.80544 m`
  - length-y range `0.0809751-0.0935682 m`
  - diameter range `8.00037-13.92007 mm`
  - diameter width `5.91970 mm`
  - background epsr `3.54531`
  - background conductivity `0.00620269 S/m`
  - fit field L1 loss `0.790956`

## Current decision
`external_2025_pipe_0806` is now represented as a policy-conditional range-release candidate. It is not a strict unique-diameter release. The product-facing claim is valid only if the accepted deliverable is a bounded diameter range plus the best candidate context.

## What remains blocked
- A unique diameter claim for `0806` remains blocked by the strict release checklist.
- The range-release policy still needs to be reflected in the default workflow/query path before it is product-clean.
- More geometry/source alignment work is still needed for blocked transfer datasets such as `0704` and `07011`.

## Validation/resource checks
- `python -m py_compile run_field_prediction_range_release_candidate_card.py`: passed.
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_range_release_candidate_card.py tests/test_field_prediction_release_policy_variant.py tests/test_field_prediction_current_predictor_card.py -q`: `7 passed`.
- `git diff --check` on the range-release branch files: passed.
- Runtime resources at resume: GPU lightly used, about 99 GiB RAM available.

## Artifact paths
- `outputs/validation_exp_on_field_data/product_leaderboard/093_field_prediction_range_release_candidate_card_0806`
- `outputs/validation_exp_on_field_data/product_leaderboard/093_field_prediction_range_release_candidate_card_0806/data/field_prediction_range_release_candidate_card_summary.json`
- `outputs/validation_exp_on_field_data/product_leaderboard/093_field_prediction_range_release_candidate_card_0806/README.md`
- `run_field_prediction_range_release_candidate_card.py`
- `tests/test_field_prediction_range_release_candidate_card.py`

## Next defensible task
Wire the range-release candidate into the product workflow command pack or default audit so the user-facing path exposes both choices: strict release blocks `0806`, while range-release can ship it with explicit uncertainty.

## Marathon status
The requested 20-hour local marathon remains active. This resumed segment started at `2026-07-04T17:51:19Z`, with a nominal 20-hour endpoint of `2026-07-05T13:51:19Z` if the active session remains uninterrupted.

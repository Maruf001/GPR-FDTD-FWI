# Field Prediction Range Release Policy Checkpoint

## What changed
- Added `run_field_prediction_release_policy_variant.py`, which evaluates an alternate release policy allowing explicit diameter ranges.
- Added tests:
  - `tests/test_field_prediction_release_policy_variant.py`
- Generated:
  - `092_field_prediction_release_policy_variant_0806_range_candidate`

## Key numbers
- Range-policy artifact `092`:
  - decision `range_release_policy_candidate`
  - source checklist decision `release_promotion_blocked`
  - allowed failed checks:
    - `diameter_unique_enough_for_release`
    - `synthesis_decision_release_ready`
  - actual failed checks:
    - `diameter_unique_enough_for_release`
    - `synthesis_decision_release_ready`
  - diameter range `8.00037-13.92007 mm`
  - diameter width `5.91970 mm`
  - max allowed width `8.0 mm`
  - range width check passed

## Current decision
Under the strict unique-diameter policy, `0806` remains blocked. Under a range-release policy, `0806` can be treated as a release-policy candidate because all non-diameter product checks pass and the diameter range is bounded.

## What remains blocked
- This is a policy variant, not an automatic release promotion.
- The advisor/user still needs to accept shipping diameter as an explicit range plus best-candidate context.
- If a unique diameter is required, the current evidence is insufficient.

## Validation/resource checks
- `python -m py_compile run_field_prediction_release_policy_variant.py`: passed.
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_release_policy_variant.py tests/test_field_prediction_release_promotion_checklist.py -q`: `4 passed`.
- `git diff --check` on release-policy branch files: passed.

## Artifact paths
- `outputs/validation_exp_on_field_data/product_leaderboard/092_field_prediction_release_policy_variant_0806_range_candidate`
- `outputs/validation_exp_on_field_data/product_leaderboard/092_field_prediction_release_policy_variant_0806_range_candidate/data/field_prediction_release_policy_variant_summary.json`
- `run_field_prediction_release_policy_variant.py`

## Next defensible task
Create a range-release candidate card that clearly labels `0806` as policy-conditional: shippable only if the accepted deliverable is a diameter range, not a unique diameter.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.

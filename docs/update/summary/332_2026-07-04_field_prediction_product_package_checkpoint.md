# Field Prediction Product Package Checkpoint

## What Changed

- Added a current-product package generator:
  - `run_field_prediction_product_package.py`
- Generated a single reproducible product package:
  - `062_field_prediction_product_package`
- The package includes:
  - release-candidate summary and rows,
  - shipping snapshot summary,
  - source-frequency sensitivity summary,
  - release figure,
  - exact scripts for release export, shipping snapshot, optimizer, and source-frequency synthesis.

## Key Numbers

- Package decision:
  - `current_product_package_ready`
- Copied artifacts:
  - `5`
- Script snapshots:
  - `4`
- Primary packaged prediction:
  - 0701 current best real-field 3D candidate from `061_field_prediction_release_candidate`
- Primary evidence:
  - `060_field_prediction_shipping_snapshot`
  - `257_field_3d_0701_joint_source_frequency_sensitivity`

## What Remains Blocked

- The package is a product/evidence bundle, not a new optimizer improvement.
- The scientific claim boundary remains unchanged:
  - finite length and material estimates are product candidates;
  - diameter is still a near-best range, not a unique scalar.

## Current Decision

Use `062_field_prediction_product_package` as the current shippable product folder.

The most compact machine-readable product output is:

- `outputs/validation_exp_on_field_data/product_leaderboard/062_field_prediction_product_package/data/release_candidate_field_prediction_release_candidate_rows.csv`

The full evidence trace is packaged beside it.

## Next Defensible Task

Continue with one of:

- deterministic CLI polish around the package/release export;
- combined multi-window/source-shape objective;
- external labeled/caliper data integration for diameter calibration.

## Validation And Resources

- Package-focused tests:
  - `19 passed`
- Broader product-focused suite:
  - `63 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile ...`
  - passed for changed scripts/tests
- touched-file `git diff --check`
  - passed

## Artifact Paths

- Product package:
  - `outputs/validation_exp_on_field_data/product_leaderboard/062_field_prediction_product_package`
- Release candidate:
  - `outputs/validation_exp_on_field_data/product_leaderboard/061_field_prediction_release_candidate`
- Shipping snapshot:
  - `outputs/validation_exp_on_field_data/product_leaderboard/060_field_prediction_shipping_snapshot`
- Checkpoint:
  - `docs/update/summary/332_2026-07-04_field_prediction_product_package_checkpoint.md`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.

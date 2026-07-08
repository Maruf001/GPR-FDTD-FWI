# Field Prediction Product Consistency Audit Checkpoint

## What Changed

- Added a package consistency audit:
  - `run_field_prediction_product_consistency_audit.py`
- Ran it against the current product package:
  - `063_field_prediction_product_package`
- Generated:
  - `064_field_prediction_product_consistency_audit`

## Key Numbers

- Audit decision:
  - `product_package_consistent`
- Checks:
  - `7 / 7` passed
- Verified release row matches packaged source-frequency evidence for:
  - diameter min/max,
  - length min/max,
  - fit loss.
- Verified combined-window evidence is consistent with source-frequency diameter range.

## Current Decision

The packaged product row is internally consistent with the packaged evidence artifacts.

The current shippable folder remains:

- `outputs/validation_exp_on_field_data/product_leaderboard/063_field_prediction_product_package`

## Validation And Resources

- Product audit/package/release tests:
  - `5 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile ...`
  - passed
- touched-file `git diff --check`
  - passed

## Artifact Paths

- Product consistency audit:
  - `outputs/validation_exp_on_field_data/product_leaderboard/064_field_prediction_product_consistency_audit`
- Current product package:
  - `outputs/validation_exp_on_field_data/product_leaderboard/063_field_prediction_product_package`
- Checkpoint:
  - `docs/update/summary/335_2026-07-04_field_prediction_product_consistency_audit_checkpoint.md`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.

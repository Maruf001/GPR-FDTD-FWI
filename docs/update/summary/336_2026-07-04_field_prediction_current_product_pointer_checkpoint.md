# Field Prediction Current Product Pointer Checkpoint

## What Changed

- Added:
  - `run_field_prediction_current_product_pointer.py`
- Generated:
  - `065_field_prediction_current_product_pointer`

## Key Numbers

- Pointer decision:
  - `current_product_pointer_ready`
- Current product package:
  - `outputs/validation_exp_on_field_data/product_leaderboard/063_field_prediction_product_package`
- Current release rows CSV:
  - `outputs/validation_exp_on_field_data/product_leaderboard/063_field_prediction_product_package/data/release_candidate_field_prediction_release_candidate_rows.csv`
- Current consistency audit:
  - `outputs/validation_exp_on_field_data/product_leaderboard/064_field_prediction_product_consistency_audit`
- Missing artifacts:
  - none

## Current Decision

Use `065_field_prediction_current_product_pointer` as the stable latest-pointer artifact for the current real-field predictor product.

## Validation And Resources

- Pointer/package/audit focused tests:
  - `5 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile ...`
  - passed
- touched-file `git diff --check`
  - passed

## Artifact Paths

- Current product pointer:
  - `outputs/validation_exp_on_field_data/product_leaderboard/065_field_prediction_current_product_pointer`
- Checkpoint:
  - `docs/update/summary/336_2026-07-04_field_prediction_current_product_pointer_checkpoint.md`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.

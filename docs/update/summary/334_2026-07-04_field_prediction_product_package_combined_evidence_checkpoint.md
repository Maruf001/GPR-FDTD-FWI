# Field Prediction Product Package Combined Evidence Checkpoint

## What Changed

- Updated `run_field_prediction_product_package.py` so the product package also includes combined-window robustness evidence.
- Regenerated the package:
  - `063_field_prediction_product_package`

## Key Numbers

- Package decision:
  - `current_product_package_ready`
- Packaged artifacts:
  - `6`
- Script snapshots:
  - `4`
- New packaged evidence:
  - `260_field_3d_0701_combined_window_source20_diameter_seed_stability`

## Current Decision

Use `063_field_prediction_product_package` as the current shippable product folder.

It contains:

- release candidate rows/summary,
- shipping snapshot summary,
- source-frequency sensitivity evidence,
- combined-window robustness evidence,
- product figure,
- frozen scripts.

## Validation And Resources

- Package/optimizer focused tests:
  - `6 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile ...`
  - passed
- touched-file `git diff --check`
  - passed

## Artifact Paths

- Updated package:
  - `outputs/validation_exp_on_field_data/product_leaderboard/063_field_prediction_product_package`
- Checkpoint:
  - `docs/update/summary/334_2026-07-04_field_prediction_product_package_combined_evidence_checkpoint.md`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.

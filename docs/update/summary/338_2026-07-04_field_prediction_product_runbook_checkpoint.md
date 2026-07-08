# Field Prediction Product Runbook Checkpoint

## What Changed

- Added:
  - `run_field_prediction_product_runbook.py`
- Generated:
  - `067_field_prediction_product_runbook`
- The runbook writes `run_current_product_pipeline.sh` with commands to regenerate:
  - shipping snapshot,
  - release candidate,
  - product package,
  - consistency audit,
  - current product pointer,
  - validation tests.

## Key Numbers

- Runbook decision:
  - `product_runbook_ready`
- Commands:
  - `5` product pipeline commands
  - `1` validation command
- Current package referenced:
  - `063_field_prediction_product_package`
- Current pointer referenced:
  - `065_field_prediction_current_product_pointer`

## Current Decision

Use `067_field_prediction_product_runbook` when the current product pipeline needs to be regenerated or audited.

## Validation And Resources

- Runbook/readiness/pointer tests:
  - `7 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile ...`
  - passed
- touched-file `git diff --check`
  - passed

## Artifact Paths

- Product runbook:
  - `outputs/validation_exp_on_field_data/product_leaderboard/067_field_prediction_product_runbook`
- Checkpoint:
  - `docs/update/summary/338_2026-07-04_field_prediction_product_runbook_checkpoint.md`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.

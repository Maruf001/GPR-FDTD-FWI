# Field Prediction Transfer Readiness Checkpoint

## What Changed

- Added:
  - `run_field_prediction_transfer_readiness.py`
- Generated:
  - `066_field_prediction_transfer_readiness`

## Key Numbers

- Decision:
  - `transfer_readiness_current_3d_predictor_ready_for_0701_only`
- Ready for current 3D predictor:
  - `external_2025_pipe_0701`
  - profile count `38`
  - stack shape `38 x 479 x 740`
  - time range about `187.109 ns`
- Limited:
  - `gssi51600s`
  - profile count `4`
  - stack shape `4 x 510 x 274`
  - time range `5 ns`
  - reason: limited profile count and shallow time window for finite-length 3D claim

## Current Decision

Do not claim the same finite-length 3D product transfer on GSSI51600S.

Use GSSI51600S for surface-B-scan x/z/material experiments unless additional crossline/longer-window support is added.

## Validation And Resources

- Transfer/pointer/package focused tests:
  - `6 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile ...`
  - passed
- touched-file `git diff --check`
  - passed

## Artifact Paths

- Transfer readiness:
  - `outputs/validation_exp_on_field_data/product_leaderboard/066_field_prediction_transfer_readiness`
- Current product pointer:
  - `outputs/validation_exp_on_field_data/product_leaderboard/065_field_prediction_current_product_pointer`
- Checkpoint:
  - `docs/update/summary/337_2026-07-04_field_prediction_transfer_readiness_checkpoint.md`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.

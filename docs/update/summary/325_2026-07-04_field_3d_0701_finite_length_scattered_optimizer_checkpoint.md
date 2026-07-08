# Field 3D 0701 Finite-Length Scattered Optimizer Checkpoint

## What Changed

- Added the first bounded finite-length optimizer result to the shipping snapshot.
- Kept the claim boundary explicit: this optimizer fits the receiver-mean scattered objective, not the full-field L1 objective.
- Updated and regenerated the product snapshot:
  - `054_field_prediction_shipping_snapshot`

## Key Numbers

- Finite-length optimizer artifact:
  - `237_field_3d_0701_fastgpr_finite_length_scattered_optimizer_seed_len010_diam08_adamax_iter3`
- Optimizer:
  - `Adamax`
  - `3` iterations
  - mean runtime `5.493 s/iteration`
- Objective:
  - initial scattered loss `0.769292891`
  - best scattered loss `0.766483188`
  - best loss improvement `0.002809703`
  - infinite-reference scattered loss `0.922254443`
  - best improvement vs infinite reference `0.155771255`
- Best finite geometry/material row:
  - x `9.819386151981593 m`
  - assumed y center `1.5 m`
  - z `1.488030195236206 m`
  - epsr `3.2966508865356445`
  - best finite length `0.094058372 m`
  - final finite length `0.091491562 m`
  - best diameter `8.000395261 mm`
  - final diameter `8.000391797 mm`
- Gradients:
  - max raw length gradient `3.448254574e-05`
  - max raw radius gradient `9.705857229e-10`

## What Remains Blocked

- Diameter is not yet supported by this objective because the radius gradient is effectively zero in the first bounded run.
- Length moved toward `0.09-0.10 m`, but this is a single seed/family result and must be stress-tested before changing the product prediction.
- Full-field L1 remains flat from the forward contrast branch, so the improvement is a receiver-mean scattered-objective result only.

## Current Decision

The finite-length optimizer is useful and should remain in the product evidence chain, but it is not ready to promote a final finite-length/diameter estimate.

The current shipping statement is:

- 0701 has x/y/z, epsr, conductivity, and a provisional finite-length optimizer result.
- The finite-length optimizer supports a length update around `0.09-0.10 m` on the receiver-mean scattered objective.
- Diameter remains a reported range/top candidate rather than an identified parameter.

## Next Defensible Task

Run finite-length seed and optimizer-family stability:

- seed length `0.2 m`, diameter `8 mm`, Adamax;
- seed length `0.1 m`, diameter `12 mm`, Adamax or AdamW;
- compare convergence, loss improvements, length stability, diameter gradients, and runtime.

If the optimized length repeatedly returns to `0.09-0.10 m`, promote it as a stronger receiver-mean scattered-objective finite-length candidate. If it stays seed-sensitive, keep the broader range.

## Validation And Resources

- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_shipping_snapshot.py -q`
  - `8 passed`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py tests/test_field_3d_0701_scattered_optimizer_seed_synthesis.py tests/test_field_3d_0701_predictor_product_report.py tests/test_field_3d_0701_product_stability_synthesis.py tests/test_field_3d_0701_finite_length_support_proxy.py tests/test_field_3d_0701_finite_length_support_proxy_sensitivity.py tests/test_field_3d_0701_fastgpr_finite_length_forward_contrast.py tests/test_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py tests/test_field_prediction_product_leaderboard.py tests/test_field_prediction_shipping_snapshot.py -q`
  - `41 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile ...`
  - passed for changed field-product scripts and tests
- touched-file `git diff --check`
  - passed
- Figure check:
  - `054.../figures/field_prediction_shipping_snapshot.png`: size `(2263, 750)`, stddev `64.402`

## Artifact Paths

- Finite-length optimizer:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/237_field_3d_0701_fastgpr_finite_length_scattered_optimizer_seed_len010_diam08_adamax_iter3`
- Updated shipping snapshot:
  - `outputs/validation_exp_on_field_data/product_leaderboard/054_field_prediction_shipping_snapshot`
- Checkpoint:
  - `docs/update/summary/325_2026-07-04_field_3d_0701_finite_length_scattered_optimizer_checkpoint.md`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.

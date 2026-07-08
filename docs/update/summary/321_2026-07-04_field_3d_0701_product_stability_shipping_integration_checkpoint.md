# Field 3D 0701 Product-Stability Shipping Integration Checkpoint

Date: 2026-07-04

## What Changed

- Added `run_field_3d_0701_product_stability_synthesis.py`.
- Added focused tests for the stability synthesis decisions.
- Generated a consolidated 0701 stability artifact:
  - optimizer-family stress,
  - residual-mode stress,
  - source-frequency stress,
  - timing-prior stress,
  - promoted operational product row.
- Wired the new stability artifact into the shipping snapshot.
- Regenerated the shipping snapshot so the 0701 row now carries product-stability fields directly.

## Key Numbers

- Stability artifact:
  - `227_field_3d_0701_product_stability_synthesis`
  - decision `field_3d_0701_promoted_row_stable_but_diameter_range_and_legacy_y_conflict`
  - stability status `y_length_stable_across_optimizer_residual_source_timing`
  - operational source `adaptive_scattered_common_objective`
  - x `9.819386 m`
  - y center `1.50 m`
  - z depth `1.488030 m`
  - y length center-span `0.20 m`
  - epsr `3.296651`
  - background conductivity `0.003776330 S/m`
  - fit loss `0.537833989`
  - product diameter range `8.002209-11.896786 mm`
  - stress-union diameter range `8.002196-11.965089 mm`
  - adaptive/legacy y conflict `0.25 m`
- Shipping artifact:
  - `050_field_prediction_shipping_snapshot`
  - 0701 row now includes `product_stability_status`
  - 0701 row now includes stability diameter union `8.002195507-11.965089478 mm`
  - 0701 row keeps `not_full_finite_length_3d_fdtd_inversion` as an explicit blocker.

## What Remains Blocked

- Diameter is still a reported range, not a unique field-data size claim.
- Legacy global-y conflict remains `0.25 m`.
- This is still not a full finite-length 3D FDTD steel-cylinder inversion.
- GSSI 51600S still lacks y/length support from the current surface-B-scan product.

## Current Decision

The promoted 0701 row is now guarded as the current shipping candidate:

- stable y/length under optimizer-family, residual-mode, source-frequency, and timing-prior stress;
- product-ready fields for x/y/z, y-length proxy, epsr, and background conductivity;
- diameter must be communicated as top candidate plus stress-union range;
- full-3D finite-length inversion remains the next major product upgrade path.

## Next Defensible Task

Run the next field-data improvement branch against the promoted 0701 objective with the stability synthesis as the product guard.

The highest-value branch is a finite-length 3D geometry proxy/preconditioner:

- keep the current promoted x/y/z/epsr/conductivity row fixed as the initial state;
- vary finite-length geometry parameters locally instead of restarting with broad synthetic search;
- benchmark whether finite-length effects reduce residual or narrow the diameter/length ambiguity;
- only update the shipping row if the new branch beats the current stability-guarded product.

## Validation And Resources

- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_product_stability_synthesis.py -q`
  - `3 passed`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_product_stability_synthesis.py tests/test_field_prediction_shipping_snapshot.py -q`
  - `8 passed`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py tests/test_field_3d_0701_scattered_optimizer_seed_synthesis.py tests/test_field_3d_0701_predictor_product_report.py tests/test_field_3d_0701_product_stability_synthesis.py tests/test_field_prediction_product_leaderboard.py tests/test_field_prediction_shipping_snapshot.py -q`
  - `25 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile run_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py run_field_3d_0701_scattered_optimizer_seed_synthesis.py run_field_3d_0701_predictor_product_report.py run_field_3d_0701_product_stability_synthesis.py run_field_prediction_product_leaderboard.py run_field_prediction_shipping_snapshot.py`
  - passed
- Touched-file `git diff --check` passed.
- Figure checks:
  - `227.../figures/field_3d_0701_product_stability_synthesis.png`: size `(2297, 767)`, min/max `(0, 255)`, stddev `65.615`
  - `050.../figures/field_prediction_shipping_snapshot.png`: size `(2263, 750)`, min/max `(0, 255)`, stddev `64.402`

## Artifact Paths

- Stability synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/227_field_3d_0701_product_stability_synthesis`
- Shipping snapshot:
  - `outputs/validation_exp_on_field_data/product_leaderboard/050_field_prediction_shipping_snapshot`
- Checkpoint:
  - `docs/update/summary/321_2026-07-04_field_3d_0701_product_stability_shipping_integration_checkpoint.md`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.

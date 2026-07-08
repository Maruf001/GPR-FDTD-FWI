# 254 2026-07-03 Field 3D 0701 Fast-GPR Background Anomaly Optimizer Checkpoint

## What Changed

- Added `run_field_3d_0701_fastgpr_background_anomaly_optimizer.py`.
- Added focused tests in `tests/test_field_3d_0701_fastgpr_background_anomaly_optimizer.py`.
- Generated artifact `outputs/validation_exp_on_field_data/3d_geometry_inventory/016_field_3d_0701_fastgpr_background_anomaly_optimizer/`.
- This extends run `015` from scalar homogeneous epsr to background epsr plus a fixed smooth anomaly contrast.

## Method

The optimizer uses the same real `4 x 31 x 16` 0701 field window and Fast-GPR
bridge as runs `014-015`, but parameterizes permittivity as:

```text
er = background_epsr + anomaly_delta_epsr * smooth_fixed_anomaly_mask
```

Optimized variables:

- bounded background epsr
- bounded positive anomaly delta epsr

The anomaly mask is fixed in the tiny Fast-GPR bridge grid:

- center x: `0.60 m`
- center y/depth coordinate: `1.50 m`
- sigma x: `0.15 m`
- sigma y: `0.20 m`

This is still not calibrated full-field geometry inversion; it tests whether a
richer target-like permittivity parameterization improves the tiny real-field
objective more than scalar epsr alone.

## Key Numbers

- iterations: `5`
- learning rate: `0.08`
- initial background epsr: `3.830539`
- final background epsr: `3.308675`
- initial anomaly delta epsr: `1.000000`
- final anomaly delta epsr: `0.701260`
- initial normalized field L1: `0.754463`
- final normalized field L1: `0.754448`
- loss delta: `-1.5378e-05`
- mean iteration runtime: `0.165992 s`
- finite all iterations: `True`

Comparison against scalar epsr-only run `015`:

- scalar epsr-only loss delta: `-1.6928e-05`
- background-plus-anomaly loss delta: `-1.5378e-05`
- result: the fixed anomaly mask did not improve the tiny field objective beyond scalar epsr-only.

## Current Decision

`field_3d_0701_fastgpr_background_anomaly_optimizer_decreased_field_loss`

The richer parameterization is differentiable and reduces loss, but it does not
beat scalar epsr in this tiny bridge. That is a useful negative result: the
current fixed anomaly placement/normalization is not enough. The next geometry
step should align the Fast-GPR acquisition/model coordinates to the 0701 field
window more carefully before claiming target geometry.

## Claim Boundary

This is a normalized tiny-window optimizer diagnostic. It does not yet support
rebar x/y/z/radius/length prediction. It only shows that a richer Fast-GPR
parameterization can be optimized end to end and that this particular fixed
mask is not a meaningful improvement.

## Validation

- `conda run -n gpr-fdtd-fwi python -m py_compile run_field_3d_0701_fastgpr_background_anomaly_optimizer.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_background_anomaly_optimizer.py -q`
- `conda run -n dev python -m py_compile run_field_3d_0701_fastgpr_background_anomaly_optimizer.py`
- `conda run -n dev python -m pytest tests/test_field_3d_0701_fastgpr_background_anomaly_optimizer.py -q`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_survey_geometry_inventory.py tests/test_field_3d_rad_grid_metadata_audit.py tests/test_field_3d_0701_grid_contract.py tests/test_field_3d_0701_rd3_intake_preview.py tests/test_field_3d_0701_y_spacing_sensitivity_contract.py tests/test_field_3d_0701_stack_manifest.py tests/test_field_3d_0701_acceleration_backend_benchmark.py tests/test_field_3d_0701_conditional_event_optimizer.py tests/test_field_3d_0701_fastgpr_forward_smoke.py tests/test_field_3d_0701_fastgpr_field_bridge_smoke.py tests/test_field_3d_0701_fastgpr_scalar_epsr_optimizer.py tests/test_field_3d_0701_fastgpr_background_anomaly_optimizer.py -q`
- Focused project-env result: `42 passed`.
- Focused dev-env acceleration/optimizer/Fast-GPR result: `21 passed`.
- `git diff --check -- run_field_3d_0701_fastgpr_background_anomaly_optimizer.py tests/test_field_3d_0701_fastgpr_background_anomaly_optimizer.py`
- Figure check: `field_3d_0701_fastgpr_background_anomaly_optimizer.png` is `1719 x 767` PNG.

## Artifact Paths

- Summary: `outputs/validation_exp_on_field_data/3d_geometry_inventory/016_field_3d_0701_fastgpr_background_anomaly_optimizer/data/field_3d_0701_fastgpr_background_anomaly_optimizer_summary.json`
- Iteration rows: `outputs/validation_exp_on_field_data/3d_geometry_inventory/016_field_3d_0701_fastgpr_background_anomaly_optimizer/data/field_3d_0701_fastgpr_background_anomaly_optimizer_rows.csv`
- Config: `outputs/validation_exp_on_field_data/3d_geometry_inventory/016_field_3d_0701_fastgpr_background_anomaly_optimizer/data/field_3d_0701_fastgpr_background_anomaly_optimizer_config.json`
- Figure: `outputs/validation_exp_on_field_data/3d_geometry_inventory/016_field_3d_0701_fastgpr_background_anomaly_optimizer/figures/field_3d_0701_fastgpr_background_anomaly_optimizer.png`

## Next Defensible Task

Build a coordinate-alignment audit between the 0701 field stack and the
Fast-GPR bridge grid: trace spacing, source/receiver motion, time sample
mapping, and candidate event window. The fixed anomaly mask should not be
expanded until that coordinate mapping is defensible.

## Marathon Status

The local field-data marathon remains active; this is a checkpoint, not a stop.

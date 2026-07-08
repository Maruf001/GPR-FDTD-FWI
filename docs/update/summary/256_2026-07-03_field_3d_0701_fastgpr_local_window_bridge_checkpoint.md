# 256 2026-07-03 Field 3D 0701 Fast-GPR Local Window Bridge Checkpoint

## What Changed

- Added `run_field_3d_0701_fastgpr_local_window_bridge_smoke.py`.
- Added focused tests in `tests/test_field_3d_0701_fastgpr_local_window_bridge_smoke.py`.
- Generated corrected artifact `outputs/validation_exp_on_field_data/3d_geometry_inventory/019_field_3d_0701_fastgpr_local_window_bridge_smoke/`.
- The earlier `018_field_3d_0701_fastgpr_local_window_bridge_smoke/` artifact is superseded by `019` because the summary method scope was corrected.

## Method

This branch fixes the largest coordinate problem from run `255` by replacing
the full-profile `linspace` field trace mapping with a local contiguous field
window:

- center: run `011` top candidate `x0_m=9.665786`
- center trace: `378`
- trace window: `363-393`
- trace stride: `2`
- effective field trace spacing: `0.0512 m`
- Fast-GPR receiver step: `0.05 m`

It also interpolates the field time samples to the Fast-GPR `0.1 ns` target
grid over the local comparison window:

- field dt: `0.390625 ns`
- Fast-GPR dt: `0.1 ns`
- target field window: `15.625-18.625 ns`

## Key Numbers

- epsr seed: `3.830539`
- Fast-GPR output shape: `[4, 31, 16]`
- field window shape: `[4, 31, 16]`
- normalized field L1 loss: `0.761302`
- forward time: `0.149758 s`
- backward time: `0.129400 s`
- gradient abs mean: `0.002146`
- finite forward: `True`
- finite gradient: `True`

Comparison:

- run `014` full-profile linspace bridge loss: `0.754462`
- run `019` local coordinate-aligned bridge loss: `0.761302`

The local bridge has a slightly worse normalized L1, but it is more physically
defensible because its x spacing and time sampling are aligned to the Fast-GPR
bridge.

## Current Decision

`field_3d_0701_fastgpr_local_window_bridge_ready`

The Fast-GPR bridge now has a local field window with x spacing close to the
model receiver spacing and a resampled time grid. This should replace the
full-profile linspace bridge for the next optimizer test.

## Claim Boundary

This remains a local normalized bridge smoke. The time-zero is handled as a
relative local window, not as calibrated absolute time-zero. It supports the
next optimizer loop, not final geometry claims.

## Validation

- `conda run -n gpr-fdtd-fwi python -m py_compile run_field_3d_0701_fastgpr_local_window_bridge_smoke.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_local_window_bridge_smoke.py -q`
- `conda run -n dev python -m py_compile run_field_3d_0701_fastgpr_local_window_bridge_smoke.py`
- `conda run -n dev python -m pytest tests/test_field_3d_0701_fastgpr_local_window_bridge_smoke.py -q`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_survey_geometry_inventory.py tests/test_field_3d_rad_grid_metadata_audit.py tests/test_field_3d_0701_grid_contract.py tests/test_field_3d_0701_rd3_intake_preview.py tests/test_field_3d_0701_y_spacing_sensitivity_contract.py tests/test_field_3d_0701_stack_manifest.py tests/test_field_3d_0701_acceleration_backend_benchmark.py tests/test_field_3d_0701_conditional_event_optimizer.py tests/test_field_3d_0701_fastgpr_forward_smoke.py tests/test_field_3d_0701_fastgpr_field_bridge_smoke.py tests/test_field_3d_0701_fastgpr_scalar_epsr_optimizer.py tests/test_field_3d_0701_fastgpr_background_anomaly_optimizer.py tests/test_field_3d_0701_fastgpr_coordinate_alignment_audit.py tests/test_field_3d_0701_fastgpr_local_window_bridge_smoke.py -q`
- Focused project-env result: `46 passed`.
- Focused dev-env acceleration/optimizer/Fast-GPR result: `25 passed`.
- `git diff --check -- run_field_3d_0701_fastgpr_local_window_bridge_smoke.py tests/test_field_3d_0701_fastgpr_local_window_bridge_smoke.py`
- Figure check: `field_3d_0701_fastgpr_local_window_bridge_smoke.png` is `1634 x 767` PNG.

## Artifact Paths

- Summary: `outputs/validation_exp_on_field_data/3d_geometry_inventory/019_field_3d_0701_fastgpr_local_window_bridge_smoke/data/field_3d_0701_fastgpr_local_window_bridge_smoke_summary.json`
- Row metrics: `outputs/validation_exp_on_field_data/3d_geometry_inventory/019_field_3d_0701_fastgpr_local_window_bridge_smoke/data/field_3d_0701_fastgpr_local_window_bridge_smoke_rows.csv`
- Window metadata: `outputs/validation_exp_on_field_data/3d_geometry_inventory/019_field_3d_0701_fastgpr_local_window_bridge_smoke/data/field_3d_0701_fastgpr_local_window_bridge_smoke_window_meta.json`
- Config: `outputs/validation_exp_on_field_data/3d_geometry_inventory/019_field_3d_0701_fastgpr_local_window_bridge_smoke/data/field_3d_0701_fastgpr_local_window_bridge_smoke_config.json`
- Figure: `outputs/validation_exp_on_field_data/3d_geometry_inventory/019_field_3d_0701_fastgpr_local_window_bridge_smoke/figures/field_3d_0701_fastgpr_local_window_bridge_smoke.png`

## Next Defensible Task

Rerun the scalar epsr optimizer on the corrected local-window bridge and compare
its loss decrease against run `015`. If it remains tiny, the next improvement
should be source/time alignment inside Fast-GPR rather than adding geometry
parameters.

## Marathon Status

The local field-data marathon remains active; this is a checkpoint, not a stop.

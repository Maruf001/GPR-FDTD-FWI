# 257 2026-07-03 Field 3D 0701 Fast-GPR Local Window Scalar Epsr Checkpoint

## What Changed

- Added `run_field_3d_0701_fastgpr_local_window_scalar_epsr_optimizer.py`.
- Added focused tests in `tests/test_field_3d_0701_fastgpr_local_window_scalar_epsr_optimizer.py`.
- Generated artifact `outputs/validation_exp_on_field_data/3d_geometry_inventory/020_field_3d_0701_fastgpr_local_window_scalar_epsr_optimizer/`.
- This reruns the scalar epsr Adam loop from run `015`, but on the coordinate-aligned local window from run `019`.

## Method

The optimizer reuses the Fast-GPR scalar epsr loop, but its observed field data
comes from the corrected local window:

- center trace: `378`
- trace window: `363-393`
- trace stride: `2`
- effective field dx: `0.0512 m`
- Fast-GPR receiver step: `0.05 m`
- target time window: `15.625-18.625 ns`
- Fast-GPR dt: `0.1 ns`

Optimized variable:

- bounded homogeneous epsr, initialized from run `011` top epsr.

## Key Numbers

- iterations: `5`
- learning rate: `0.08`
- initial epsr: `3.830539`
- final epsr: `4.505875`
- initial normalized field L1: `0.761302`
- final normalized field L1: `0.761298`
- loss delta: `-4.1723e-06`
- mean iteration runtime: `0.191383 s`
- finite all iterations: `True`

Per-iteration trajectory:

| iter | epsr before | epsr after | loss | raw grad | seconds |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | `3.830539` | `3.953221` | `0.761302` | `-3.949646` | `0.360627` |
| 1 | `3.953220` | `4.082076` | `0.761300` | `-4.008512` | `0.121689` |
| 2 | `4.082076` | `4.217152` | `0.761299` | `-4.049487` | `0.168007` |
| 3 | `4.217152` | `4.358442` | `0.761298` | `-4.071152` | `0.169879` |
| 4 | `4.358442` | `4.505875` | `0.761298` | `-4.072335` | `0.136713` |

## Current Decision

`field_3d_0701_fastgpr_scalar_epsr_optimizer_decreased_field_loss`

The corrected local-window bridge remains differentiable and Adam reduces the
field loss, but the reduction is even smaller than the old full-profile bridge.
The epsr direction also flips upward. This indicates the scalar epsr objective
is dominated by local normalization/source-time mismatch, not stable material
recovery.

## Comparison

- run `015`, old full-profile bridge: loss delta `-1.6928e-05`, epsr moved `3.83 -> 3.31`.
- run `020`, corrected local window: loss delta `-4.1723e-06`, epsr moved `3.83 -> 4.51`.

The corrected bridge is more physically defensible, but scalar epsr alone is not
enough. The next improvement should be source/time alignment or a measured
wavelet bridge, not more geometry parameters.

## Claim Boundary

This is still not a permittivity estimate. It is an optimizer-coupling and
coordinate-window diagnostic on a tiny normalized Fast-GPR field bridge.

## Validation

- `conda run -n gpr-fdtd-fwi python -m py_compile run_field_3d_0701_fastgpr_local_window_scalar_epsr_optimizer.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_local_window_scalar_epsr_optimizer.py -q`
- `conda run -n dev python -m py_compile run_field_3d_0701_fastgpr_local_window_scalar_epsr_optimizer.py`
- `conda run -n dev python -m pytest tests/test_field_3d_0701_fastgpr_local_window_scalar_epsr_optimizer.py -q`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_survey_geometry_inventory.py tests/test_field_3d_rad_grid_metadata_audit.py tests/test_field_3d_0701_grid_contract.py tests/test_field_3d_0701_rd3_intake_preview.py tests/test_field_3d_0701_y_spacing_sensitivity_contract.py tests/test_field_3d_0701_stack_manifest.py tests/test_field_3d_0701_acceleration_backend_benchmark.py tests/test_field_3d_0701_conditional_event_optimizer.py tests/test_field_3d_0701_fastgpr_forward_smoke.py tests/test_field_3d_0701_fastgpr_field_bridge_smoke.py tests/test_field_3d_0701_fastgpr_scalar_epsr_optimizer.py tests/test_field_3d_0701_fastgpr_background_anomaly_optimizer.py tests/test_field_3d_0701_fastgpr_coordinate_alignment_audit.py tests/test_field_3d_0701_fastgpr_local_window_bridge_smoke.py tests/test_field_3d_0701_fastgpr_local_window_scalar_epsr_optimizer.py -q`
- Focused project-env result: `47 passed`.
- Focused dev-env acceleration/optimizer/Fast-GPR result: `26 passed`.
- `git diff --check -- run_field_3d_0701_fastgpr_local_window_scalar_epsr_optimizer.py tests/test_field_3d_0701_fastgpr_local_window_scalar_epsr_optimizer.py`
- Figure check: `field_3d_0701_fastgpr_local_window_scalar_epsr_optimizer.png` is `1719 x 767` PNG.

## Artifact Paths

- Summary: `outputs/validation_exp_on_field_data/3d_geometry_inventory/020_field_3d_0701_fastgpr_local_window_scalar_epsr_optimizer/data/field_3d_0701_fastgpr_local_window_scalar_epsr_optimizer_summary.json`
- Iteration rows: `outputs/validation_exp_on_field_data/3d_geometry_inventory/020_field_3d_0701_fastgpr_local_window_scalar_epsr_optimizer/data/field_3d_0701_fastgpr_local_window_scalar_epsr_optimizer_rows.csv`
- Window metadata: `outputs/validation_exp_on_field_data/3d_geometry_inventory/020_field_3d_0701_fastgpr_local_window_scalar_epsr_optimizer/data/field_3d_0701_fastgpr_local_window_scalar_epsr_optimizer_window_meta.json`
- Figure: `outputs/validation_exp_on_field_data/3d_geometry_inventory/020_field_3d_0701_fastgpr_local_window_scalar_epsr_optimizer/figures/field_3d_0701_fastgpr_local_window_scalar_epsr_optimizer.png`

## Next Defensible Task

Add source/time alignment inside the local-window Fast-GPR objective: compare
small time shifts and polarity/sign conventions before running more geometry or
material parameters. The current scalar epsr response is too weak and unstable
for material claims.

## Marathon Status

The local field-data marathon remains active; this is a checkpoint, not a stop.

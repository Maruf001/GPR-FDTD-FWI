# 251 2026-07-03 Field 3D 0701 Fast-GPR Forward Smoke Checkpoint

## What Changed

- Added `run_field_3d_0701_fastgpr_forward_smoke.py`.
- Added focused tests in `tests/test_field_3d_0701_fastgpr_forward_smoke.py`.
- Generated artifact `outputs/validation_exp_on_field_data/3d_geometry_inventory/012_field_3d_0701_fastgpr_forward_smoke/`.
- The Fast-GPR-FWI repo is unpacked into the artifact, stale packaged `.so`
  files are removed, and all CUDA kernels are rebuilt locally before import.

## Method

This is a tiny differentiable Fast-GPR-FWI CUDA/PyTorch forward/backward smoke.
It uses the top field-fit epsr from run `011` as the homogeneous permittivity
seed and runs the paper repo's `compute(...)` path on a small grid.

This is not yet a field-stack inversion. It proves that the paper-code kernel
path can run locally and produce finite gradients.

## Key Numbers

- epsr seed from real field optimizer: `3.830539`.
- device: NVIDIA GB10.
- PyTorch: `2.9.1+cu130`.
- CUDA version reported by PyTorch: `13.0`.
- Fast-GPR stale packaged `.so` files removed: `1`.
- rebuilt local `.so` files: `6`.
- `make_returncode`: `0`.
- `make_seconds`: `3.794079`.
- forward output shape: `[2, 31, 4]`.
- forward time: `0.142513 s`.
- backward time: `0.090110 s`.
- loss abs mean: `4.570107e-07`.
- finite forward: `True`.
- finite gradient: `True`.
- gradient abs mean: `0.005646`.

## Current Decision

`field_3d_0701_fastgpr_forward_backward_ready_for_tiny_field_bridge`

The Fast-GPR-FWI CUDA/PyTorch kernel path is locally executable after rebuilding
the architecture-specific shared libraries. This removes the repo-integration
blocker found in run `009`.

## Claim Boundary

This smoke uses a tiny homogeneous model seeded by the field-fit epsr. It does
not yet fit measured B-scan amplitudes or output rebar geometry. The next step
must connect the kernel path to a real field-stack objective or document the
shape/physics mismatch that prevents that connection.

## Validation

- `conda run -n gpr-fdtd-fwi python -m py_compile run_field_3d_0701_fastgpr_forward_smoke.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_forward_smoke.py -q`
- `conda run -n dev python -m py_compile run_field_3d_0701_fastgpr_forward_smoke.py`
- `conda run -n dev python -m pytest tests/test_field_3d_0701_fastgpr_forward_smoke.py -q`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_survey_geometry_inventory.py tests/test_field_3d_rad_grid_metadata_audit.py tests/test_field_3d_0701_grid_contract.py tests/test_field_3d_0701_rd3_intake_preview.py tests/test_field_3d_0701_y_spacing_sensitivity_contract.py tests/test_field_3d_0701_stack_manifest.py tests/test_field_3d_0701_acceleration_backend_benchmark.py tests/test_field_3d_0701_conditional_event_optimizer.py tests/test_field_3d_0701_fastgpr_forward_smoke.py -q`
- Focused project-env result: `33 passed`.
- Focused dev-env acceleration/optimizer/Fast-GPR result: `12 passed`.
- `git diff --check -- run_field_3d_0701_fastgpr_forward_smoke.py tests/test_field_3d_0701_fastgpr_forward_smoke.py`
- Figure check: `field_3d_0701_fastgpr_forward_smoke.png` is `1175 x 784` PNG.

## Artifact Paths

- Summary: `outputs/validation_exp_on_field_data/3d_geometry_inventory/012_field_3d_0701_fastgpr_forward_smoke/data/field_3d_0701_fastgpr_forward_smoke_summary.json`
- Row metrics: `outputs/validation_exp_on_field_data/3d_geometry_inventory/012_field_3d_0701_fastgpr_forward_smoke/data/field_3d_0701_fastgpr_forward_smoke_rows.csv`
- Config: `outputs/validation_exp_on_field_data/3d_geometry_inventory/012_field_3d_0701_fastgpr_forward_smoke/data/field_3d_0701_fastgpr_forward_smoke_config.json`
- Build log: `outputs/validation_exp_on_field_data/3d_geometry_inventory/012_field_3d_0701_fastgpr_forward_smoke/data/field_3d_0701_fastgpr_forward_smoke_build.json`
- Figure: `outputs/validation_exp_on_field_data/3d_geometry_inventory/012_field_3d_0701_fastgpr_forward_smoke/figures/field_3d_0701_fastgpr_forward_smoke.png`
- Rebuilt repo snapshot: `outputs/validation_exp_on_field_data/3d_geometry_inventory/012_field_3d_0701_fastgpr_forward_smoke/repo/Fast-GPR-FWI-main/`

## Next Defensible Task

Build a field-stack bridge contract for Fast-GPR-FWI: map the run `011`
conditional parameters and run `007` field stack dimensions into the repo's
`compute(...)` acquisition/model tensors, then run the smallest measurable
field-aligned objective smoke or explicitly report the blocking mismatch.

## Marathon Status

The local field-data marathon remains active; this is a checkpoint, not a stop.

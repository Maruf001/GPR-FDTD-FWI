# 252 2026-07-03 Field 3D 0701 Fast-GPR Field Bridge Checkpoint

## What Changed

- Added `run_field_3d_0701_fastgpr_field_bridge_smoke.py`.
- Added focused tests in `tests/test_field_3d_0701_fastgpr_field_bridge_smoke.py`.
- Generated clean artifact `outputs/validation_exp_on_field_data/3d_geometry_inventory/014_field_3d_0701_fastgpr_field_bridge_smoke/`.
- A failed partial attempt exists at `013_field_3d_0701_fastgpr_field_bridge_smoke/`; it is superseded by `014`. The failure exposed that the repo's public `compute(...)` returns `[step, iterations, nrx]`, not `[step, 6, iterations, nrx]`.

## Method

This branch maps a real 0701 field-stack window to the Fast-GPR-FWI output
shape and computes a differentiable normalized field objective:

- field window shape: `[4, 31, 16]`
- Fast-GPR output shape: `[4, 31, 16]`
- loss: normalized L1 between field window and Fast-GPR output
- gradient target: homogeneous `er` seeded by the run `011` field-fit epsr

This is the first working bridge from the paper-code Fast-GPR forward kernel to
real field-stack data in this local run. It is still a bridge smoke, not a
calibrated field FWI inversion.

## Key Numbers

- epsr seed: `3.830539`.
- model grid: `nx=80`, `ny=50`, `nz=1`, `dx=0.05 m`.
- time window: `3.0e-9 s`.
- `step`: `4`.
- `nrx`: `16`.
- field sample start: `40`.
- output/field shape: `[4, 31, 16]`.
- forward time: `0.142642 s`.
- backward time: `0.119139 s`.
- normalized field L1 loss: `0.754462`.
- finite forward: `True`.
- finite gradient: `True`.
- gradient abs mean: `0.001976`.

## Current Decision

`field_3d_0701_fastgpr_field_stack_objective_bridge_ready`

Fast-GPR-FWI can now be connected to a real 0701 field-stack objective with a
finite differentiable loss and nonzero gradient. This is the practical bridge
needed before a small optimizer loop over permittivity/background or geometry.

## Claim Boundary

The bridge uses a normalized, tiny field window and a simplified homogeneous
model. It does not yet estimate rebar geometry or match calibrated amplitudes.
It proves interface viability: real field data can be shaped into the Fast-GPR
objective and backpropagated.

## Validation

- `conda run -n gpr-fdtd-fwi python -m py_compile run_field_3d_0701_fastgpr_field_bridge_smoke.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_field_bridge_smoke.py -q`
- `conda run -n dev python -m py_compile run_field_3d_0701_fastgpr_field_bridge_smoke.py`
- `conda run -n dev python -m pytest tests/test_field_3d_0701_fastgpr_field_bridge_smoke.py -q`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_survey_geometry_inventory.py tests/test_field_3d_rad_grid_metadata_audit.py tests/test_field_3d_0701_grid_contract.py tests/test_field_3d_0701_rd3_intake_preview.py tests/test_field_3d_0701_y_spacing_sensitivity_contract.py tests/test_field_3d_0701_stack_manifest.py tests/test_field_3d_0701_acceleration_backend_benchmark.py tests/test_field_3d_0701_conditional_event_optimizer.py tests/test_field_3d_0701_fastgpr_forward_smoke.py tests/test_field_3d_0701_fastgpr_field_bridge_smoke.py -q`
- Focused project-env result: `36 passed`.
- Focused dev-env acceleration/optimizer/Fast-GPR result: `15 passed`.
- `git diff --check -- run_field_3d_0701_fastgpr_field_bridge_smoke.py tests/test_field_3d_0701_fastgpr_field_bridge_smoke.py`
- Figure check: `field_3d_0701_fastgpr_field_bridge_smoke.png` is `1634 x 767` PNG.

## Artifact Paths

- Summary: `outputs/validation_exp_on_field_data/3d_geometry_inventory/014_field_3d_0701_fastgpr_field_bridge_smoke/data/field_3d_0701_fastgpr_field_bridge_smoke_summary.json`
- Row metrics: `outputs/validation_exp_on_field_data/3d_geometry_inventory/014_field_3d_0701_fastgpr_field_bridge_smoke/data/field_3d_0701_fastgpr_field_bridge_smoke_rows.csv`
- Config: `outputs/validation_exp_on_field_data/3d_geometry_inventory/014_field_3d_0701_fastgpr_field_bridge_smoke/data/field_3d_0701_fastgpr_field_bridge_smoke_config.json`
- Build log: `outputs/validation_exp_on_field_data/3d_geometry_inventory/014_field_3d_0701_fastgpr_field_bridge_smoke/data/field_3d_0701_fastgpr_field_bridge_smoke_build.json`
- Figure: `outputs/validation_exp_on_field_data/3d_geometry_inventory/014_field_3d_0701_fastgpr_field_bridge_smoke/figures/field_3d_0701_fastgpr_field_bridge_smoke.png`

## Next Defensible Task

Run the smallest Fast-GPR field optimizer loop: a few Adam iterations on a
bounded homogeneous/background permittivity parameter against the same real
field window, reporting runtime, loss decrease, epsr estimate, and whether the
gradient direction is stable. Geometry can be added after this field objective
loop is stable.

## Marathon Status

The local field-data marathon remains active; this is a checkpoint, not a stop.

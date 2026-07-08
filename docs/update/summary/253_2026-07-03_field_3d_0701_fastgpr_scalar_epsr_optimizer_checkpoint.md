# 253 2026-07-03 Field 3D 0701 Fast-GPR Scalar Epsr Optimizer Checkpoint

## What Changed

- Added `run_field_3d_0701_fastgpr_scalar_epsr_optimizer.py`.
- Added focused tests in `tests/test_field_3d_0701_fastgpr_scalar_epsr_optimizer.py`.
- Generated artifact `outputs/validation_exp_on_field_data/3d_geometry_inventory/015_field_3d_0701_fastgpr_scalar_epsr_optimizer/`.
- This is the first Fast-GPR-FWI Adam loop in this branch that optimizes a
  parameter against a real 0701 field-stack window.

## Method

The optimizer uses the run `014` Fast-GPR field bridge and promotes epsr from a
fixed seed to a bounded scalar Adam parameter:

- epsr bounds: `2-12`
- initial epsr: run `011` top field-fit epsr
- objective: normalized L1 against a real `4 x 31 x 16` field-stack window
- forward engine: rebuilt Fast-GPR-FWI CUDA/PyTorch `compute(...)`
- optimized variable: homogeneous/background scalar epsr only

This is not yet geometry inversion. It tests whether the paper-code forward
engine, field objective, autograd, and Adam update are coupled end to end.

## Key Numbers

- iterations: `5`
- learning rate: `0.08`
- initial epsr: `3.830539`
- final epsr: `3.308643`
- initial normalized field L1: `0.754462`
- final normalized field L1: `0.754445`
- loss delta: `-1.6928e-05`
- mean iteration runtime: `0.196542 s`
- finite all iterations: `True`

Per-iteration trajectory:

| iter | epsr before | epsr after | loss | raw grad | seconds |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | `3.830539` | `3.713922` | `0.754462` | `5.347372` | `0.437010` |
| 1 | `3.713922` | `3.603471` | `0.754460` | `5.062093` | `0.111883` |
| 2 | `3.603471` | `3.499161` | `0.754456` | `4.786311` | `0.105296` |
| 3 | `3.499161` | `3.400923` | `0.754452` | `4.520941` | `0.143835` |
| 4 | `3.400923` | `3.308643` | `0.754445` | `4.266646` | `0.184684` |

## Current Decision

`field_3d_0701_fastgpr_scalar_epsr_optimizer_decreased_field_loss`

The Fast-GPR-FWI field objective is differentiable and Adam can reduce the real
field-window loss. The decrease is very small, so scalar homogeneous epsr alone
does not explain the field B-scan. This supports moving next to richer
parameters, not claiming epsr recovery from this scalar loop.

## Claim Boundary

This is a tiny normalized field-window loop with a homogeneous epsr variable.
It is an optimizer-coupling result, not a rebar geometry or calibrated
permittivity prediction.

## Validation

- `conda run -n gpr-fdtd-fwi python -m py_compile run_field_3d_0701_fastgpr_scalar_epsr_optimizer.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_scalar_epsr_optimizer.py -q`
- `conda run -n dev python -m py_compile run_field_3d_0701_fastgpr_scalar_epsr_optimizer.py`
- `conda run -n dev python -m pytest tests/test_field_3d_0701_fastgpr_scalar_epsr_optimizer.py -q`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_survey_geometry_inventory.py tests/test_field_3d_rad_grid_metadata_audit.py tests/test_field_3d_0701_grid_contract.py tests/test_field_3d_0701_rd3_intake_preview.py tests/test_field_3d_0701_y_spacing_sensitivity_contract.py tests/test_field_3d_0701_stack_manifest.py tests/test_field_3d_0701_acceleration_backend_benchmark.py tests/test_field_3d_0701_conditional_event_optimizer.py tests/test_field_3d_0701_fastgpr_forward_smoke.py tests/test_field_3d_0701_fastgpr_field_bridge_smoke.py tests/test_field_3d_0701_fastgpr_scalar_epsr_optimizer.py -q`
- Focused project-env result: `39 passed`.
- Focused dev-env acceleration/optimizer/Fast-GPR result: `18 passed`.
- `git diff --check -- run_field_3d_0701_fastgpr_scalar_epsr_optimizer.py tests/test_field_3d_0701_fastgpr_scalar_epsr_optimizer.py`
- Figure check: `field_3d_0701_fastgpr_scalar_epsr_optimizer.png` is `1719 x 767` PNG.

## Artifact Paths

- Summary: `outputs/validation_exp_on_field_data/3d_geometry_inventory/015_field_3d_0701_fastgpr_scalar_epsr_optimizer/data/field_3d_0701_fastgpr_scalar_epsr_optimizer_summary.json`
- Iteration rows: `outputs/validation_exp_on_field_data/3d_geometry_inventory/015_field_3d_0701_fastgpr_scalar_epsr_optimizer/data/field_3d_0701_fastgpr_scalar_epsr_optimizer_rows.csv`
- Config: `outputs/validation_exp_on_field_data/3d_geometry_inventory/015_field_3d_0701_fastgpr_scalar_epsr_optimizer/data/field_3d_0701_fastgpr_scalar_epsr_optimizer_config.json`
- Figure: `outputs/validation_exp_on_field_data/3d_geometry_inventory/015_field_3d_0701_fastgpr_scalar_epsr_optimizer/figures/field_3d_0701_fastgpr_scalar_epsr_optimizer.png`

## Next Defensible Task

Add one richer but still bounded field parameterization to the Fast-GPR bridge:
for example a shallow rectangular/cylindrical permittivity anomaly initialized
from run `011` `x/z/length` and optimize anomaly contrast plus background epsr.
Report top values, near-best ranges, runtime, and whether the field loss
decrease is meaningfully larger than the scalar-epsr-only loop.

## Marathon Status

The local field-data marathon remains active; this is a checkpoint, not a stop.

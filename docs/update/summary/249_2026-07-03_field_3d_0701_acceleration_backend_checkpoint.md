# 249 2026-07-03 Field 3D 0701 Acceleration Backend Checkpoint

## What Changed

- Added `run_field_3d_0701_acceleration_backend_benchmark.py`.
- Added focused tests in `tests/test_field_3d_0701_acceleration_backend_benchmark.py`.
- Generated corrected artifact `outputs/validation_exp_on_field_data/3d_geometry_inventory/009_field_3d_0701_acceleration_backend_benchmark/`.
- The earlier `008_field_3d_0701_acceleration_backend_benchmark/` artifact is superseded by `009` because the script now removes packaged `.so` files and rebuilds Fast-GPR-FWI locally before import.

## Key Numbers

Benchmark input: real 0701 normalized stack from run `007`, shape
`38 x 479 x 740`, `13,469,480` float32 elements.

Median tensor-kernel times over 20 iterations:

| backend | device/status | median seconds | throughput |
| --- | --- | ---: | ---: |
| `numpy_cpu` | CPU | `0.040048` | `336.33 M elems/s` |
| `torch_cpu` | CPU | `0.064409` | `209.13 M elems/s` |
| `torch_cuda` | NVIDIA GB10 | `0.005790` | `2326.25 M elems/s` |
| `jax_jit` | `cuda:0` | `0.001806` | `7456.81 M elems/s` |
| `cupy_cuda` | unavailable in `dev` env | `nan` | `nan` |

- Fastest backend: `jax_jit`.
- JAX-vs-NumPy tensor-kernel speedup: `22.17x`.
- Torch-CUDA-vs-NumPy tensor-kernel speedup: about `6.92x`.
- Fast-GPR-FWI repo zip contains 6 `.cu` files.
- Removed 1 packaged stale `.so` before build.
- Rebuilt 6 local `.so` files with `nvcc`.
- Fast-GPR-FWI build/import status: `build_import_ready`.
- Fast-GPR-FWI local rebuild/import time evidence: `make_returncode=0`, `import_returncode=0`.

## Current Decision

`field_3d_0701_acceleration_backend_ready_for_engine_selection`

For field-stack tensor operations, JAX/JIT is the fastest local backend. PyTorch
CUDA is also usable, and the downloaded Fast-GPR-FWI CUDA/PyTorch repo can now
build and import locally after removing architecture-mismatched packaged shared
libraries.

## Important Caveat

This benchmark is a real-field-stack acceleration benchmark, not a full FDTD/FWI
runtime. It times tensor loss/regularization-style kernels on the actual 0701
stack. The next step is to wire one real forward/inversion kernel path to the
same stack and measure end-to-end optimizer iterations.

PyTorch emitted a warning that the NVIDIA GB10 has CUDA capability `12.1` while
the installed PyTorch build declares support through `12.0`; the tested CUDA
kernel still executed and produced the same scalar value as NumPy/JAX.

## Validation

- `conda run -n dev python -m py_compile run_field_3d_0701_acceleration_backend_benchmark.py`
- `conda run -n dev python -m pytest tests/test_field_3d_0701_acceleration_backend_benchmark.py -q`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_survey_geometry_inventory.py tests/test_field_3d_rad_grid_metadata_audit.py tests/test_field_3d_0701_grid_contract.py tests/test_field_3d_0701_rd3_intake_preview.py tests/test_field_3d_0701_y_spacing_sensitivity_contract.py tests/test_field_3d_0701_stack_manifest.py tests/test_field_3d_0701_acceleration_backend_benchmark.py -q`
- Focused project-env result: `26 passed`.
- Focused dev-env acceleration result: `5 passed`.
- `git diff --check -- run_field_3d_0701_acceleration_backend_benchmark.py tests/test_field_3d_0701_acceleration_backend_benchmark.py`

## Artifact Paths

- Summary: `outputs/validation_exp_on_field_data/3d_geometry_inventory/009_field_3d_0701_acceleration_backend_benchmark/data/field_3d_0701_acceleration_backend_summary.json`
- Backend rows: `outputs/validation_exp_on_field_data/3d_geometry_inventory/009_field_3d_0701_acceleration_backend_benchmark/data/field_3d_0701_acceleration_backend_rows.csv`
- Fast-GPR status: `outputs/validation_exp_on_field_data/3d_geometry_inventory/009_field_3d_0701_acceleration_backend_benchmark/data/field_3d_0701_fastgpr_repo_status.json`
- Figure: `outputs/validation_exp_on_field_data/3d_geometry_inventory/009_field_3d_0701_acceleration_backend_benchmark/figures/field_3d_0701_acceleration_backend_benchmark.png`
- Fast-GPR repo snapshot: `outputs/validation_exp_on_field_data/3d_geometry_inventory/009_field_3d_0701_acceleration_backend_benchmark/repo/Fast-GPR-FWI-main/`

## Next Defensible Task

Build a first conditional 3D parameter optimizer scaffold on the 0701 stack:
`x_m`, assumed `y_m`, `z_m`, `radius_m`, `length_y_m`, and `epsr_background`,
with hyperbola/stack-event energy used only as initialization and Fast-GPR/JAX
benchmarks used to choose the forward-engine path. The deliverable should report
top candidate values plus near-best ranges rather than suppressing degenerate
diameter/permittivity results.

## Marathon Status

The local field-data marathon remains active; this is a checkpoint, not a stop.

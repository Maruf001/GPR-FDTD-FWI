# External 2025 JAX 3D Reference Smoke Checkpoint

## What changed
- Added a tiny JAX CUDA 3D scalar FDTD reference smoke.
- The reference includes a real 3D Laplacian, z-offset receiver, and finite-y rebar-length proxy.
- Added the result to the field-method validation leaderboard as diagnostic reference evidence.

## Key numbers
- Artifact: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/268_external_2025_jax_3d_reference_smoke`
- Grid: `[32, 24, 16]`
- Time steps: `128`
- `dx`: `0.01 m`
- `dt`: `6.740416205412646e-12 s`
- JAX device: `cuda:0`
- Homogeneous z-offset peak: `0.0022601927630603313`
- Finite-y length sensitivity L1, y14 vs y6: `1.574518648794765e-08`
- Figure validation: `ok`, `96626` bytes
- Leaderboard evidence score: `1` diagnostic

## What remains blocked
- This is not a full Maxwell solver.
- This is not field-data fitting.
- This is not a 3D rebar prediction.
- The length sensitivity is nonzero but small in this first tiny setup; a stronger acquisition/scatterer placement is needed before using it as an optimizer target.

## Current decision
`external_2025_jax_3d_reference_smoke_true_z_coupled_length_sensitive`

The JAX route proves true z-coupled propagation and finite-y length sensitivity on GPU, unlike the current Fast-GPR backend. It is a reference development path, not a claim-ready inversion method.

## Next defensible task
Move this JAX reference toward a real optimizer target:
- strengthen the finite-y length sensitivity with a better source/receiver/scatterer layout;
- add differentiable parameters for x, y, z, radius, length, and epsr proxy;
- then connect a small field-window objective only after the forward model produces meaningful 3D sensitivities.

## Validation/resource checks
- `python -m py_compile run_external_2025_jax_3d_reference_smoke.py run_field_method_validation_leaderboard.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_external_2025_jax_3d_reference_smoke.py tests/test_field_method_validation_leaderboard.py -q`
- Result: `31 passed`
- Leaderboard regenerated at `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard`

## Artifact paths
- Summary: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/268_external_2025_jax_3d_reference_smoke/data/external_2025_jax_3d_reference_smoke_summary.json`
- Rows: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/268_external_2025_jax_3d_reference_smoke/data/external_2025_jax_3d_reference_smoke_rows.csv`
- Trace figure: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/268_external_2025_jax_3d_reference_smoke/figures/external_2025_jax_3d_reference_smoke_traces.png`
- Leaderboard CSV: `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard/data/field_method_validation_leaderboard.csv`

## Marathon status
The marathon request is still active; continue toward a differentiable 3D optimizer prototype rather than treating this scalar smoke as a finished result.

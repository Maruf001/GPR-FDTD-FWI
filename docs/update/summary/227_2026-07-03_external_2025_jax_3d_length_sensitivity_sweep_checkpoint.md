# External 2025 JAX 3D Length Sensitivity Sweep Checkpoint

## What changed
- Added a JAX CUDA 3D scalar layout sweep to strengthen finite-y length sensitivity.
- Tested four small 3D layouts with short-vs-long y-length cylinders.
- Extended the time window from `150` to `360` steps after the first sweep showed receivers were too far for arrival.
- Added the improved layout sweep to the field-method validation leaderboard.

## Key numbers
- Artifact: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/270_external_2025_jax_3d_length_sensitivity_sweep`
- Best layout: `through_y_center`
- Grid: `[36, 30, 18]`
- Time steps: `360`
- `dx`: `0.01 m`
- `dt`: `6.740416205412646e-12 s`
- Short y-length cells: `4`
- Long y-length cells: `18`
- Best length sensitivity L1: `0.00975995697081089`
- Best length sensitivity max: `0.09498065710067749`
- Best relative sensitivity: `0.1022554486989975`
- z-offset peak: `0.0056396666914224625`
- Improvement over prior tiny reference: `619869.2519953175`
- Figure validation: `ok`, `90984` bytes
- Leaderboard evidence score: `1` diagnostic

## What remains blocked
- This is still a scalar reference, not full Maxwell.
- This is not field-data fitting.
- This is not a rebar prediction.
- It is an optimizer-development testbed showing that y-length can produce a measurable 3D signal when acquisition geometry and time window are sane.

## Current decision
`external_2025_jax_3d_length_sensitivity_sweep_improved_layout_found`

Use the `through_y_center` geometry as the immediate scalar 3D optimizer sandbox for y-length/radius/epsr parameterization.

## Next defensible task
Add differentiable 3D scalar parameters for x, y, z, radius, length, and epsr proxy, then run a small inverse recovery test on the `through_y_center` layout. Keep it labeled as scalar-reference inversion until Maxwell-complete updates exist.

## Validation/resource checks
- `python -m py_compile run_external_2025_jax_3d_length_sensitivity_sweep.py run_field_method_validation_leaderboard.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_external_2025_jax_3d_length_sensitivity_sweep.py tests/test_field_method_validation_leaderboard.py -q`
- Result: `32 passed`
- Leaderboard regenerated at `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard`

## Artifact paths
- Summary: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/270_external_2025_jax_3d_length_sensitivity_sweep/data/external_2025_jax_3d_length_sensitivity_sweep_summary.json`
- Rows: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/270_external_2025_jax_3d_length_sensitivity_sweep/data/external_2025_jax_3d_length_sensitivity_sweep_rows.csv`
- Best-layout figure: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/270_external_2025_jax_3d_length_sensitivity_sweep/figures/external_2025_jax_3d_length_sensitivity_best_layout.png`
- Leaderboard CSV: `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard/data/field_method_validation_leaderboard.csv`

## Marathon status
The marathon request is still active; continue with differentiable 3D scalar parameter recovery next.

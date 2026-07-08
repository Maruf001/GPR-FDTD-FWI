# External 2025 Fast-GPR 3D Forward Smoke Checkpoint

## What changed
- Added a reproducible patched Fast-GPR non-singleton-z forward smoke.
- Added a stricter z-coupling criterion:
  - z-offset receiver must be nonzero.
  - core CUDA field-update kernel must contain z-derivative terms.
- Superseded the too-loose artifact `266` with corrected artifact `267`.
- Added the forward-smoke result to the field-method validation leaderboard.

## Key numbers
- Artifact: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/267_external_2025_fastgpr_3d_forward_smoke`
- Grid: `nx=16`, `ny=14`, `nz=6`, `dx=0.01 m`
- Runtime: `0.10402652202174067 s`
- CUDA peak memory: `0.52392578125 MB`
- Output shape: `[1, 79, 3]`
- Output finite: `true`
- Nonzero samples: `148`
- Peak receiver amplitudes: `[1623.9466552734375, 1087.01953125, 0.0]`
- z-offset receiver peak: `0.0`
- Core kernel z-coupling terms present: `false`
- Leaderboard evidence score: `1` diagnostic

## What remains blocked
- The patched backend allocates and indexes non-singleton-z arrays, but the core `fields_updates_gpu.cu` update is still effectively 2D-TMz/extruded:
  - it updates Ez/Hx/Hy;
  - it does not update Ex/Ey/Hz in the core field-update kernel;
  - it does not include `k + 1` or `k - 1` z-derivative terms.
- Therefore this Fast-GPR code path is not yet valid for full 3D y-location or rebar-length prediction.

## Current decision
`external_2025_fastgpr_3d_forward_smoke_blocked_z_offset_zero_or_no_z_derivatives`

Treat the current Fast-GPR repo as an accelerated 2D-TMz/extruded backend for our project until the field-update kernels are replaced or extended for true 3D.

## Next defensible task
Do not build 3D field-data inversion on this backend yet. The next 3D path should either:
- implement true 3D Ex/Ey/Ez/Hx/Hy/Hz CUDA updates with z derivatives, then rerun the smoke; or
- build a small JAX/PyTorch 3D reference FDTD forward smoke for benchmarking before reconnecting field-data inversion.

## Validation/resource checks
- `python -m py_compile run_external_2025_fastgpr_3d_forward_smoke.py run_field_method_validation_leaderboard.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_external_2025_fastgpr_3d_forward_smoke.py tests/test_field_method_validation_leaderboard.py -q`
- Result: `30 passed`
- Leaderboard regenerated at `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard`

## Artifact paths
- Smoke summary: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/267_external_2025_fastgpr_3d_forward_smoke/data/external_2025_fastgpr_3d_forward_smoke_summary.json`
- Smoke rows: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/267_external_2025_fastgpr_3d_forward_smoke/data/external_2025_fastgpr_3d_forward_smoke_rows.csv`
- Trace figure: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/267_external_2025_fastgpr_3d_forward_smoke/figures/external_2025_fastgpr_3d_forward_smoke_traces.png`
- Leaderboard CSV: `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard/data/field_method_validation_leaderboard.csv`

## Marathon status
The marathon request is still active; continue with a true-3D reference route rather than forcing full-3D claims onto the current Fast-GPR backend.

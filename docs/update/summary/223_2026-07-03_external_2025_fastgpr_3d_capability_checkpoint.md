# External 2025 Fast-GPR 3D Capability Checkpoint

## What Changed

- Generated Fast-GPR full-3D capability audit artifact `263_external_2025_fastgpr_3d_capability_audit`.
- Audited the compiled Fast-GPR-FWI `compute.py` from artifact `261`.
- Added the capability audit to the field-method leaderboard.

## Key Numbers

- Capability checks: `6`.
- Passed checks: `2`.
- Failed checks: `4`.
- Passed:
  - `compute_signature_accepts_nz`.
  - `field_arrays_allocate_3d`.
- Failed:
  - `initialization_labels_mode_2d_tmz`.
  - `initialization_keeps_z_pml`.
  - `dt_uses_three_spatial_dimensions`.
  - `example_uses_single_z_slice`.
- Leaderboard evidence score for this capability audit row: `1`.

## Current Decision

Decision string:

`external_2025_fastgpr_backend_compiled_import_ready_but_2d_tmz_default`

Interpretation: Fast-GPR-FWI is compiled and importable, but the code audit shows the default backend is 2D/2.5D-like, not a safely claimable full-3D backend. It can be used now for accelerated 2D/2.5D IFWI-style work. For true `x,y,z,radius,length,epsr` inversion, we need to patch/test z-dimension semantics or use another true 3D FDTD backend.

## What Remains Blocked

- Do not claim Fast-GPR-FWI gives full 3D y-position or rebar length prediction yet.
- The backend disables z PML in initialization and computes dt from dx/dy only.
- The published example uses a singleton z dimension.

## Validation

- `python -m py_compile run_external_2025_fastgpr_3d_capability_audit.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_external_2025_fastgpr_3d_capability_audit.py -q`
- Result: `2 passed in 0.31s`.
- `python -m py_compile run_field_method_validation_leaderboard.py run_external_2025_fastgpr_3d_capability_audit.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_method_validation_leaderboard.py tests/test_external_2025_fastgpr_3d_capability_audit.py -q`
- Result: `26 passed in 0.44s`.
- `git diff --check -- run_external_2025_fastgpr_field_interface_map.py tests/test_external_2025_fastgpr_field_interface_map.py run_external_2025_fastgpr_3d_capability_audit.py tests/test_external_2025_fastgpr_3d_capability_audit.py run_field_method_validation_leaderboard.py tests/test_field_method_validation_leaderboard.py docs/update/summary/222_2026-07-03_external_2025_fastgpr_field_interface_checkpoint.md`
- Capability audit figure: `1804x835`, nonblank RGB channel extrema.
- Leaderboard figure validation status: `ok`.

## Artifact Paths

- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/263_external_2025_fastgpr_3d_capability_audit`
- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/263_external_2025_fastgpr_3d_capability_audit/data/external_2025_fastgpr_3d_capability_audit_rows.csv`
- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/263_external_2025_fastgpr_3d_capability_audit/data/external_2025_fastgpr_3d_capability_audit_summary.json`
- `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard`

## Next Defensible Task

Fork the compiled Fast-GPR-FWI copy into a guarded field-backend adapter branch and patch only the z-dimension semantics needed for a real 3D smoke: 3D CFL using dx/dy/dz, keep z PML enabled, and run a minimal backend shape smoke before any inversion claim. In parallel, keep using the compiled backend as a fast 2D/2.5D optimizer.

## Marathon Status

The requested real-field-data marathon is still active.

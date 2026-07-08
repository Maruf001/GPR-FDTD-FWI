# External 2025 Fast-GPR 3D Semantics Patch Checkpoint

## What changed
- Created an isolated patched copy of the Fast-GPR-FWI source under artifact `265`.
- Patched Python initialization semantics for 3D smoke readiness:
  - CFL stability expression now includes `dz`.
  - Backend mode label no longer says `2D TMz`.
  - z-boundary PML is no longer disabled by default in the patched copy.
- Added focused tests for duplicate mode/z-PML occurrences so the patch cannot silently leave one backend branch unpatched.
- Added the patched Fast-GPR row to the field-method validation leaderboard.

## Key numbers
- Artifact: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/265_external_2025_fastgpr_3d_semantics_patch`
- Patches applied: `6`
- Patched backend import: `true`
- Post-patch failed checks: `1`
- Remaining failed check: `example_uses_single_z_slice`
- Leaderboard evidence score: `1` diagnostic, not a prediction claim

## What remains blocked
- The bundled Fast-GPR example still uses `nz=1`, so it is not a full-3D example.
- This checkpoint does not validate a non-singleton-z forward solve.
- No 3D inversion or y/length prediction is claimed yet.

## Current decision
`external_2025_fastgpr_3d_semantics_patch_import_ready_audit_improved`

The Fast-GPR path is now patched enough to attempt a small non-singleton-z forward smoke, but it is not yet a validated 3D field-data inversion backend.

## Next defensible task
Run a tiny patched Fast-GPR forward smoke with `nz > 1`, minimal source/receiver geometry, and explicit runtime/memory reporting. If that passes, connect the field-seeded 3D parameter contract to the patched backend.

## Validation/resource checks
- `python -m py_compile run_external_2025_fastgpr_3d_semantics_patch.py run_field_method_validation_leaderboard.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_external_2025_fastgpr_3d_semantics_patch.py tests/test_field_method_validation_leaderboard.py -q`
- Result: `26 passed`
- Leaderboard regenerated at `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard`

## Artifact paths
- Patch summary: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/265_external_2025_fastgpr_3d_semantics_patch/data/external_2025_fastgpr_3d_semantics_patch_summary.json`
- Patch audit rows: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/265_external_2025_fastgpr_3d_semantics_patch/data/external_2025_fastgpr_3d_semantics_patch_audit_rows.csv`
- Patched source root: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/265_external_2025_fastgpr_3d_semantics_patch/patched/Fast-GPR-FWI-main`
- Leaderboard CSV: `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard/data/field_method_validation_leaderboard.csv`

## Marathon status
The marathon request is still active; continue to the patched non-singleton-z Fast-GPR smoke next.

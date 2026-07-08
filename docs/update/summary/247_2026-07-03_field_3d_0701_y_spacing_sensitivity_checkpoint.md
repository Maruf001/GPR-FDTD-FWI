# 247 2026-07-03 Field 3D 0701 Y-Spacing Sensitivity Checkpoint

## What Changed

- Added `run_field_3d_0701_y_spacing_sensitivity_contract.py`.
- Added focused tests in `tests/test_field_3d_0701_y_spacing_sensitivity_contract.py`.
- Generated artifact `outputs/validation_exp_on_field_data/3d_geometry_inventory/005_field_3d_0701_y_spacing_sensitivity_contract/`.
- Snapshotted the exact run script inside the artifact `scripts/` folder with SHA-256 manifest.

## Key Numbers

- 0701 grid contract input: 2 row IDs, 20 column IDs, 38 present profiles, 2 missing cells.
- Assumed y-spacing values tested: `0.0256 m`, `0.05 m`, `0.10 m`, `0.20 m`.
- Resulting two-row y extents: `0.0256 m`, `0.05 m`, `0.10 m`, `0.20 m`.
- X trace spacing remains `0.0256 m`.
- Profile length range remains `18.9002-19.1815 m`.

## Current Decision

`field_3d_0701_y_spacing_sensitivity_ready_not_measured`

The 0701 grid can now be used for sensitivity/benchmark planning under explicit
assumed row spacings. These assumptions do not replace measured row spacing and
cannot support a final y-position or rebar-length field claim.

## What Remains Blocked

- Final `y_m` and `length_y_m` claims remain blocked until row spacing and row
  order direction are measured or recovered from external metadata.
- 3D inversion is ready for a conditional benchmark contract, not a measured
  geometry claim.

## Validation

- `conda run -n gpr-fdtd-fwi python -m py_compile run_field_3d_0701_y_spacing_sensitivity_contract.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_y_spacing_sensitivity_contract.py -q`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_survey_geometry_inventory.py tests/test_field_3d_rad_grid_metadata_audit.py tests/test_field_3d_0701_grid_contract.py tests/test_field_3d_0701_rd3_intake_preview.py tests/test_field_3d_0701_y_spacing_sensitivity_contract.py -q`
- Focused 3D geometry result: `15 passed`.
- Figure check: `field_3d_0701_y_spacing_sensitivity.png` is `1379 x 801` PNG.

## Artifact Paths

- Summary: `outputs/validation_exp_on_field_data/3d_geometry_inventory/005_field_3d_0701_y_spacing_sensitivity_contract/data/field_3d_0701_y_spacing_sensitivity_summary.json`
- Rows: `outputs/validation_exp_on_field_data/3d_geometry_inventory/005_field_3d_0701_y_spacing_sensitivity_contract/data/field_3d_0701_y_spacing_sensitivity_rows.csv`
- Figure: `outputs/validation_exp_on_field_data/3d_geometry_inventory/005_field_3d_0701_y_spacing_sensitivity_contract/figures/field_3d_0701_y_spacing_sensitivity.png`

## Next Defensible Task

Build a 0701 RD3 stack manifest/preview that links profile row/column IDs,
RAD-derived x geometry, assumed y-spacing labels, and waveform array paths. This
is the input contract needed before attempting a conditional 3D x/y/z/radius/
length/epsr optimizer or Fast-GPR/JAX acceleration benchmark.

## Marathon Status

The local field-data marathon remains active; this is a checkpoint, not a stop.

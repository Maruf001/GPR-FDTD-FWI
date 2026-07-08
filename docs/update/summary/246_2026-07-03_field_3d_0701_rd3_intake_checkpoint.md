# Field 3D 0701 RD3 Intake Checkpoint

## What changed

- Added `run_field_3d_0701_rd3_intake_preview.py`.
- Added tests in `tests/test_field_3d_0701_rd3_intake_preview.py`.
- Loaded selected `0701` RD3 files directly from `data/2025-01-13_GPR_Dataset/Data Set.zip`.
- Used RAD metadata for samples, trace count, distance interval, and profile length.
- Generated artifact:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/004_field_3d_0701_rd3_intake_preview`

## Key numbers

- Decision: `field_3d_0701_rd3_intake_numeric_bscans_ready`.
- Loaded profiles:
  - `row01_col0001`: 481 samples x 750 traces, stop position 19.156 m, RMS 427.87.
  - `row01_col0002`: 494 samples x 751 traces, stop position 19.1815 m, RMS 498.75.
  - `row02_col0001`: 481 samples x 750 traces, stop position 19.156 m, RMS 396.55.
  - `row02_col0002`: 481 samples x 751 traces, stop position 19.1815 m, RMS 396.50.
- x trace spacing: 0.0256 m for all loaded profiles.
- RD3 numeric type used: little-endian int16 reshaped to samples x traces.
- All loaded arrays finite.

## What remains blocked

- y spacing is still unresolved, so these profiles can be stacked only under an explicit y-spacing assumption.
- This intake verifies B-scan loading, not yet 3D inversion.

## Current decision

The 0701 grid is now usable as numeric B-scan input for a 3D benchmark stack. The remaining blocker for y/length claims is not file decoding; it is the missing y spacing/field geometry.

## Next defensible task

- Build a small 0701 stack manifest using the loaded profiles and the grid contract.
- Add y-spacing sensitivity values as explicit assumptions, then run a tiny 3D forward benchmark against a cropped subset.

## Validation/resource checks

- `/home/lam002/miniforge3/bin/python -m py_compile run_field_3d_0701_rd3_intake_preview.py`
- `/home/lam002/miniforge3/bin/python -m pytest tests/test_field_3d_0701_rd3_intake_preview.py -q` -> 3 passed.
- RD3 intake command completed -> artifact 004.
- `/home/lam002/miniforge3/bin/python -m pytest tests/test_field_3d_0701_rd3_intake_preview.py tests/test_field_3d_0701_grid_contract.py tests/test_field_3d_rad_grid_metadata_audit.py tests/test_field_3d_survey_geometry_inventory.py -q` -> 12 passed.
- `git diff --check` passed for touched 3D intake/contract files and checkpoint docs.
- Figure metadata: 2943 x 835 RGBA.

## Artifact paths

- Summary: `outputs/validation_exp_on_field_data/3d_geometry_inventory/004_field_3d_0701_rd3_intake_preview/data/field_3d_0701_rd3_intake_summary.json`
- Rows CSV: `outputs/validation_exp_on_field_data/3d_geometry_inventory/004_field_3d_0701_rd3_intake_preview/data/field_3d_0701_rd3_intake_rows.csv`
- Arrays NPZ: `outputs/validation_exp_on_field_data/3d_geometry_inventory/004_field_3d_0701_rd3_intake_preview/data/field_3d_0701_rd3_intake_arrays.npz`
- Figure: `outputs/validation_exp_on_field_data/3d_geometry_inventory/004_field_3d_0701_rd3_intake_preview/figures/field_3d_0701_rd3_intake_preview.png`

## Marathon status

The requested active-session marathon remains active; this is a checkpoint, not a stop.

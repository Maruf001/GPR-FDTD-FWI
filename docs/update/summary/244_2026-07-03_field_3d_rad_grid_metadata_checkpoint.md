# Field 3D RAD Grid Metadata Checkpoint

## What changed

- Added `run_field_3d_rad_grid_metadata_audit.py`.
- Added tests in `tests/test_field_3d_rad_grid_metadata_audit.py`.
- Parsed RAD headers inside `data/2025-01-13_GPR_Dataset/Data Set.zip` for the three candidate grid groups found by the 3D inventory:
  - `Data Set/pipe/0701/ASCII_707-01/ASCII`
  - `Data Set/pipe/0704`
  - `Data Set/pipe/0806`
- Generated artifact:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/002_field_3d_rad_grid_metadata_audit`

## Key numbers

- Decision: `field_3d_rad_grid_x_sampling_known_y_spacing_missing`.
- `Data Set/pipe/0701/ASCII_707-01/ASCII`:
  - 38 RAD/RD3 profiles.
  - LA row IDs: 01 and 02.
  - Column range: 0001-0020.
  - Distance interval: 0.0256 m.
  - Stop-position range: 18.9002-19.1815 m.
  - Samples: 479-499.
- `Data Set/pipe/0704`:
  - 15 RAD/RD3 profiles.
  - LA row IDs: 01 and 02.
  - Column range: 0001-0010.
  - Distance interval: 0.0256 m.
  - Stop-position range: 5.7033-9.7954 m.
  - Samples: 484-486.
- `Data Set/pipe/0806`:
  - 8 RAD/RD3 profiles.
  - LA row IDs: 01 and 02.
  - Column range: 0002-0020.
  - Distance interval: 0.0256 m.
  - Stop-position range: 23.0434-53.5549 m.
  - Samples: 486-512.

## What remains blocked

- RAD headers provide x trace spacing, profile length, samples, time window, and nominal frequency.
- RAD headers do not provide row-to-row y spacing for the inspected groups.
- A true x/y/z/radius/length inversion needs either extracted y spacing from other metadata/field notes or an explicit declared grid-spacing contract.

## Current decision

The best 3D candidate is still `pipe/0701/ASCII_707-01/ASCII`, because it has the most regular grid-like acquisition: two row IDs, up to 20 columns, 38 profile files, and consistent 0.0256 m x trace spacing. It is not yet 3D-inversion-ready because y spacing is unresolved.

## Next defensible task

- Build a 3D data contract file for the `0701` grid with explicit required fields:
  - x trace spacing from RAD: 0.0256 m.
  - y row/line spacing: required external parameter.
  - row/column naming rules.
  - profile selection and missing-column handling.
- Then run a small 3D forward/optimizer benchmark with y spacing as a declared sensitivity parameter, not a hidden assumption.

## Validation/resource checks

- `/home/lam002/miniforge3/bin/python -m py_compile run_field_3d_rad_grid_metadata_audit.py`
- `/home/lam002/miniforge3/bin/python -m pytest tests/test_field_3d_rad_grid_metadata_audit.py -q` -> 3 passed.
- RAD metadata command completed -> artifact 002.
- `/home/lam002/miniforge3/bin/python -m pytest tests/test_field_3d_rad_grid_metadata_audit.py tests/test_field_3d_survey_geometry_inventory.py -q` -> 6 passed.
- `git diff --check` passed for touched 3D inventory files and checkpoint docs.
- Figure metadata: 1974 x 801 RGBA.

## Artifact paths

- Summary: `outputs/validation_exp_on_field_data/3d_geometry_inventory/002_field_3d_rad_grid_metadata_audit/data/field_3d_rad_grid_metadata_summary.json`
- RAD rows: `outputs/validation_exp_on_field_data/3d_geometry_inventory/002_field_3d_rad_grid_metadata_audit/data/field_3d_rad_grid_metadata_rows.csv`
- Group rows: `outputs/validation_exp_on_field_data/3d_geometry_inventory/002_field_3d_rad_grid_metadata_audit/data/field_3d_rad_grid_metadata_group_rows.csv`
- Figure: `outputs/validation_exp_on_field_data/3d_geometry_inventory/002_field_3d_rad_grid_metadata_audit/figures/field_3d_rad_grid_metadata_audit.png`

## Marathon status

The requested active-session marathon remains active; this is a checkpoint, not a stop.

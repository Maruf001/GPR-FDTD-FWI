# Field 3D 0701 Grid Contract Checkpoint

## What changed

- Added `run_field_3d_0701_grid_contract.py`.
- Added tests in `tests/test_field_3d_0701_grid_contract.py`.
- Built an explicit 3D grid contract for:
  - `Data Set/pipe/0701/ASCII_707-01/ASCII`
- Generated artifact:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/003_field_3d_0701_grid_contract`

## Key numbers

- Decision: `field_3d_0701_grid_contract_ready_except_y_spacing`.
- Known geometry:
  - Row IDs: 01, 02.
  - Column IDs: 0001-0020.
  - Present profiles: 38.
  - Expected full grid profile count: 40.
  - Missing cells:
    - row 01, column 0003.
    - row 02, column 0007.
  - x trace spacing: 0.0256 m.
  - x trace spacing uniform: true.
  - profile length range: 18.9002-19.1815 m.
  - samples range: 479-499.
- Required external geometry:
  - `y_spacing_m` is required before a 3D length/y-location claim.
  - row and column order direction must be explicitly declared or intentionally assumed.

## What remains blocked

- y spacing is still not encoded in the local RAD headers.
- Without y spacing, the project can report x/z/radius/epsr per profile but cannot honestly report y location or rebar length from this grid.
- A 3D optimizer can be benchmarked only as a sensitivity run with declared y-spacing hypotheses, not as a final field claim.

## Current decision

The 0701 grid is ready as a structured 3D data contract except for y spacing. This is now a concrete bridge from the earlier 2D field fits to a true 3D x/y/z/radius/length formulation, but the y axis must be supplied explicitly.

## Next defensible task

- Build a small 3D benchmark configuration using the 0701 contract with y-spacing sensitivity values, clearly marked as assumptions.
- Or, if field notes can supply row spacing, replace the sensitivity values with the measured spacing and promote the contract.

## Validation/resource checks

- `/home/lam002/miniforge3/bin/python -m py_compile run_field_3d_0701_grid_contract.py`
- `/home/lam002/miniforge3/bin/python -m pytest tests/test_field_3d_0701_grid_contract.py -q` -> 3 passed.
- Grid contract command completed -> artifact 003.
- `/home/lam002/miniforge3/bin/python -m pytest tests/test_field_3d_0701_grid_contract.py tests/test_field_3d_rad_grid_metadata_audit.py tests/test_field_3d_survey_geometry_inventory.py -q` -> 9 passed.
- `git diff --check` passed for touched 3D contract and metadata files.
- Figure metadata: 1804 x 631 RGBA.

## Artifact paths

- Contract JSON: `outputs/validation_exp_on_field_data/3d_geometry_inventory/003_field_3d_0701_grid_contract/data/field_3d_0701_grid_contract.json`
- Grid profiles CSV: `outputs/validation_exp_on_field_data/3d_geometry_inventory/003_field_3d_0701_grid_contract/data/field_3d_0701_grid_profiles.csv`
- Missing cells CSV: `outputs/validation_exp_on_field_data/3d_geometry_inventory/003_field_3d_0701_grid_contract/data/field_3d_0701_missing_cells.csv`
- Figure: `outputs/validation_exp_on_field_data/3d_geometry_inventory/003_field_3d_0701_grid_contract/figures/field_3d_0701_grid_contract.png`

## Marathon status

The requested active-session marathon remains active; this is a checkpoint, not a stop.

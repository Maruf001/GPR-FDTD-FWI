# Field 3D Survey Geometry Inventory Checkpoint

## What changed

- Added `run_field_3d_survey_geometry_inventory.py`.
- Added tests in `tests/test_field_3d_survey_geometry_inventory.py`.
- Parsed local GSSI DZX metadata for `data/2026-06-09_GSSI_model_51600S`.
- Inventoried the zipped `data/2025-01-13_GPR_Dataset/Data Set.zip` without bulk extraction.
- Generated artifact:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/001_field_3d_survey_geometry_inventory`

## Key numbers

- Decision: `field_3d_geometry_inventory_candidate_grids_found_spacing_unresolved`.
- GSSI model 51600S profiles:
  - Four DZT/DZX profile pairs.
  - Sampling: 300 scans/m, 512 samples/scan, depth range 0.45 m, dielectric metadata 2.25.
  - Profile lengths:
    - `PROJECT001C__013`: 2.69 m.
    - `PROJECT001C__014`: 0.913 m.
    - `PROJECT001C__015`: 2.713 m.
    - `PROJECT001C__016`: 0.913 m.
  - DZX does not provide explicit profile-to-profile y spacing.
- 2025 ZIP inventory:
  - 212 profile groups found.
  - Three RAD/RD3 candidate grid groups found:
    - `Data Set/pipe/0701/ASCII_707-01/ASCII`: 38 RD3/RAD profiles, LA rows 01 and 02, columns 0001-0020.
    - `Data Set/pipe/0704`: 15 RD3/RAD profiles, LA rows 01 and 02, columns 0001-0010.
    - `Data Set/pipe/0806`: 8 RD3/RAD profiles, LA rows 01 and 02, columns 0002-0020.

## What remains blocked

- The local GSSI 51600S field profiles support 2D/adjacent-profile analysis but do not currently provide explicit y spacing in the DZX metadata.
- The 2025 RAD/RD3 groups look like better 3D candidates, but y spacing and grid geometry must be extracted from RAD metadata or field notes before claiming y-position or rebar length.
- 3D inversion should not be launched on these data until the survey geometry contract is explicit.

## Current decision

The best immediate 3D target is the 2025 dataset RAD/RD3 grid-like groups, especially `pipe/0701/ASCII_707-01/ASCII`. For the current GSSI 51600S data, x/z/radius/epsr fitting is defensible, but y-position and length remain underdetermined without profile spacing.

## Next defensible task

- Extract RAD metadata for the candidate grid groups to find trace spacing, time sampling, antenna settings, and possible line spacing.
- If RAD does not encode y spacing, create a required field-note parameter in the 3D data contract instead of silently assuming spacing.
- Then build a small 3D forward/optimizer benchmark on the candidate grid data.

## Validation/resource checks

- `/home/lam002/miniforge3/bin/python -m py_compile run_field_3d_survey_geometry_inventory.py`
- `/home/lam002/miniforge3/bin/python -m pytest tests/test_field_3d_survey_geometry_inventory.py -q` -> 3 passed.
- Inventory command completed -> artifact 001.
- `/home/lam002/miniforge3/bin/python -m pytest tests/test_field_3d_survey_geometry_inventory.py tests/test_external_2025_190424aa_event_window_waveform_audit.py tests/test_field_method_validation_leaderboard.py -q` -> 42 passed.
- `git diff --check` passed for the touched 3D inventory, audit, leaderboard, and checkpoint files.
- Figure metadata: 2229 x 835 RGBA.

## Artifact paths

- Summary: `outputs/validation_exp_on_field_data/3d_geometry_inventory/001_field_3d_survey_geometry_inventory/data/field_3d_survey_geometry_inventory_summary.json`
- GSSI profile CSV: `outputs/validation_exp_on_field_data/3d_geometry_inventory/001_field_3d_survey_geometry_inventory/data/field_3d_gssi_dzx_profiles.csv`
- 2025 ZIP profile-group CSV: `outputs/validation_exp_on_field_data/3d_geometry_inventory/001_field_3d_survey_geometry_inventory/data/field_3d_2025_zip_profile_groups.csv`
- Figure: `outputs/validation_exp_on_field_data/3d_geometry_inventory/001_field_3d_survey_geometry_inventory/figures/field_3d_survey_geometry_inventory.png`

## Marathon status

The requested active-session marathon remains active; this is a checkpoint, not a stop.

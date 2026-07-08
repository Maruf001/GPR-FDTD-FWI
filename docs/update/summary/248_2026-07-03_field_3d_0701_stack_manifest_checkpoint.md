# 248 2026-07-03 Field 3D 0701 Stack Manifest Checkpoint

## What Changed

- Added `run_field_3d_0701_stack_manifest.py`.
- Added focused tests in `tests/test_field_3d_0701_stack_manifest.py`.
- Generated corrected artifact `outputs/validation_exp_on_field_data/3d_geometry_inventory/007_field_3d_0701_stack_manifest/`.
- The earlier `006_field_3d_0701_stack_manifest/` artifact is superseded by `007` because the assumption-label order was corrected and regenerated.
- Snapshotted the exact stack script and parser dependencies inside the artifact `scripts/` folder.

## Key Numbers

- Loaded 38 0701 RAD/RD3 profiles.
- Cropped common normalized stack shape: `38 x 479 x 740` as profile/sample/trace.
- Manifest rows: 152, from 38 profiles across four explicit y-spacing assumptions.
- Y-spacing assumptions: `26 mm`, `50 mm`, `100 mm`, `200 mm`.
- Time-sample interval range: `0.390624948-0.390625103 ns`.
- Saved normalized stack size: `11 MB`.
- Figure: `field_3d_0701_stack_manifest.png`, `2058 x 835` PNG.

## Current Decision

`field_3d_0701_stack_manifest_ready_for_conditional_3d_benchmark`

The 0701 field data now has a numeric multi-profile stack artifact suitable for
conditional 3D benchmark design. The stack links profile labels, RAD/RD3 file
paths, x trace spacing, raw profile dimensions, normalized cropped waveforms,
row/column IDs, and explicit assumed y-spacing labels.

## Claim Boundary

The y coordinates in this artifact are assumptions, not measured survey
geometry. It can support benchmark/runtime/optimizer development and conditional
3D sensitivity, but final `y_m` or `length_y_m` claims still require measured
profile spacing and row/column order metadata.

## Validation

- `conda run -n gpr-fdtd-fwi python -m py_compile run_field_3d_0701_stack_manifest.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_stack_manifest.py -q`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_survey_geometry_inventory.py tests/test_field_3d_rad_grid_metadata_audit.py tests/test_field_3d_0701_grid_contract.py tests/test_field_3d_0701_rd3_intake_preview.py tests/test_field_3d_0701_y_spacing_sensitivity_contract.py tests/test_field_3d_0701_stack_manifest.py -q`
- Focused 3D geometry/stack result: `21 passed`.
- `git diff --check -- run_field_3d_0701_stack_manifest.py tests/test_field_3d_0701_stack_manifest.py`

## Artifact Paths

- Summary: `outputs/validation_exp_on_field_data/3d_geometry_inventory/007_field_3d_0701_stack_manifest/data/field_3d_0701_stack_manifest_summary.json`
- Manifest rows: `outputs/validation_exp_on_field_data/3d_geometry_inventory/007_field_3d_0701_stack_manifest/data/field_3d_0701_stack_manifest_rows.csv`
- Stack: `outputs/validation_exp_on_field_data/3d_geometry_inventory/007_field_3d_0701_stack_manifest/data/field_3d_0701_stack_normalized_crop.npz`
- Figure: `outputs/validation_exp_on_field_data/3d_geometry_inventory/007_field_3d_0701_stack_manifest/figures/field_3d_0701_stack_manifest.png`

## Next Defensible Task

Build an acceleration benchmark contract using this stack as the field-data
input: compare the current NumPy/PyTorch intake path, available Fast-GPR-FWI
repo capabilities, CUDA availability, and a small JAX/JIT smoke if the local
environment supports it. The goal is to choose the engine for conditional 3D
FWI-style x/y/z/radius/length/epsr fitting.

## Marathon Status

The local field-data marathon remains active; this is a checkpoint, not a stop.

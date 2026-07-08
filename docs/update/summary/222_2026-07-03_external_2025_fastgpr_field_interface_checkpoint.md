# External 2025 Fast-GPR Field Interface Checkpoint

## What Changed

- Generated Fast-GPR field interface map artifact `262_external_2025_fastgpr_field_interface_map`.
- Confirmed the compiled Fast-GPR-FWI backend from artifact `261` imports cleanly from Python.
- Captured the backend `compute(...)` signature and mapped its required arguments to the real `190424AA_LID10002` field-data window.
- Added a leaderboard diagnostic row for the interface map.

## Key Numbers

- Compiled backend import: `true`.
- Estimated first smoke grid shape, Fast-GPR order `ny,nx,nz`: `151,39,59`.
- Estimated grid cells: `347451`.
- Grid spacing for first smoke: `0.004 m`.
- Blocked Fast-GPR arguments: `0`.
- Tensor-builder arguments still needed: `6`.
- Acquisition-lock arguments still needed: `2`.
- First field-seeded forward-smoke interface ready: `true`.
- Leaderboard evidence score for this interface row: `1`.

## Current Decision

Decision string:

`external_2025_fastgpr_field_interface_import_ready_tensor_builder_next`

Interpretation: Fast-GPR-FWI is compiled, importable, and mapped to the real field-data window. The next work is not another paper-reading or synthetic gate; it is a tensor builder for `er/se/mr`, source/receiver locations, wavelet/source amplitudes, and the first field-seeded 3D forward smoke.

## What Remains Blocked

- No 3D forward model or inversion has run yet.
- The tensor builder still needs to construct `er`, `se`, `mr`, `source`, `source_apmlitudes`, `step`, and source locations from the measured wavelet and field scan geometry.
- Receiver/source acquisition geometry still needs a lock: whether to treat the field profile as collocated, bistatic with offset, or use a measured antenna-offset estimate.

## Validation

- `python -m py_compile run_external_2025_fastgpr_field_interface_map.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_external_2025_fastgpr_field_interface_map.py -q`
- Result: `3 passed in 0.33s`.
- `python -m py_compile run_field_method_validation_leaderboard.py run_external_2025_fastgpr_field_interface_map.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_method_validation_leaderboard.py tests/test_external_2025_fastgpr_field_interface_map.py -q`
- Result: `26 passed in 0.44s`.
- `git diff --check -- run_external_2025_fastgpr_field_interface_map.py tests/test_external_2025_fastgpr_field_interface_map.py run_field_method_validation_leaderboard.py tests/test_field_method_validation_leaderboard.py docs/update/summary/221_2026-07-03_external_2025_3d_geometry_acceleration_bridge_checkpoint.md`
- Interface grid figure: `1243x784`, nonblank RGB channel extrema.
- Leaderboard figure validation status: `ok`.

## Artifact Paths

- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/262_external_2025_fastgpr_field_interface_map`
- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/262_external_2025_fastgpr_field_interface_map/data/external_2025_fastgpr_field_interface_mapping.csv`
- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/262_external_2025_fastgpr_field_interface_map/data/external_2025_fastgpr_import_probe.json`
- `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard`

## Next Defensible Task

Implement the field-seeded Fast-GPR tensor builder for the first 3D forward smoke: construct the `er/se/mr` volume from the `x,y,z,radius,length,epsr,sigma` contract, load the measured wavelet, build source/receiver tensors for the 14-shot event window, and run a minimal forward pass or produce a precise blocker if the backend API requires an additional shape convention.

## Marathon Status

The requested real-field-data marathon is still active.

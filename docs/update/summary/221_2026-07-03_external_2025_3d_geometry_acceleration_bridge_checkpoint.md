# External 2025 3D Geometry Acceleration Bridge Checkpoint

## What Changed

- Generated field-seeded 3D geometry/acceleration bridge artifact `261_external_2025_3d_geometry_acceleration_bridge`.
- Seeded the 3D contract from the real `190424AA_LID10002` radius/epsr candidate artifact `260`.
- Extracted `paper/accelerator/Fast-GPR-FWI-main.zip` inside the artifact and successfully compiled the CUDA kernels with `make clean all`.
- Added a leaderboard diagnostic row for the 3D bridge.

## Key Numbers

- Seed source: `external_2025_190424aa_radius_epsr_candidate_top16mm_range8to24mm`.
- 2D seed diameter: `16.00 mm`.
- 2D seed epsr: `3.9855180978775024`.
- 2D near-best diameter range: `8.00-24.00 mm`.
- 3D parameter contract rows: `9`.
- Fast-GPR-FWI compiled libraries: `6/6`.
- CUDA build prerequisites ready: `true`.
- JAX CUDA ready: `true`.
- Leaderboard evidence score for this bridge row: `1`.

## 3D Contract

The generated parameter contract includes:

- `x_center_m`: seeded at `0.13384640216827393`.
- `y_center_m`: seeded at `0.0`, but explicitly marked not identified from a single B-scan profile.
- `cover_depth_z_m`: seeded at `0.093923419713974`.
- `radius_m`: seeded at `0.008`, range `0.003999999761581421-0.012`.
- `length_y_m`: seeded at `0.50`, range `0.05-1.50`, explicitly marked as a 3D-only parameter not identified by the current 2D model.
- `concrete_epsr`: seeded at `3.9855180978775024`, near-best range `3.9718658924102783-3.9855180978775024`.
- `concrete_sigma_s_m`, `source_delay_ns`, and `time_shift_ns` are seeded from the current best 2D field fits.

## Current Decision

Decision string:

`external_2025_3d_geometry_acceleration_bridge_fastgpr_build_ready_field_seeded`

Interpretation: the local machine and artifact copy of Fast-GPR-FWI are ready for a field-seeded accelerated 3D forward/inversion branch. This is not yet a 3D prediction. It only closes the bridge from the current real 2D candidate to a concrete 3D parameter contract and compiled CUDA backend.

## What Remains Blocked

- No `y` location, rebar length, or full 3D shape has been predicted yet.
- A single B-scan profile alone cannot uniquely determine `y_center_m` or `length_y_m`; the next branch must either use multiple profiles or explicitly regularize those parameters.
- The Fast-GPR-FWI backend is compiled, but it has not yet been adapted to this field-data acquisition geometry.

## Validation

- `python -m py_compile run_external_2025_3d_geometry_acceleration_bridge.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_external_2025_3d_geometry_acceleration_bridge.py -q`
- Result: `3 passed in 0.33s`.
- `python -m py_compile run_field_method_validation_leaderboard.py run_external_2025_3d_geometry_acceleration_bridge.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_method_validation_leaderboard.py tests/test_external_2025_3d_geometry_acceleration_bridge.py -q`
- Result: `25 passed in 0.43s`.
- `git diff --check -- run_external_2025_3d_geometry_acceleration_bridge.py tests/test_external_2025_3d_geometry_acceleration_bridge.py run_field_method_validation_leaderboard.py tests/test_field_method_validation_leaderboard.py docs/update/summary/220_2026-07-03_external_2025_190424aa_radius_epsr_candidate_checkpoint.md`
- 3D contract figure: `869x903`, nonblank RGB channel extrema.
- Leaderboard figure: `1575x720`, figure validation status `ok`.

## Artifact Paths

- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/261_external_2025_3d_geometry_acceleration_bridge`
- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/261_external_2025_3d_geometry_acceleration_bridge/data/external_2025_3d_geometry_parameter_contract.csv`
- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/261_external_2025_3d_geometry_acceleration_bridge/data/external_2025_3d_acceleration_backend_preflight.csv`
- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/261_external_2025_3d_geometry_acceleration_bridge/data/external_2025_fast_gpr_fwi_build_summary.json`
- `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard`

## Next Defensible Task

Adapt the compiled Fast-GPR-FWI source/receiver/model interface to the `190424AA_LID10002` field window: build the first field-seeded 3D forward smoke that uses the measured wavelet, the 2D-derived `x/z/radius/epsr` seed, and explicit `y/length` parameters. The output should be runtime plus waveform mismatch, not a synthetic validation claim.

## Marathon Status

The requested real-field-data marathon is still active.

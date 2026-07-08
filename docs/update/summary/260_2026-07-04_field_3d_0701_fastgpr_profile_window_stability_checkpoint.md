# 260 2026-07-04 Field 3D 0701 Fast-GPR Profile-Window Stability Checkpoint

## What Changed

- Added `profile_start` support to the local field-window extractor.
- Added `run_field_3d_0701_fastgpr_profile_window_transfer_ladder.py`.
- Scanned the aligned Fast-GPR prediction across overlapping 4-profile windows in the 0701 stack.
- Re-ran the rebar-scale conductivity optimizer on the best transfer window, profiles `2-5`.
- Regenerated the predictor scorecard with the profile `2-5` candidate.

## Key Artifacts

- Transfer scan: `outputs/validation_exp_on_field_data/3d_geometry_inventory/029_field_3d_0701_fastgpr_profile_window_transfer_ladder/`
- Profile `2-5` rebar-scale conductivity optimizer: `outputs/validation_exp_on_field_data/3d_geometry_inventory/030_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer_rebar_scale_conductivity_profile02/`
- Updated scorecard: `outputs/validation_exp_on_field_data/3d_geometry_inventory/031_field_3d_0701_fastgpr_aligned_predictor_scorecard/`

## Key Numbers

Profile transfer scan `029`:

- windows scanned: `18`
- best profile window: `2-5`
- assumed y range: `0.2-0.5 m` using candidate y spacing `0.1 m`
- best fixed-prediction loss: `0.737877`
- original profile `0-3` fixed-prediction loss: `0.755577`
- profile `0-3` minus best: `0.017700`
- near-best window count: `1`

Profile `2-5` optimizer `030`:

- best loss: `0.732343`
- initial loss: `0.735405`
- best epsr: `4.708607`
- background conductivity: `0.008067 S/m`
- anomaly conductivity: `0.050000 S/m`
- depth: `1.507812 m`
- diameter proxy: `30.0 mm`
- mean runtime: `0.267 s/iter`

Updated scorecard `031` candidate:

- x: `9.665786 m`
- cover/depth z: `1.507821 m`
- best profile window: `2-5`
- assumed y window: `0.2-0.5 m`
- epsr: Fast-GPR profile candidate `4.708607`, analytic event `3.830539`
- background conductivity: `0.008067 S/m`
- anomaly conductivity: `0.050000 S/m`
- supported diameter range: `8-30 mm`
- source shift/polarity: `+1.8 ns`, polarity `-1`

## Current Decision

`field_3d_0701_predictor_candidate_ready_with_diameter_degeneracy_flag`

The y/profile window is now a material part of the predictor. Profiles `2-5`
fit substantially better than the original profile `0-3` window under the same
aligned Fast-GPR prediction, and re-optimizing on profiles `2-5` improves the
best loss to `0.732343`.

## Claim Boundary

This supports a profile-window-scoped 3D candidate, not a universal detector.
The y coordinate remains tied to the assumed stack spacing and profile ordering.
The Fast-GPR anomaly remains a rebar-scale Gaussian proxy rather than a
steel-cylinder FDTD target.

## Next Defensible Task

Re-run the source time/polarity ladder directly on the profile `2-5` window, then
rerun the profile `2-5` conductivity optimizer with that profile-specific
alignment. The current profile `2-5` optimizer still uses the profile `0-3`
alignment (`+1.8 ns`, polarity `-1`).

## Validation

- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_local_window_bridge_smoke.py tests/test_field_3d_0701_fastgpr_local_window_time_polarity_ladder.py tests/test_field_3d_0701_fastgpr_local_window_aligned_scalar_epsr_optimizer.py tests/test_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py tests/test_field_3d_0701_fastgpr_aligned_predictor_scorecard.py tests/test_field_3d_0701_fastgpr_profile_window_transfer_ladder.py -q`
- Result: `20 passed`
- `conda run -n dev python -m pytest tests/test_field_3d_0701_fastgpr_local_window_bridge_smoke.py tests/test_field_3d_0701_fastgpr_local_window_time_polarity_ladder.py tests/test_field_3d_0701_fastgpr_local_window_aligned_scalar_epsr_optimizer.py tests/test_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py tests/test_field_3d_0701_fastgpr_aligned_predictor_scorecard.py tests/test_field_3d_0701_fastgpr_profile_window_transfer_ladder.py -q`
- Result: `20 passed`
- `git diff --check` on the touched scripts, tests, and checkpoint docs
- Figure checks: profile transfer and scorecard figures are nonblank PNGs.

## Marathon Status

The local field-data predictor marathon remains active; this is a checkpoint,
not a stop.

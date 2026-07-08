# 264 2026-07-04 Field 3D 0701 Fast-GPR Smooth-Cylinder Candidate Checkpoint

## What Changed

- Added `--mask-kind smooth_cylinder` to the aligned geometry/material optimizer.
- Ran the current best profile/x window with a differentiable smooth-cylinder rebar cross-section instead of a Gaussian anomaly.
- Updated the predictor scorecard to reference the smooth-cylinder conductivity run.

## Key Artifacts

- Smooth-cylinder optimizer: `outputs/validation_exp_on_field_data/3d_geometry_inventory/044_field_3d_0701_fastgpr_local_window_aligned_smooth_cylinder_rebar_conductivity_profile02_xshift/`
- Updated scorecard: `outputs/validation_exp_on_field_data/3d_geometry_inventory/045_field_3d_0701_fastgpr_aligned_predictor_scorecard/`

## Key Numbers

Smooth-cylinder run `044`:

- field x window center: `9.819386 m`
- profile window: `2-5`
- source shift/polarity: `+2.2 ns`, polarity `+1`
- best loss: `0.724010`
- epsr: `4.819113`
- background conductivity: `0.008443 S/m`
- anomaly conductivity: `0.050000 S/m`
- depth: `1.507663 m`
- radius proxy: `15.000 mm`
- diameter proxy: `30.000 mm`

Comparison to Gaussian rebar-scale run `042`:

- Gaussian best loss: `0.724010`
- Smooth-cylinder best loss: `0.724010`
- Both support the same rebar-scale radius/diameter under this local objective.

Scorecard `045` current candidate:

- x: `9.819386 m`
- analytic-event x: `9.665786 m`
- cover/depth z: `1.507821 m`
- profile window: `2-5`
- assumed y window: `0.2-0.5 m`
- epsr: Fast-GPR `4.819113`, analytic event `3.830539`
- background conductivity: `0.008443 S/m`
- anomaly conductivity: `0.050000 S/m`
- supported diameter range: `8-30 mm`
- source shift/polarity: `+2.2 ns`, polarity `+1`

## Current Decision

`field_3d_0701_predictor_candidate_ready_with_diameter_degeneracy_flag`

The rebar-scale result is no longer only a Gaussian-anomaly artifact. A
differentiable smooth-cylinder cross-section reaches the same local field
objective with the same `30 mm` diameter proxy. This strengthens the current
diameter range support, but does not remove the need to report a range rather
than a unique diameter.

## Claim Boundary

The smooth-cylinder mask is closer to rebar physics than the Gaussian proxy, but
it is still a simplified local Fast-GPR cross-section, not a full 3D
steel-cylinder FDTD inversion with finite length.

## Next Defensible Task

Run the smooth-cylinder candidate over neighboring profile/x windows to test
stability, or add a finite-length 3D cylinder parameterization. The former is a
fast field-data stability test; the latter is the path toward a physical length
claim.

## Validation

- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_local_window_bridge_smoke.py tests/test_field_3d_0701_fastgpr_local_window_time_polarity_ladder.py tests/test_field_3d_0701_fastgpr_local_window_aligned_scalar_epsr_optimizer.py tests/test_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py tests/test_field_3d_0701_fastgpr_aligned_predictor_scorecard.py tests/test_field_3d_0701_fastgpr_profile_window_transfer_ladder.py tests/test_field_3d_0701_fastgpr_x_window_transfer_ladder.py -q`
- Result: `22 passed`
- `conda run -n dev python -m pytest tests/test_field_3d_0701_fastgpr_local_window_bridge_smoke.py tests/test_field_3d_0701_fastgpr_local_window_time_polarity_ladder.py tests/test_field_3d_0701_fastgpr_local_window_aligned_scalar_epsr_optimizer.py tests/test_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py tests/test_field_3d_0701_fastgpr_aligned_predictor_scorecard.py tests/test_field_3d_0701_fastgpr_profile_window_transfer_ladder.py tests/test_field_3d_0701_fastgpr_x_window_transfer_ladder.py -q`
- Result: `22 passed`
- `git diff --check` on touched scripts, tests, and checkpoint docs

## Marathon Status

The local field-data predictor marathon remains active; this is a checkpoint,
not a stop.

# 263 2026-07-04 Field 3D 0701 Fast-GPR X-Window Refinement Checkpoint

## What Changed

- Added `run_field_3d_0701_fastgpr_x_window_transfer_ladder.py`.
- Scanned neighboring x field windows around the analytic event candidate using the profile `2-5`, interior-shift aligned Fast-GPR prediction.
- Added `--x0-m` support to the aligned geometry/material optimizer.
- Re-ran the profile `2-5` rebar-scale conductivity optimizer at the best x transfer window.
- Updated the predictor scorecard so field x comes from the selected field window, while analytic-event x is retained separately.

## Key Artifacts

- X transfer scan: `outputs/validation_exp_on_field_data/3d_geometry_inventory/041_field_3d_0701_fastgpr_x_window_transfer_ladder/`
- X-shifted optimizer: `outputs/validation_exp_on_field_data/3d_geometry_inventory/042_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer_rebar_scale_conductivity_profile02_xshift/`
- Updated scorecard: `outputs/validation_exp_on_field_data/3d_geometry_inventory/043_field_3d_0701_fastgpr_aligned_predictor_scorecard/`

## Key Numbers

X transfer scan `041`:

- scanned trace offsets: `-12..+12` by `2`
- best trace offset: `+6`
- best x: `9.819386 m`
- x delta from analytic-event x: `+0.153600 m`
- best transfer loss: `0.724231`
- original x transfer loss: `0.730782`
- original minus best: `0.006550`
- near-best x range: `9.768186-9.870586 m`

X-shifted optimizer `042`:

- x field window center: `9.819386 m`
- trace window: `369-399`
- profile window: `2-5`
- best loss: `0.724010`
- epsr: `4.819113`
- background conductivity: `0.008443 S/m`
- anomaly conductivity: `0.050000 S/m`
- depth: `1.507820 m`
- diameter proxy: `30.0 mm`

Scorecard `043` current candidate:

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

The best current field-window candidate has moved in x from the analytic event
seed by about `+0.154 m`. This improves the aligned Fast-GPR objective and
should be treated as the current x estimate for the local predictor scorecard,
with the analytic-event x retained as a separate seed/reference.

## Claim Boundary

This remains a local-window, rebar-scale Gaussian-proxy predictor. It now reports
x, y-window, z/depth, epsr, conductivity, and diameter range from real field
data, but not a unique steel-cylinder diameter.

## Next Defensible Task

Run the same x-window transfer/refinement on adjacent profile windows or add a
true steel-cylinder/rebar parameterization in the Fast-GPR grid. The former
tests spatial stability; the latter is required for stronger diameter claims.

## Validation

- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_local_window_bridge_smoke.py tests/test_field_3d_0701_fastgpr_local_window_time_polarity_ladder.py tests/test_field_3d_0701_fastgpr_local_window_aligned_scalar_epsr_optimizer.py tests/test_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py tests/test_field_3d_0701_fastgpr_aligned_predictor_scorecard.py tests/test_field_3d_0701_fastgpr_profile_window_transfer_ladder.py tests/test_field_3d_0701_fastgpr_x_window_transfer_ladder.py -q`
- Result: `22 passed`
- `conda run -n dev python -m pytest tests/test_field_3d_0701_fastgpr_local_window_bridge_smoke.py tests/test_field_3d_0701_fastgpr_local_window_time_polarity_ladder.py tests/test_field_3d_0701_fastgpr_local_window_aligned_scalar_epsr_optimizer.py tests/test_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py tests/test_field_3d_0701_fastgpr_aligned_predictor_scorecard.py tests/test_field_3d_0701_fastgpr_profile_window_transfer_ladder.py tests/test_field_3d_0701_fastgpr_x_window_transfer_ladder.py -q`
- Result: `22 passed`
- `git diff --check` on touched scripts, tests, and checkpoint docs

## Marathon Status

The local field-data predictor marathon remains active; this is a checkpoint,
not a stop.

# 262 2026-07-04 Field 3D 0701 Fast-GPR Interior-Shift Candidate Checkpoint

## What Changed

- Ran a wider 61-sample profile `2-5` alignment sensitivity scan with shifts `-30..+30`.
- Re-ran the profile `2-5` rebar-scale conductivity optimizer using the interior-shift alignment.
- Updated the predictor scorecard to prefer the interior-shift candidate over the lower-loss boundary-shift candidate.

## Key Artifacts

- Interior-shift alignment sensitivity: `outputs/validation_exp_on_field_data/3d_geometry_inventory/038_field_3d_0701_fastgpr_local_window_time_polarity_ladder_profile02_shift30_sensitivity/`
- Interior-shift optimizer: `outputs/validation_exp_on_field_data/3d_geometry_inventory/039_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer_rebar_scale_conductivity_profile02_shift30/`
- Updated scorecard: `outputs/validation_exp_on_field_data/3d_geometry_inventory/040_field_3d_0701_fastgpr_aligned_predictor_scorecard/`

## Key Numbers

Alignment `038`:

- profile window: `2-5`
- time samples: `61`
- shift range: `-30..+30` samples
- best shift: `+22` samples = `+2.2 ns`
- best polarity: `+1`
- fixed overlap: `31` samples
- best alignment loss: `0.730782`
- baseline shift-0 positive loss: `0.801837`

Optimizer `039`:

- best loss: `0.730568`
- epsr: `3.984818`
- background conductivity: `0.005497 S/m`
- anomaly conductivity: `0.050000 S/m`
- depth: `1.507821 m`
- diameter proxy: `30.0 mm`
- mean runtime: `0.214 s/iter`

Scorecard `040` current candidate:

- x: `9.665786 m`
- cover/depth z: `1.507821 m`
- profile window: `2-5`
- assumed y window: `0.2-0.5 m`
- epsr: Fast-GPR `3.984818`, analytic event `3.830539`
- background conductivity: `0.005497 S/m`
- anomaly conductivity: `0.050000 S/m`
- supported diameter range: `8-30 mm`
- source shift/polarity: `+2.2 ns`, polarity `+1`

## Current Decision

`field_3d_0701_predictor_candidate_ready_with_diameter_degeneracy_flag`

The best raw loss remains the edge-shift run `035` (`0.726952`), but the
current scorecard intentionally uses interior-shift run `039` (`0.730568`) as
the more defensible candidate because its alignment is not at the search
boundary.

## Claim Boundary

This is now a real-field, profile-window-scoped predictor candidate with x,
y-window, depth, diameter range, epsr, and conductivity. Diameter remains a
range, not a unique value, because rebar-scale and broad smooth-anomaly fits
remain close under the current proxy physics.

## Next Defensible Task

Repeat the profile-window transfer and interior-shift optimizer on neighboring
candidate x trace windows, or replace the Gaussian anomaly proxy with a
steel-cylinder/rebar parameterization. The latter is needed before claiming an
actual physical diameter rather than a supported range.

## Validation

- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_local_window_bridge_smoke.py tests/test_field_3d_0701_fastgpr_local_window_time_polarity_ladder.py tests/test_field_3d_0701_fastgpr_local_window_aligned_scalar_epsr_optimizer.py tests/test_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py tests/test_field_3d_0701_fastgpr_aligned_predictor_scorecard.py tests/test_field_3d_0701_fastgpr_profile_window_transfer_ladder.py -q`
- Result: `20 passed`
- `conda run -n dev python -m pytest tests/test_field_3d_0701_fastgpr_local_window_bridge_smoke.py tests/test_field_3d_0701_fastgpr_local_window_time_polarity_ladder.py tests/test_field_3d_0701_fastgpr_local_window_aligned_scalar_epsr_optimizer.py tests/test_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py tests/test_field_3d_0701_fastgpr_aligned_predictor_scorecard.py tests/test_field_3d_0701_fastgpr_profile_window_transfer_ladder.py -q`
- Result: `20 passed`
- `git diff --check` on the touched scripts, tests, and checkpoint docs

## Marathon Status

The local field-data predictor marathon remains active; this is a checkpoint,
not a stop.

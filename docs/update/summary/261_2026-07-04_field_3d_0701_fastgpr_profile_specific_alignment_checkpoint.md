# 261 2026-07-04 Field 3D 0701 Fast-GPR Profile-Specific Alignment Checkpoint

## What Changed

- Added `--profile-start` support to the Fast-GPR time/polarity ladder.
- Ran profile `2-5` source time/polarity alignment.
- Re-ran profile `2-5` rebar-scale conductivity optimizer with profile-specific alignments.
- Updated the predictor scorecard so candidate source shift/polarity comes from the selected candidate row, not the older global alignment.

## Key Artifacts

- Profile `2-5`, 61-sample alignment: `outputs/validation_exp_on_field_data/3d_geometry_inventory/032_field_3d_0701_fastgpr_local_window_time_polarity_ladder_wide_profile02/`
- Profile `2-5`, 81-sample wider alignment: `outputs/validation_exp_on_field_data/3d_geometry_inventory/033_field_3d_0701_fastgpr_local_window_time_polarity_ladder_wider_profile02/`
- Profile `2-5`, 81-sample conductivity optimizer: `outputs/validation_exp_on_field_data/3d_geometry_inventory/034_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer_rebar_scale_conductivity_profile02_aligned/`
- Profile `2-5`, 61-sample conductivity optimizer: `outputs/validation_exp_on_field_data/3d_geometry_inventory/035_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer_rebar_scale_conductivity_profile02_aligned61/`
- Corrected scorecard: `outputs/validation_exp_on_field_data/3d_geometry_inventory/037_field_3d_0701_fastgpr_aligned_predictor_scorecard/`

## Key Numbers

Profile `2-5` 61-sample alignment `032`:

- best shift: `+24` samples = `+2.4 ns`
- best polarity: `+1`
- best alignment loss: `0.727103`
- baseline shift-0 positive loss: `0.808933`
- caveat: best shift is at the `+24` search boundary

Profile `2-5` 81-sample wider alignment `033`:

- best shift: `+33` samples = `+3.3 ns`
- best polarity: `+1`
- best alignment loss: `0.749143`
- baseline shift-0 positive loss: `0.910424`
- fixed overlap: `45` samples

Profile `2-5` optimizer comparisons:

| run | time samples | shift / polarity | best loss | epsr | background conductivity |
| --- | ---: | --- | ---: | ---: | ---: |
| `030` | `61` | `+18`, `-1` borrowed from profile `0-3` | `0.732343` | `4.708607` | `0.008067 S/m` |
| `034` | `81` | `+33`, `+1` profile-specific | `0.739720` | `4.041367` | `0.006477 S/m` |
| `035` | `61` | `+24`, `+1` profile-specific | `0.726952` | `3.805530` | `0.004238 S/m` |

Corrected scorecard `037` candidate:

- x: `9.665786 m`
- cover/depth z: `1.507821 m`
- best profile window: `2-5`
- assumed y window: `0.2-0.5 m`
- epsr: Fast-GPR candidate `3.805530`, analytic event `3.830539`
- background conductivity: `0.004238 S/m`
- anomaly conductivity: `0.050000 S/m`
- supported diameter range: `8-30 mm`
- source shift/polarity: `+2.4 ns`, polarity `+1`

## Current Decision

`field_3d_0701_predictor_candidate_ready_with_diameter_degeneracy_flag`

The best current scorecard candidate is profile-window scoped and profile-aligned.
It is materially better than the profile `0-3` candidate, but the 61-sample
profile alignment used by the best run has a boundary-shift caveat. The wider
81-sample alignment confirms polarity `+1` and a later source shift, but changes
the objective window enough that losses are not directly comparable.

## Claim Boundary

The candidate is now closer to the requested deliverable: it reports x, y-window,
z/depth, diameter range, epsr, and conductivity from real B-scan/stack data.
However, it is still a local-window Gaussian-proxy Fast-GPR predictor, not a
full 3D steel-cylinder FDTD inversion.

## Next Defensible Task

Run a profile `2-5` alignment with a wider shift range while preserving a 61-sample
comparison target, or implement a continuous differentiable time-shift parameter
inside the optimizer. This should remove the boundary-shift caveat before
claiming the `+2.4 ns` alignment as final.

## Validation

- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_local_window_bridge_smoke.py tests/test_field_3d_0701_fastgpr_local_window_time_polarity_ladder.py tests/test_field_3d_0701_fastgpr_local_window_aligned_scalar_epsr_optimizer.py tests/test_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py tests/test_field_3d_0701_fastgpr_aligned_predictor_scorecard.py tests/test_field_3d_0701_fastgpr_profile_window_transfer_ladder.py -q`
- Result: `20 passed`
- `conda run -n dev python -m pytest tests/test_field_3d_0701_fastgpr_local_window_bridge_smoke.py tests/test_field_3d_0701_fastgpr_local_window_time_polarity_ladder.py tests/test_field_3d_0701_fastgpr_local_window_aligned_scalar_epsr_optimizer.py tests/test_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py tests/test_field_3d_0701_fastgpr_aligned_predictor_scorecard.py tests/test_field_3d_0701_fastgpr_profile_window_transfer_ladder.py -q`
- Result: `20 passed`
- `git diff --check` on the touched scripts, tests, and checkpoint docs

## Marathon Status

The local field-data predictor marathon remains active; this is a checkpoint,
not a stop.

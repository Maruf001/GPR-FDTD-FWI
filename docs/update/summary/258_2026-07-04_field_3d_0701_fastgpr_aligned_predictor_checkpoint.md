# 258 2026-07-04 Field 3D 0701 Fast-GPR Aligned Predictor Checkpoint

## What Changed

- Added a fixed-overlap Fast-GPR local-window source time/polarity ladder.
- Added aligned scalar epsr Adam using the measured source alignment.
- Added aligned smooth-anomaly geometry/material Adam.
- Added a rebar-scale constrained geometry/material rerun.
- Added a predictor scorecard that consolidates the analytic 3D event candidate and aligned Fast-GPR candidates.

## Key Artifacts

- `021_field_3d_0701_fastgpr_local_window_time_polarity_ladder/`
- `022_field_3d_0701_fastgpr_local_window_time_polarity_ladder_wide/`
- `023_field_3d_0701_fastgpr_local_window_aligned_scalar_epsr_optimizer/`
- `024_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer/`
- `025_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer_rebar_scale/`
- `026_field_3d_0701_fastgpr_aligned_predictor_scorecard/`

## Method

The Fast-GPR field objective now uses the corrected local field window:

- trace window: `363-393`
- trace stride: `2`
- effective field dx: `0.0512 m`
- target window for the wide alignment: `15.625-21.625 ns`
- Fast-GPR dt: `0.1 ns`
- fixed overlap for alignment/scored objective: `37` time samples

The source/time calibration is scored with a fixed overlap so large shifts do not
win just by discarding difficult waveform samples.

## Key Numbers

- Wide source alignment best shift: `+18` Fast-GPR samples = `+1.8 ns`
- Wide source alignment best polarity: `-1`
- Wide alignment baseline loss: `0.864574`
- Wide alignment best loss: `0.755577`
- Alignment improvement: `0.108997` normalized L1, `12.61%`

Aligned optimizer results:

| run | best loss | best epsr | depth / proxy | runtime |
| --- | ---: | ---: | ---: | ---: |
| scalar epsr | `0.753237` | `4.079820` | n/a | `0.192 s/iter` |
| broad smooth anomaly | `0.753071` | `3.978348` | depth `1.440 m`, diameter proxy `353 mm` | `0.256 s/iter` |
| rebar-scale anomaly | `0.753234` | `4.063327` | depth `1.508 m`, diameter proxy `30 mm` | `0.256 s/iter` |

Current consolidated candidate from scorecard `026`:

- x: `9.665786 m`
- cover/depth z: `1.507821 m`
- epsr: analytic event `3.830539`, Fast-GPR rebar-scale best `4.063327`
- supported diameter range: `8-30 mm`
- supported length-y range: `0.095178-0.191499 m`
- source shift/polarity: `+1.8 ns`, polarity `-1`

## Current Decision

`field_3d_0701_predictor_candidate_ready_with_diameter_degeneracy_flag`

The aligned Fast-GPR path is now useful as a real-data optimizer pipeline. The
strongest shippable statement is not a single unique diameter; it is a candidate
with a diameter-degeneracy flag. A rebar-scale `30 mm` proxy and a much broader
smooth anomaly differ by only `0.000163` normalized L1 on this local objective.

## Still Not Modeled

- conductivity inversion
- steel-cylinder physics instead of Gaussian anomaly proxy
- full 3D Fast-GPR/FDTD y-position and length inversion
- profile/window transfer validation beyond the current local window

## Next Defensible Task

Add conductivity as an aligned optimizer parameter and compare constrained
steel/rebar-scale candidates against the broad smooth anomaly. After that, run
the same predictor scorecard over additional windows/profiles to test whether
the x/depth/diameter/epsr candidate remains stable.

## Validation

- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_local_window_time_polarity_ladder.py tests/test_field_3d_0701_fastgpr_local_window_aligned_scalar_epsr_optimizer.py tests/test_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py tests/test_field_3d_0701_fastgpr_aligned_predictor_scorecard.py -q`
- Result: `13 passed`
- `conda run -n dev python -m pytest tests/test_field_3d_0701_fastgpr_local_window_time_polarity_ladder.py tests/test_field_3d_0701_fastgpr_local_window_aligned_scalar_epsr_optimizer.py tests/test_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py tests/test_field_3d_0701_fastgpr_aligned_predictor_scorecard.py -q`
- Result: `13 passed`
- `python -m py_compile run_field_3d_0701_fastgpr_local_window_time_polarity_ladder.py run_field_3d_0701_fastgpr_local_window_aligned_scalar_epsr_optimizer.py run_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py run_field_3d_0701_fastgpr_aligned_predictor_scorecard.py`
- `git diff --check` on the new scripts/tests
- Figure checks: artifacts `021-026` are nonblank PNGs.

## Marathon Status

The local field-data predictor marathon remains active; this is a checkpoint,
not a stop.

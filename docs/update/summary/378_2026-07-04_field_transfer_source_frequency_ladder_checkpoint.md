# Field Transfer Source-Frequency Ladder Checkpoint

## What changed
- Updated the local Fast-GPR time/polarity ladder so the Ricker source frequency and amplitude are explicit inputs instead of a hard-coded 100 MHz source.
- Added a focused unit test for source frequency/amplitude mapping.
- Reran source-consistent time/polarity ladders for the follow-up transfer scans:
  - `0704` at 20 MHz
  - `07011` at 10 MHz
- Added the daily update for Saturday, July 4, 2026.

## Key numbers
- 0704 source-consistent ladder:
  - source frequency `20 MHz`
  - best shift `+0.2 ns`
  - best polarity `-1`
  - best loss `0.832048`
  - improvement vs positive zero-shift baseline `0.004491`
  - prediction standard deviation `1.51e-9`
  - observed standard deviation `0.2956`
- 07011 source-consistent ladder:
  - source frequency `10 MHz`
  - best shift `-2.2 ns`
  - best polarity `-1`
  - best loss `0.830876`
  - improvement vs positive zero-shift baseline `0.049308`
  - prediction standard deviation `1.48e-9`
  - observed standard deviation `0.2812`

## Current decision
The previous time-shift findings were not caused by the hard-coded ladder frequency: 0704 still prefers a small positive shift and 07011 still prefers a negative shift. The stronger blocker is source/amplitude modeling, because the simulated direct-wave amplitude in these ladders is many orders of magnitude smaller than the normalized observed field window.

## What remains blocked
- 0704 and 07011 should not be promoted from these diagnostics.
- The next repair should focus on source amplitude, source injection, acquisition geometry, or field-window normalization before rerunning expensive geometry/material optimizers.

## Validation/resource checks
- `python -m py_compile run_field_3d_0701_fastgpr_local_window_time_polarity_ladder.py tests/test_field_3d_0701_fastgpr_local_window_time_polarity_ladder.py`: passed.
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_local_window_time_polarity_ladder.py -q`: `6 passed`.
- `git diff --check` on touched ladder, daily update, and checkpoint files: passed.
- Figures for the two source-consistent ladders opened with nonzero dimensions.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/354_field_3d_0704_fastgpr_time_polarity_ladder_transfer_seed_mid_profile4_sample60_source20`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/355_field_3d_07011_fastgpr_time_polarity_ladder_transfer_seed_profile0_sample66_source10`
- `docs/update/daily_update/2026-06-29_to_2026-07-05_daily_update.md`

## Next defensible task
Add an amplitude/source diagnostic that compares simulated and observed window scales under the same acquisition geometry, then decide whether to introduce a learnable source scale or repair source injection before the next transfer optimizer run.

## Marathon status
The requested local marathon remains active. Continue with real-data source/amplitude repair and product-focused validation.

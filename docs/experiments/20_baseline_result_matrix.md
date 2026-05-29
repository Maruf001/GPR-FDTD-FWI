# Experiment 20: Baseline Result Matrix

## Goal

Create a machine-readable baseline table for all saved single-rebar runs before launching more paper-guided experiments.

## Outputs

```text
outputs/experiments/single_rebar_baseline_matrix.csv
```

## Summary Table

| experiment | noise_fraction | recovered_x_mm | recovered_z_mm | recovered_radius_mm | radius_error_mm | best_misfit | nrms_data_primary | best_radius_mm | next_radius_mm | radius_margin_abs | elapsed_time_s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 007_single_rebar_grid1mm_cli_smoke | 0 | 235 | 80 | 8 | 2 | 0.09444 | 0.03132 |  |  |  | 2.937 |
| 008_single_rebar_grid1mm_de_5src_60eval_bounded | 0 | 105.7 | 127.8 | 7.83 | 1.83 | 1.045 | 0.1773 |  |  |  | 319.2 |
| 009_single_rebar_grid1mm_powell_refine_from_2mm | 0 | 249.5 | 90.65 | 6.955 | 0.9548 | 0.002083 | 0.00789 |  |  |  | 266.6 |
| 014_single_rebar_grid1mm_gridpolish_from_run009 | 0 | 250 | 89.75 | 6 | 0 | 0 | 0 |  |  |  | 865.7 |
| 015_single_rebar_grid1mm_powell_gridpolish_from_2mm | 0 | 250 | 89.75 | 6 | 0 | 0 | 0 |  |  |  | 1124 |
| 016_single_rebar_grid1mm_gridpolish_earlystop_from_run009 | 0 | 250 | 89.75 | 6 | 0 | 0 | 0 |  |  |  | 15.84 |
| 017_single_rebar_grid1mm_noise01_gridpolish | 0.01 | 250 | 89.75 | 6 | 0 | 0.002483 | 0.01005 |  |  |  | 1119 |
| 018_single_rebar_grid1mm_noise05_gridpolish | 0.05 | 250 | 89.75 | 6 | 0 | 0.05856 | 0.05021 |  |  |  | 1127 |
| 019_single_rebar_grid1mm_noise05_gridpolish_stop006 | 0.05 | 250 | 89.75 | 6 | 0 | 0.05856 | 0.05021 |  |  |  | 15.92 |
| 020_single_rebar_grid1mm_noise05_coarsepolish | 0.05 | 250 | 90 | 6 | 0 | 0.05856 | 0.05021 |  |  |  | 490.5 |
| 021_single_rebar_grid1mm_noise05_seed21_coarsepolish | 0.05 | 250 | 90 | 6 | 0 | 0.05772 | 0.04983 |  |  |  | 483.6 |
| 022_single_rebar_grid1mm_noise10_coarsepolish | 0.1 | 250 | 90 | 6 | 0 | 0.1992 | 0.1001 |  |  |  | 487.1 |
| 023_single_rebar_grid1mm_noise10_coarsepolish_topk | 0.1 | 250 | 90 | 6 | 0 | 0.1992 | 0.1001 | 6 | 6.2 | 0.0005594 | 224.3 |
| 027_trace_shift_summary_smoke | 0 | 235 | 80 | 8 | 2 | 0.07579 | 0.03427 |  |  |  | 2.951 |
| 028_bandpass_objective_summary_smoke | 0 | 235 | 80 | 8 | 2 | 0.007893 | 0.03427 |  |  |  | 2.894 |
| 029_bandwidth_stage1_020_080_from_2mm | 0 | 249.8 | 90.59 | 6.573 | 0.5735 | 0.0001005 | 0.01068 |  |  |  | 185.3 |
| 030_bandwidth_stage2_020_110_from_stage1 | 0 | 249.7 | 90.73 | 6.864 | 0.864 | 8.653e-05 | 0.00789 |  |  |  | 185.2 |
| 031_bandwidth_stage3_full_from_stage2_coarsepolish | 0 | 250 | 90 | 6 | 0 | 0 | 0 | 6 | 6.2 | 0.001037 | 361 |
| 032_bandwidth_full_from_stage1_no_polish | 0 | 249.5 | 90.65 | 6.955 | 0.9548 | 0.002083 | 0.00789 |  |  |  | 263.6 |
| 033_bandwidth_stage1_then_full_coarsepolish | 0 | 250 | 90 | 6 | 0 | 0 | 0 | 6 | 6.2 | 0.001037 | 215.9 |
| 034_bandwidth_noise05_stage1_020_080_seed13 | 0.05 | 250.4 | 90.53 | 6.999 | 0.9989 | 0.0003611 | 0.05092 |  |  |  | 185.4 |
| 035_bandwidth_noise05_full_coarsepolish_from_lowband_seed13 | 0.05 | 250 | 90 | 6 | 0 | 0.05856 | 0.05021 | 6 | 6.2 | 0.0008169 | 216.7 |
| 036_bandwidth_noise10_stage1_020_080_seed13 | 0.1 | 249.9 | 90.77 | 6.927 | 0.9271 | 0.001188 | 0.1005 |  |  |  | 186 |
| 037_bandwidth_noise10_full_coarsepolish_from_lowband_seed13 | 0.1 | 250 | 90 | 6 | 0 | 0.1992 | 0.1001 | 6 | 6.2 | 0.0005594 | 217.5 |
| 038_cumulative_frequency_misfit_summary_smoke | 0 | 235 | 80 | 8 | 2 | 0.03984 | 0.03427 |  |  |  | 5.869 |
| 039_cumulative_frequency_gridpolish_topk_smoke | 0 | 250 | 90 | 6 | 0 | 0 | 0 | 6 |  |  | 8.752 |
| 040_cumulative_frequency_10_15_coarsepolish_from_highradius | 0 | 250 | 90 | 6 | 0 | 0 | 0 | 6 | 6.2 | 0.0005364 | 451.6 |
| 041_cumulative_frequency_weighted_objective_smoke | 0 | 235 | 80 | 8 | 2 | 0.0638 | 0.03427 |  |  |  | 5.874 |
| 042_plotting_template_validation_smoke | 0 | 235 | 80 | 8 | 2 | 0.07579 | 0.03427 |  |  |  | 2.917 |

## Current Interpretation

This table is an index for comparing future experiments. Use the CSV for filtering and the top-candidate margin columns for radius confidence checks.

## Pondered Result

Key baseline facts before new paper-guided experiments:

```text
single-frequency exact coarse polish:
  r=6.0 beats r=6.2 by about 1.037e-03

5% noise coarse polish:
  r=6.0 beats r=6.2 by about 8.169e-04

10% noise coarse polish:
  r=6.0 beats r=6.2 by about 5.594e-04

unweighted 1.0+1.5 GHz exact coarse polish:
  r=6.0 beats r=6.2 by about 5.364e-04
```

Interpretation:

```text
Noise and naive lower-frequency averaging both shrink radius confidence.
The next experiment should not be another broad optimizer run. It should be
spectrum-driven PEBDD design so band choices are based on actual source,
observed, and candidate-residual spectra.
```

Next action:

```text
Experiment 21: spectrum-driven PEBDD setup.
```

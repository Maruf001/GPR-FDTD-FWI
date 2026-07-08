# Field 3D 0701 Combined-Window Objective Checkpoint

## What Changed

- Extended the finite-length joint optimizer with `--sample-starts`, allowing one optimization run to average receiver-mean scattered loss across multiple real-data windows.
- Ran combined-window 20 MHz source-frequency objective over sample starts `30,40,50`.
- Stress-tested diameter seeds `8 mm` and `12 mm`.
- Synthesized the combined-window diameter stability result.

## Key Numbers

- Combined-window optimizer runs:
  - `258_field_3d_0701_fastgpr_finite_length_joint_combined_windows_30_40_50_source20mhz_seed_len010_diam08_adamw_iter3`
  - `259_field_3d_0701_fastgpr_finite_length_joint_combined_windows_30_40_50_source20mhz_seed_len010_diam12_adamw_iter3`
- Synthesis artifact:
  - `260_field_3d_0701_combined_window_source20_diameter_seed_stability`
- Synthesis decision:
  - `finite_length_joint_xz_material_stability_supports_010m_length_not_diameter`
- Combined-window best:
  - label `combined_source20_diam08`
  - objective loss `0.660975575`
  - field L1 loss `0.660956025`
- Near-best ranges:
  - length `0.096881904-0.096882388 m`
  - diameter `8.000393398-11.999592185 mm`
- Max gradients:
  - radius `3.106112478e-09`
  - length `4.949193681e-05`
  - source-time shift `1.795907505e-02`
  - background epsr `7.999237860e-04`

## What Remains Blocked

- The combined-window objective does not identify diameter.
- It is more robust than a single time window but does not outperform the best single late-window 20 MHz fit (`0.600213468`).
- Radius gradient remains negligible.

## Current Decision

Combined multi-window fitting is useful as a robustness check, not as a diameter resolver.

The current product benchmark remains the single late-window 20 MHz source-frequency fit, while the combined-window run confirms the finite-length estimate and the diameter range boundary.

## Next Defensible Task

If continuing optimization, do not repeat the same geometry objective. Next useful directions are:

- richer antenna/source waveform parameterization;
- independent diameter calibration data;
- or a real-data profile transfer test on another 2025 stack row.

## Validation And Resources

- Focused/product suite:
  - `64 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile ...`
  - passed for changed scripts/tests
- touched-file `git diff --check`
  - passed
- Figure check:
  - `260.../figures/field_3d_0701_finite_length_optimizer_seed_stability.png`: size `(2365, 767)`, stddev `64.779`

## Artifact Paths

- Combined-window synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/260_field_3d_0701_combined_window_source20_diameter_seed_stability`
- Product package remains:
  - `outputs/validation_exp_on_field_data/product_leaderboard/062_field_prediction_product_package`
- Checkpoint:
  - `docs/update/summary/333_2026-07-04_field_3d_0701_combined_window_objective_checkpoint.md`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.

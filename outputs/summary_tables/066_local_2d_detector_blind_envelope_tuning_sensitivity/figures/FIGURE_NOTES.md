# Figure Notes

## `local_2d_detector_blind_envelope_tuning_sensitivity.png`

This CPU-only figure decomposes why the two close50 nominal cases
are tuning-sensitive under the blind-envelope policy grid.

Policy label: `local_2d_detector_blind_envelope_tuning_sensitivity_cpu_no_fwi`.
Tuning-sensitive cases: `2`.
Maximum knob effect: `1.0`.
Top-effect knob: `structural_weight`.
Structural-weight direction conflict: `True`.
Support-weight direction conflict: `True`.
Ready for global policy tuning fix: `False`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

Outputs:

- Knob-effect rows: `local_2d_detector_blind_envelope_tuning_sensitivity_knob_effects.csv`.
- Feature-contrast rows: `local_2d_detector_blind_envelope_tuning_sensitivity_features.csv`.

Scope boundary:

This audit reads saved CPU detector summaries only. It does not run FDTD, FWI,
GPU kernels, 3D/HPC jobs, or neural-network training.


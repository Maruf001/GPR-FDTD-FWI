# Figure Notes

## `local_2d_detector_parameter_sensitivity.png`

This figure summarizes CPU-only detector rescoring over saved B-scans from
the same-case close14/close50 detector baseline. It does not rerun FDTD, FWI,
GPU kernels, field FWI, or 3D/HPC work.

Policy label: `local_2d_detector_parameter_sensitivity_saved_bscan_cpu`.
Configurations: `81`.
Case/config rows: `972`.
Rescued cases: `12`.
Best config: `median_top40_moderate12_single667`.
Best-config mean max assigned rank: `23.416666666666668`.
Best-config worst max assigned rank: `36.0`.
GPU used: `False`.

Saved-B-scan detector sensitivity recovered all truths in every case for at
least one configuration, so the earlier negative detector baseline is a
parameter-setting artifact. Because some recoveries require deeper candidate
ranks, this is candidate-list recoverability, not yet a clean standalone
top-pick detector result.

Outputs:

- Case/config rows: `local_2d_detector_parameter_sensitivity_rows.csv`.
- Config summary: `local_2d_detector_parameter_sensitivity_config_summary.csv`.
- Case summary: `local_2d_detector_parameter_sensitivity_case_summary.csv`.
- Summary: `local_2d_detector_parameter_sensitivity_summary.json`.

# Figure Notes

## `local_2d_detector_selector_counterfactual_sensitivity.png`

This CPU-only analysis tests simple one-dimensional reweighting around
the current local 2D geometry-family detector selector.

Policy label: `local_2d_detector_selector_counterfactual_sensitivity_cpu_no_fwi`.
Counterfactual variants: `44`.
Base all-truth cases: `3`.
Best counterfactual: `signed_gap_sweep_w2`.
Best all-truth cases: `3`.
Best improvement over base: `0`.
Best dominant loss feature: `signed_gap_prior_score`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

Outputs:

- Variant rows: `local_2d_detector_selector_counterfactual_sensitivity_rows.csv`.
- Family summary: `local_2d_detector_selector_counterfactual_sensitivity_family_summary.csv`.

Scope boundary:

This audit reads saved detector rows only. It does not run FDTD, FWI,
GPU kernels, field FWI, 3D/HPC jobs, or neural-network training.


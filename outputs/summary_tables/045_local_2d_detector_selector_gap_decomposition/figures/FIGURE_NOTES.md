# Figure Notes

## `local_2d_detector_selector_gap_decomposition.png`

This CPU-only analysis decomposes why the current geometry-family detector
selector still misses all-truth triples on saved local 2D detector cases.

Policy label: `local_2d_detector_selector_gap_decomposition_cpu_no_fwi`.
Selector label: `cb0.5_hy0.2_min0_span0.5_sgap4_center0.2_rank0.1`.
Selected all-truth cases: `3` / `12`.
Median required selector gain: `0.18097749906867877`.
Max required selector gain: `0.5505405776977454`.
Dominant loss feature: `signed_gap_prior_score`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

Outputs:

- Per-case gap rows: `local_2d_detector_selector_gap_decomposition_cases.csv`.
- Feature summary: `local_2d_detector_selector_gap_decomposition_feature_summary.csv`.
- Branch summary: `local_2d_detector_selector_gap_decomposition_branch_summary.csv`.

Scope boundary:

This audit reads saved detector rows only. It does not run FDTD, FWI,
GPU kernels, field FWI, 3D/HPC jobs, or neural-network training.


# Figure Notes

## `local_2d_detector_geometry_family_selector.png`

This CPU-only audit evaluates branch-family geometry priors over saved
component-gated detector triples.

Policy label: `local_2d_detector_geometry_family_selector_cpu_no_fwi`.
Selector candidates: `2160`.
Best in-sample selector: `cb0.5_hy0.2_min0_span0.5_sgap4_center0.2_rank0.1`.
Best in-sample all-truth cases: `3`.
Leave-one-case all-truth cases: `2`.
Improvement over component selector, in-sample: `2`.
Improvement over component selector, leave-one-case: `2`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

Outputs:

- Selector summary: `local_2d_detector_geometry_family_selector_summary.csv`.
- Best selected cases: `local_2d_detector_geometry_family_selector_best_cases.csv`.
- Cross-validation cases: `local_2d_detector_geometry_family_selector_cv_cases.csv`.

Scope boundary:

This audit reads saved CPU rows only. It does not run FDTD, FWI,
GPU kernels, field FWI, 3D/HPC jobs, or neural-network training.


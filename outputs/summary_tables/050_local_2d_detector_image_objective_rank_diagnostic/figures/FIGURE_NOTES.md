# Figure Notes

## `local_2d_detector_image_objective_rank_diagnostic.png`

This CPU-only diagnostic reads saved image-objective rows from run 027
and asks how deep the first all-truth row appears under each objective.

Policy label: `local_2d_detector_image_objective_rank_diagnostic_cpu_no_fwi`.
Best objective: `row_background_sigma100`.
Best top-50 all-truth cases: `0`.
Best top-1000 all-truth cases: `6`.
Best median first all-truth rank: `639.0`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

Outputs:

- Case ranks: `local_2d_detector_image_objective_rank_cases.csv`.
- Objective summary: `local_2d_detector_image_objective_rank_summary.csv`.

Scope boundary:

This audit reads saved image-objective rows only. It does not run FDTD, FWI,
GPU kernels, field FWI, 3D/HPC jobs, or neural-network training.


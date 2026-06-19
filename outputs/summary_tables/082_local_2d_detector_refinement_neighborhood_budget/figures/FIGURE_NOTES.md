# Figure Notes

## `local_2d_detector_refinement_neighborhood_budget.png`

This CPU-only figure sizes coordinate neighborhoods from saved detector seed errors.

Policy label: `local_2d_detector_refinement_neighborhood_budget_cpu_no_fwi`.
Stable seed cases: `10`.
Review cases: `2`.
Min half-width for all stable cases: `10.0` mm.
Per-case h10 step2 grid points: `1771561.0`.
Ready for narrow refinement contract: `False`.
Ready for detector-seeded FWI: `False`.
GPU priority: `none`.

Outputs:

- Half-width rows: `local_2d_detector_refinement_neighborhood_half_width_rows.csv`.
- Grid budget rows: `local_2d_detector_refinement_neighborhood_grid_budget_rows.csv`.

Scope boundary:

This audit reads saved detector contract and seed-export artifacts only. It does not run FDTD,
FWI, GPU kernels, field FWI, 3D/HPC jobs, or neural-network training.

